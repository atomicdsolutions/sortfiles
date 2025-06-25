"""Utilities for cleaning up empty directories after file operations."""

import os
import logging
from pathlib import Path
from typing import List, Set

logger = logging.getLogger(__name__)

def is_directory_empty(path: str) -> bool:
    """
    Check if a directory is empty.
    
    Args:
        path: Directory path to check
        
    Returns:
        bool: True if directory is empty (contains no files or subdirectories)
        
    Raises:
        OSError: If there's an error accessing the directory
    """
    try:
        with os.scandir(path) as it:
            return not any(it)
    except OSError as e:
        logger.error(f"Error checking if directory is empty: {path} - {str(e)}")
        raise

def remove_empty_directory(path: str) -> bool:
    """
    Remove an empty directory.
    
    Args:
        path: Directory path to remove
        
    Returns:
        bool: True if directory was removed successfully
    """
    try:
        if is_directory_empty(path):
            os.rmdir(path)
            logger.info(f"Removed empty directory: {path}")
            return True
        return False
    except OSError as e:
        logger.error(f"Error removing directory: {path} - {str(e)}")
        return False

def get_empty_directories(root_path: str, ignore_patterns: Set[str] = None) -> List[str]:
    """
    Find all empty directories under the root path.
    
    Args:
        root_path: Starting directory for search
        ignore_patterns: Set of directory names to ignore (e.g., '.git', '__pycache__')
        
    Returns:
        List[str]: List of paths of empty directories, sorted from deepest to shallowest
    """
    if ignore_patterns is None:
        ignore_patterns = {'.git', '__pycache__', '.pytest_cache', '.mypy_cache'}
        
    empty_dirs = []
    try:
        root = Path(root_path)
        
        # Walk bottom-up so we can identify empty dirs after their contents are processed
        for dirpath, dirnames, filenames in os.walk(root, topdown=False):
            # Skip ignored directories
            dirnames[:] = [d for d in dirnames if d not in ignore_patterns]
            
            # If directory has no files and no subdirectories, it's empty
            if not filenames and not dirnames:
                # Don't include the root directory
                if dirpath != str(root):
                    empty_dirs.append(dirpath)
                    
    except OSError as e:
        logger.error(f"Error scanning directories: {str(e)}")
        
    return empty_dirs

def cleanup_empty_directories(root_path: str, recursive: bool = True, ignore_patterns: Set[str] = None) -> List[str]:
    """
    Remove empty directories under the root path.
    
    Args:
        root_path: Starting directory for cleanup
        recursive: Whether to handle nested directories
        ignore_patterns: Set of directory names to ignore
        
    Returns:
        List[str]: List of removed directory paths
    """
    removed_dirs = []
    
    try:
        # Get list of empty directories
        empty_dirs = get_empty_directories(root_path, ignore_patterns)
        
        # If not recursive, only process direct subdirectories
        if not recursive:
            root = Path(root_path)
            empty_dirs = [d for d in empty_dirs if Path(d).parent == root]
        
        # Remove empty directories
        for dir_path in empty_dirs:
            if remove_empty_directory(dir_path):
                removed_dirs.append(dir_path)
                
    except Exception as e:
        logger.error(f"Error during directory cleanup: {str(e)}")
        
    return removed_dirs