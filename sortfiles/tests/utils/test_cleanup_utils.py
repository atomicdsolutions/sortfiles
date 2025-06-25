"""Unit tests for directory cleanup utilities."""

import os
import shutil
import pytest
from pathlib import Path
from typing import Set

from sortfiles.utils.cleanup_utils import (
    is_directory_empty,
    remove_empty_directory,
    get_empty_directories,
    cleanup_empty_directories
)

@pytest.fixture
def test_dir(tmp_path):
    """Create a temporary directory structure for testing."""
    # Create test directory structure
    root = tmp_path / "test_root"
    root.mkdir()
    
    # Create nested directories
    dir1 = root / "dir1"
    dir2 = root / "dir2"
    dir3 = root / "dir2" / "dir3"
    empty_dir = root / "empty_dir"
    
    for d in [dir1, dir2, dir3, empty_dir]:
        d.mkdir()
    
    # Create some files
    (dir1 / "file1.txt").write_text("content1")
    (dir2 / "file2.txt").write_text("content2")
    
    return root

def test_is_directory_empty(test_dir):
    """Test empty directory detection."""
    # Test empty directory
    empty_dir = test_dir / "empty_dir"
    assert is_directory_empty(str(empty_dir)) is True
    
    # Test non-empty directory
    non_empty_dir = test_dir / "dir1"
    assert is_directory_empty(str(non_empty_dir)) is False
    
    # Test non-existent directory
    with pytest.raises(OSError):
        is_directory_empty(str(test_dir / "nonexistent"))

def test_remove_empty_directory(test_dir):
    """Test directory removal."""
    # Test removing empty directory
    empty_dir = test_dir / "empty_dir"
    assert remove_empty_directory(str(empty_dir)) is True
    assert not empty_dir.exists()
    
    # Test removing non-empty directory
    non_empty_dir = test_dir / "dir1"
    assert remove_empty_directory(str(non_empty_dir)) is False
    assert non_empty_dir.exists()
    
    # Test removing non-existent directory
    assert remove_empty_directory(str(test_dir / "nonexistent")) is False

def test_get_empty_directories(test_dir):
    """Test finding empty directories."""
    empty_dirs = get_empty_directories(str(test_dir))
    
    # Should find only the empty_dir
    assert len(empty_dirs) == 1
    assert str(test_dir / "empty_dir") in empty_dirs
    
    # Create new empty nested directories
    nested_empty = test_dir / "dir2" / "dir3" / "empty_nested"
    nested_empty.mkdir()
    
    empty_dirs = get_empty_directories(str(test_dir))
    assert len(empty_dirs) == 2
    assert str(nested_empty) in empty_dirs
    assert str(test_dir / "empty_dir") in empty_dirs

def test_get_empty_directories_with_ignore_patterns(test_dir):
    """Test finding empty directories with ignore patterns."""
    # Create some directories that should be ignored
    git_dir = test_dir / ".git"
    git_dir.mkdir()
    
    pycache_dir = test_dir / "__pycache__"
    pycache_dir.mkdir()
    
    ignore_patterns = {".git", "__pycache__"}
    empty_dirs = get_empty_directories(str(test_dir), ignore_patterns)
    
    # Should not include ignored directories
    assert str(git_dir) not in empty_dirs
    assert str(pycache_dir) not in empty_dirs

def test_cleanup_empty_directories(test_dir):
    """Test recursive cleanup of empty directories."""
    # Create nested empty directories
    nested_empty1 = test_dir / "dir2" / "dir3" / "empty1"
    nested_empty2 = test_dir / "dir2" / "dir3" / "empty2"
    nested_empty1.mkdir()
    nested_empty2.mkdir()
    
    # Run cleanup
    removed_dirs = cleanup_empty_directories(str(test_dir))
    
    # Check that empty directories were removed
    assert len(removed_dirs) == 3  # empty_dir, empty1, empty2
    assert not nested_empty1.exists()
    assert not nested_empty2.exists()
    assert not (test_dir / "empty_dir").exists()
    
    # Check that non-empty directories remain
    assert (test_dir / "dir1").exists()
    assert (test_dir / "dir2").exists()

def test_cleanup_empty_directories_non_recursive(test_dir):
    """Test non-recursive cleanup of empty directories."""
    # Create nested empty directories
    nested_empty = test_dir / "dir2" / "dir3" / "empty_nested"
    nested_empty.mkdir()
    
    # Run non-recursive cleanup
    removed_dirs = cleanup_empty_directories(str(test_dir), recursive=False)
    
    # Should only remove top-level empty directory
    assert len(removed_dirs) == 1
    assert str(test_dir / "empty_dir") in removed_dirs
    assert nested_empty.exists()

def test_cleanup_empty_directories_error_handling(test_dir):
    """Test error handling during cleanup."""
    # Create a directory with insufficient permissions
    restricted_dir = test_dir / "restricted"
    restricted_dir.mkdir()
    os.chmod(restricted_dir, 0o000)
    
    try:
        # Cleanup should continue despite errors
        removed_dirs = cleanup_empty_directories(str(test_dir))
        
        # Should have removed other empty directories
        assert str(test_dir / "empty_dir") in removed_dirs
        
    finally:
        # Restore permissions for cleanup
        os.chmod(restricted_dir, 0o755)
        shutil.rmtree(restricted_dir)