"""Command line interface for the application."""

import os
import sys
import time
import socket
import webbrowser
import argparse
import multiprocessing as mp
from pathlib import Path
from typing import List, Dict, Any, Optional

from .config import CLEANUP_CONFIG
from .core.file_operations import move_files
from .core.path_utils import get_file_type
from .utils.progress_monitor import progress_monitor
from .web.app import start_web_interface, open_browser
from .models.state import state

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Sort files into directories based on their creation date.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Sort files from source to destination (copy mode):
    sortfiles /path/to/source /path/to/destination

  Sort files recursively (including subdirectories):
    sortfiles --recursive /path/to/source /path/to/destination

  Sort files and delete source after successful copy:
    sortfiles --delete-source /path/to/source /path/to/destination

  Sort files and start web interface:
    sortfiles --web /path/to/source /path/to/destination

  Sort files with custom port:
    sortfiles --web --port 8081 /path/to/source /path/to/destination

  Sort files and disable cleanup of empty directories:
    sortfiles --no-cleanup /path/to/source /path/to/destination

  Sort files with non-recursive cleanup:
    sortfiles --no-recursive-cleanup /path/to/source /path/to/destination
        """,
    )

    parser.add_argument("source", help="Source directory containing files to sort")
    parser.add_argument("destination", help="Destination directory for sorted files")
    parser.add_argument(
        "--web", action="store_true", help="Start web interface for monitoring progress"
    )
    parser.add_argument(
        "--port", type=int, default=8080, help="Port for web interface (default: 8080)"
    )
    parser.add_argument(
        "--delete-source", action="store_true", help="Delete source files after successful copy"
    )
    parser.add_argument(
        "--type", choices=["image", "video", "audio"], help="Filter by file type"
    )
    parser.add_argument(
        "--test", action="store_true", help="Run in test mode (no files will be moved)"
    )
    parser.add_argument(
        "--recursive", action="store_true", help="Process files in subdirectories (default: only root)"
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    # Add cleanup-related arguments
    parser.add_argument(
        "--no-cleanup", 
        action="store_true",
        help="Disable cleanup of empty directories after file operations"
    )
    parser.add_argument(
        "--no-recursive-cleanup",
        action="store_true",
        help="Disable recursive cleanup of nested empty directories"
    )

    return parser.parse_args()