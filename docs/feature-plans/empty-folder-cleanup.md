# Empty Folder Cleanup Feature Implementation Plan

## Overview

This document outlines the implementation plan for adding automatic cleanup of empty folders after file transfer operations in the SortFiles application.

## Requirements

1. Automatically remove empty folders in the source directory after files are moved
2. Handle nested empty directories recursively
3. Provide configuration options to control cleanup behavior
4. Track and report cleanup operations
5. Handle errors gracefully
6. Add tests for the new functionality

## Implementation Steps

### 1. Core Functionality

#### a. Create Cleanup Utility Module
- Create `sortfiles/utils/cleanup_utils.py`
- Implement functions:
  - `is_directory_empty(path: str) -> bool`
  - `remove_empty_directory(path: str) -> bool`
  - `cleanup_empty_directories(root_path: str, recursive: bool = True) -> List[str]`

#### b. Progress Monitoring Integration
- Add cleanup operations to `ProgressSummary` class
- Update progress monitoring to track cleanup operations
- Add cleanup status to web interface updates

#### c. Configuration Integration
- Add cleanup-related settings to configuration
- Implement cleanup control flags in CLI

### 2. Integration

#### a. File Operations Integration
- Modify `move_files()` function to initiate cleanup after successful moves
- Add cleanup status to operation results
- Handle cleanup errors appropriately

#### b. CLI Integration
- Add cleanup-related command line arguments:
  - `--cleanup-empty-dirs`: Enable/disable cleanup (default: True)
  - `--cleanup-recursive`: Clean nested directories (default: True)

#### c. Web Interface Updates
- Add cleanup status display
- Show cleanup progress
- List removed directories

### 3. Testing

#### a. Unit Tests
- Test cleanup utility functions
- Test configuration integration
- Test progress monitoring updates

#### b. Integration Tests
- Test cleanup with file operations
- Test recursive directory handling
- Test error conditions

#### c. Web Interface Tests
- Test cleanup status display
- Test cleanup progress updates

## Implementation Details

### 1. Cleanup Utility Functions

```python
def is_directory_empty(path: str) -> bool:
    """
    Check if a directory is empty.
    
    Args:
        path: Directory path to check
        
    Returns:
        bool: True if directory is empty
    """
    pass

def remove_empty_directory(path: str) -> bool:
    """
    Remove an empty directory.
    
    Args:
        path: Directory path to remove
        
    Returns:
        bool: True if directory was removed
    """
    pass

def cleanup_empty_directories(root_path: str, recursive: bool = True) -> List[str]:
    """
    Remove empty directories under the root path.
    
    Args:
        root_path: Starting directory for cleanup
        recursive: Whether to handle nested directories
        
    Returns:
        List[str]: List of removed directory paths
    """
    pass
```

### 2. Progress Monitoring Updates

```python
@dataclass
class ProgressSummary:
    # Add new fields
    empty_dirs_removed: int = 0
    cleanup_errors: int = 0
    
    def update_cleanup_progress(self, removed_dirs: int, errors: int = 0):
        """Update cleanup operation progress."""
        pass
```

### 3. Configuration Updates

```python
# In config.py
CLEANUP_CONFIG = {
    'enabled': True,
    'recursive': True,
    'ignore_patterns': ['.git', '__pycache__'],
}
```

### 4. CLI Integration

```python
def parse_args():
    """Add new arguments for cleanup configuration."""
    parser.add_argument(
        '--cleanup-empty-dirs',
        action='store_true',
        default=True,
        help='Remove empty directories after moving files'
    )
    parser.add_argument(
        '--cleanup-recursive',
        action='store_true',
        default=True,
        help='Recursively remove nested empty directories'
    )
```

## Testing Plan

### 1. Unit Tests

```python
def test_is_directory_empty():
    """Test empty directory detection."""
    pass

def test_remove_empty_directory():
    """Test directory removal."""
    pass

def test_cleanup_empty_directories():
    """Test recursive cleanup."""
    pass

def test_cleanup_with_ignore_patterns():
    """Test ignored directory patterns."""
    pass
```

### 2. Integration Tests

```python
def test_cleanup_after_move():
    """Test cleanup after file move operations."""
    pass

def test_cleanup_nested_directories():
    """Test handling of nested empty directories."""
    pass

def test_cleanup_error_handling():
    """Test cleanup error scenarios."""
    pass
```

## Future Enhancements

1. Add more granular control over which directories to clean
2. Implement dry-run mode for cleanup operations
3. Add cleanup operation logging
4. Support for cleanup scheduling
5. Add cleanup statistics to operation reports

## Timeline

1. Core Implementation: 2-3 days
2. Testing: 1-2 days
3. Documentation: 1 day
4. Code Review & Refinements: 1-2 days

Total: 5-8 days