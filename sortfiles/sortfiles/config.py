"""Configuration settings for the application."""

import os
import importlib.util
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Directory paths
SCRIPT_DIR = Path(__file__).parent.resolve()
TEMPLATE_DIRS = [
    SCRIPT_DIR / "web" / "templates",
    SCRIPT_DIR / "templates",
]

# File extensions
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac"}
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv"}
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
PHOTO_VIDEO_EXTENSIONS = PHOTO_EXTENSIONS.union(VIDEO_EXTENSIONS)

# Required Python packages
REQUIRED_PACKAGES = [
    "flask",
    "flask-socketio",
    "exifread",
    "pathlib",
]

# Cleanup configuration
CLEANUP_CONFIG = {
    'enabled': True,  # Enable cleanup by default
    'recursive': True,  # Clean nested directories by default
    'ignore_patterns': {  # Directories to ignore during cleanup
        '.git',
        '__pycache__',
        '.pytest_cache',
        '.mypy_cache',
        'node_modules',
        'venv',
        '.venv',
    }
}

# Logging verbosity
VERBOSE = False

def check_and_install_dependencies():
    """Check and install required Python packages."""
    for package in REQUIRED_PACKAGES:
        if not importlib.util.find_spec(package):
            logger.warning(f"Required package {package} not found. Please install it using pip.")
            return False
    return True

def get_template_dir() -> Path:
    """Find the first valid template directory."""
    for template_dir in TEMPLATE_DIRS:
        if template_dir.exists():
            return template_dir
    raise FileNotFoundError("No valid template directory found")