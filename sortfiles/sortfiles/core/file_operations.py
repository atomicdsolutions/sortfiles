"""Core file operations for moving and organizing files."""

import os
import sys
import shutil
import logging
from typing import Dict, List, Optional, Tuple
from multiprocessing import Pool
from pathlib import Path

from ..utils.hash_utils import calculate_file_hash
from ..utils.cleanup_utils import cleanup_empty_directories
from ..config import CLEANUP_CONFIG

logger = logging.getLogger(__name__)

def create_operation(
    src: str,
    dest: str,
    size: int = 0,
) -> Dict[str, Any]:
    """Create a dictionary representing a file operation."""
    return {
        "source": src,
        "destination": dest,
        "size": size,
        "status": "pending",
        "progress": 0,
        "error": None,
    }

def update_summary_stats(
    progress_dict: Dict,
    operation: Dict[str, Any],
    status: str,
    completed_bytes: int = 0,
) -> None:
    """Update summary statistics in the progress dictionary."""
    if "summary" not in progress_dict:
        progress_dict["summary"] = {
            "total_files": 0,
            "completed": 0,
            "in_progress": 0,
            "errors": 0,
            "total_bytes": 0,
            "processed_bytes": 0,
        }

    summary = progress_dict["summary"]
    
    if status == "completed":
        summary["completed"] += 1
        summary["processed_bytes"] += completed_bytes
    elif status == "error":
        summary["errors"] += 1
    elif status == "in_progress":
        summary["in_progress"] += 1
        summary["processed_bytes"] += completed_bytes

def update_operation_status(
    progress_dict: Dict,
    operation: Dict[str, Any],
    status: str,
    progress: int = 0,
    error: str = None,
) -> None:
    """Update the status of a file operation."""
    operation["status"] = status
    operation["progress"] = progress
    operation["error"] = error
    
    if progress_dict is not None:
        progress_dict[operation["source"]] = (progress, status)
        update_summary_stats(
            progress_dict,
            operation,
            status,
            operation["size"] if status == "completed" else 0
        )

def handle_duplicate_file(src: str, dest: str) -> Optional[str]:
    """
    Handle duplicate files by comparing content and generating unique names.
    
    Returns:
        str or None: New destination path, or None if file should be skipped
    """
    if not os.path.exists(dest):
        return dest

    # Compare file contents
    src_hash = calculate_file_hash(src)
    dest_hash = calculate_file_hash(dest)
    
    if src_hash == dest_hash:
        # Files are identical, skip
        return None
        
    # Generate unique name
    base, ext = os.path.splitext(dest)
    counter = 1
    while os.path.exists(dest):
        dest = f"{base}_{counter}{ext}"
        counter += 1
        
    return dest

def move_single_file(
    src: str,
    dest: str,
    delete_source: bool = True,
    progress_dict: Dict = None
) -> None:
    """
    Move a single file with progress tracking.
    
    Args:
        src: Source file path
        dest: Destination file path
        delete_source: Whether to delete source after successful copy
        progress_dict: Dictionary for tracking progress
    """
    try:
        # Create operation record
        operation = create_operation(src, dest, os.path.getsize(src))
        
        # Update status to in_progress
        update_operation_status(progress_dict, operation, "in_progress")
        
        # Ensure destination directory exists
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        
        if delete_source:
            # Move file
            shutil.move(src, dest)
        else:
            # Copy file
            shutil.copy2(src, dest)
            
        # Update status to completed
        update_operation_status(progress_dict, operation, "completed", 100)
        
    except Exception as e:
        # Update status to error
        update_operation_status(progress_dict, operation, "error", 0, str(e))
        raise

def move_files(
    file_list: List[str],
    destination: str,
    progress_dict: Dict = None,
    verbose: bool = False,
    test: bool = False,
    delete_source: bool = True,
    cleanup_enabled: bool = True,
    cleanup_recursive: bool = True,
) -> None:
    """
    Move multiple files in parallel with progress tracking.

    Args:
        file_list: List of source file paths
        destination: Destination directory path
        progress_dict: Dictionary for tracking progress
        verbose: Whether to print verbose output
        test: Whether to run in test mode (no actual file operations)
        delete_source: Whether to delete source files after successful move
        cleanup_enabled: Whether to clean up empty directories after moving files
        cleanup_recursive: Whether to recursively clean up nested empty directories
    """
    try:
        # Create list of (source, destination) tuples
        file_tuples = []
        source_dirs = set()  # Keep track of source directories for cleanup
        
        for src in file_list:
            dest = os.path.join(destination, os.path.basename(src))
            source_dirs.add(os.path.dirname(src))
            
            # Initialize progress for this file
            if progress_dict is not None:
                progress_dict[src] = (0, "pending")
            
            # Handle duplicate files
            final_dest = handle_duplicate_file(src, dest)
            if final_dest is None:
                # File is a duplicate, skip it
                if progress_dict is not None:
                    progress_dict[src] = (100, "skipped")
                if verbose:
                    print(f"Skipping duplicate file: {src}")
                continue
                
            file_tuples.append((src, final_dest))

        if not test:
            # Process files in parallel
            with Pool() as pool:
                results = []
                for src, dest in file_tuples:
                    result = pool.apply_async(
                        move_single_file,
                        args=(src, dest, delete_source, progress_dict),
                    )
                    results.append((result, src))

                # Wait for all operations to complete
                for result, src in results:
                    try:
                        result.get()
                        if verbose:
                            print(f"Moved {src}")
                    except Exception as e:
                        if progress_dict is not None:
                            progress_dict[src] = (0, "error")
                        print(f"Error moving {src}: {e}")
                        raise

            # Clean up empty directories if enabled
            if cleanup_enabled and delete_source:
                for source_dir in source_dirs:
                    try:
                        removed_dirs = cleanup_empty_directories(
                            source_dir,
                            recursive=cleanup_recursive,
                            ignore_patterns=CLEANUP_CONFIG['ignore_patterns']
                        )
                        if verbose and removed_dirs:
                            print(f"Removed empty directories: {', '.join(removed_dirs)}")
                            
                        # Update progress if available
                        if progress_dict is not None and "summary" in progress_dict:
                            progress_dict["summary"]["empty_dirs_removed"] = len(removed_dirs)
                            
                    except Exception as e:
                        logger.error(f"Error cleaning up directory {source_dir}: {e}")
                        if progress_dict is not None and "summary" in progress_dict:
                            progress_dict["summary"]["cleanup_errors"] = \
                                progress_dict["summary"].get("cleanup_errors", 0) + 1

    except Exception as e:
        print(f"Error in move_files: {e}")
        raise