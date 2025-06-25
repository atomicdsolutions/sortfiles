"""Progress tracking models for file operations."""

from dataclasses import dataclass

@dataclass
class ProgressSummary:
    """
    Tracks overall progress of file operations.

    Attributes:
        total_files: Total number of files to process
        completed: Number of completed files
        in_progress: Number of files currently being processed
        skipped: Number of skipped files (e.g., duplicates)
        errors: Number of failed operations
        total_bytes: Total bytes to process
        processed_bytes: Number of bytes processed so far
        empty_dirs_found: Number of empty directories found
        empty_dirs_removed: Number of empty directories removed
        cleanup_errors: Number of errors during cleanup
    """

    total_files: int = 0
    completed: int = 0
    in_progress: int = 0
    skipped: int = 0
    errors: int = 0
    total_bytes: int = 0
    processed_bytes: int = 0
    empty_dirs_found: int = 0
    empty_dirs_removed: int = 0
    cleanup_errors: int = 0

    @property
    def percent_complete(self) -> float:
        """Calculate the overall progress percentage."""
        if self.total_bytes == 0:
            return 0.0
        return round((self.processed_bytes / self.total_bytes * 100), 2)

    def update_cleanup_progress(self, found: int = 0, removed: int = 0, errors: int = 0) -> None:
        """
        Update cleanup operation progress.
        
        Args:
            found: Number of empty directories found
            removed: Number of empty directories removed
            errors: Number of errors encountered during cleanup
        """
        self.empty_dirs_found += found
        self.empty_dirs_removed += removed
        self.cleanup_errors += errors

    def to_dict(self) -> dict:
        """Convert the summary to a dictionary for JSON serialization."""
        return {
            "total_files": self.total_files,
            "completed": self.completed,
            "in_progress": self.in_progress,
            "skipped": self.skipped,
            "errors": self.errors,
            "total_bytes": self.total_bytes,
            "processed_bytes": self.processed_bytes,
            "percent_complete": self.percent_complete,
            "empty_dirs_found": self.empty_dirs_found,
            "empty_dirs_removed": self.empty_dirs_removed,
            "cleanup_errors": self.cleanup_errors,
        }