"""Integration tests for directory cleanup with file operations."""

import os
import shutil
import pytest
from pathlib import Path

from sortfiles.core.file_operations import move_files
from sortfiles.utils.cleanup_utils import is_directory_empty

@pytest.fixture
def setup_test_environment(tmp_path):
    """Create a test environment with source and destination directories."""
    # Create directory structure
    source_dir = tmp_path / "source"
    dest_dir = tmp_path / "destination"
    
    # Create nested directories in source
    dir1 = source_dir / "dir1"
    dir2 = source_dir / "dir2"
    nested_dir = dir2 / "nested"
    
    for d in [source_dir, dest_dir, dir1, dir2, nested_dir]:
        d.mkdir()
    
    # Create test files
    test_files = [
        dir1 / "file1.txt",
        dir2 / "file2.txt",
        nested_dir / "file3.txt"
    ]
    
    for f in test_files:
        f.write_text("test content")
    
    return {
        "source_dir": source_dir,
        "dest_dir": dest_dir,
        "test_files": test_files
    }

def test_cleanup_after_move(setup_test_environment):
    """Test cleanup of empty directories after moving files."""
    env = setup_test_environment
    source_dir = env["source_dir"]
    dest_dir = env["dest_dir"]
    test_files = env["test_files"]
    
    # Move files with cleanup enabled
    move_files(
        file_list=[str(f) for f in test_files],
        destination=str(dest_dir),
        delete_source=True,
        cleanup_enabled=True,
        cleanup_recursive=True
    )
    
    # Check that files were moved
    for file in test_files:
        source_file = file
        dest_file = dest_dir / file.name
        assert not source_file.exists()
        assert dest_file.exists()
        assert dest_file.read_text() == "test content"
    
    # Check that empty directories were removed
    assert not (source_dir / "dir1").exists()
    assert not (source_dir / "dir2" / "nested").exists()
    assert not (source_dir / "dir2").exists()

def test_cleanup_without_delete_source(setup_test_environment):
    """Test that cleanup is not performed when delete_source is False."""
    env = setup_test_environment
    source_dir = env["source_dir"]
    dest_dir = env["dest_dir"]
    test_files = env["test_files"]
    
    # Copy files without deleting source
    move_files(
        file_list=[str(f) for f in test_files],
        destination=str(dest_dir),
        delete_source=False,
        cleanup_enabled=True,
        cleanup_recursive=True
    )
    
    # Check that directories still exist
    assert (source_dir / "dir1").exists()
    assert (source_dir / "dir2" / "nested").exists()
    assert (source_dir / "dir2").exists()

def test_non_recursive_cleanup(setup_test_environment):
    """Test non-recursive cleanup of empty directories."""
    env = setup_test_environment
    source_dir = env["source_dir"]
    dest_dir = env["dest_dir"]
    test_files = env["test_files"]
    
    # Move files with non-recursive cleanup
    move_files(
        file_list=[str(f) for f in test_files],
        destination=str(dest_dir),
        delete_source=True,
        cleanup_enabled=True,
        cleanup_recursive=False
    )
    
    # Check that only top-level empty directories were removed
    assert not (source_dir / "dir1").exists()  # Should be removed
    assert (source_dir / "dir2").exists()  # Should remain
    assert (source_dir / "dir2" / "nested").exists()  # Should remain

def test_cleanup_with_remaining_files(setup_test_environment):
    """Test cleanup behavior when some files remain in directories."""
    env = setup_test_environment
    source_dir = env["source_dir"]
    dest_dir = env["dest_dir"]
    test_files = env["test_files"]
    
    # Create an extra file that won't be moved
    remaining_file = source_dir / "dir2" / "keep.txt"
    remaining_file.write_text("keep this file")
    
    # Move only some files
    move_files(
        file_list=[str(f) for f in test_files[:2]],  # Move only first two files
        destination=str(dest_dir),
        delete_source=True,
        cleanup_enabled=True,
        cleanup_recursive=True
    )
    
    # Check that directory with remaining file exists
    assert (source_dir / "dir2").exists()
    assert remaining_file.exists()
    assert remaining_file.read_text() == "keep this file"
    
    # But empty dir1 should be removed
    assert not (source_dir / "dir1").exists()

def test_cleanup_error_handling(setup_test_environment):
    """Test error handling during cleanup operations."""
    env = setup_test_environment
    source_dir = env["source_dir"]
    dest_dir = env["dest_dir"]
    test_files = env["test_files"]
    
    # Create a directory with insufficient permissions
    restricted_dir = source_dir / "dir2" / "restricted"
    restricted_dir.mkdir()
    os.chmod(restricted_dir, 0o000)
    
    try:
        # Move files - cleanup should continue despite errors
        move_files(
            file_list=[str(f) for f in test_files],
            destination=str(dest_dir),
            delete_source=True,
            cleanup_enabled=True,
            cleanup_recursive=True
        )
        
        # Check that other directories were cleaned up
        assert not (source_dir / "dir1").exists()
        
    finally:
        # Restore permissions for cleanup
        os.chmod(restricted_dir, 0o755)
        shutil.rmtree(restricted_dir)