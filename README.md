# SortFiles

A Python application for automatically organizing and sorting files by type with a user-friendly web interface. The application helps you keep your files organized by automatically categorizing and moving them to appropriate directories based on their types.

## Features

- **Automated File Organization**: Automatically categorize and move files based on their types (images, videos, audio, etc.)
- **Web Interface**: Monitor the organization process through an intuitive web interface
- **Real-time Progress**: Track file operations in real-time with detailed progress information
- **Duplicate Handling**: Smart handling of duplicate files with content comparison
- **Flexible Configuration**: Support for various file types and custom organization rules
- **Recursive Processing**: Option to process files in subdirectories
- **Dry Run Mode**: Test mode to preview changes without actually moving files
- **Source Cleanup**: Option to delete source files after successful transfer and clean up empty directories

## Installation

### Option 1: Install from PyPI (Recommended)

The easiest way to install SortFiles is using pip:

```bash
pip install sortfiles
```

After installation, the `sortfiles` command will be available in your terminal.

### Option 2: Install from Source

1. Clone the repository:
```bash
git clone https://github.com/atomicdsolutions/sortfiles.git
cd sortfiles
```

2. Install the package:
```bash
# For development (editable install)
pip install -e .

# For regular installation
pip install .
```

After installation using either method, the `sortfiles` command will be available system-wide.

## Usage

### Command Line Interface

Basic usage:
```bash
sortfiles /path/to/source /path/to/destination
```

Options:
```bash
# Start with web interface
sortfiles --web /source/path /dest/path

# Specify custom port for web interface
sortfiles --web --port 8080 /source/path /dest/path

# Delete source files after successful transfer
sortfiles --delete-source /source/path /dest/path

# Run in test mode (no actual file operations)
sortfiles --test /source/path /dest/path

# Filter by file type
sortfiles --type image /source/path /dest/path

# Process subdirectories
sortfiles --recursive /source/path /dest/path

# Directory cleanup options
sortfiles --no-cleanup /source/path /dest/path          # Disable empty directory cleanup
sortfiles --no-recursive-cleanup /source/path /dest/path # Disable recursive cleanup
```

For full command options:
```bash
sortfiles --help
```

### Web Interface

1. Start the application with the web interface:
```bash
sortfiles --web /path/to/source /path/to/destination
```

2. Open your browser to `http://localhost:8080` (a browser window should open automatically)

3. Monitor and manage file operations through the web interface

## Development

### Setting up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/atomicdsolutions/sortfiles.git
cd sortfiles
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e .
```

### Running Tests

```bash
pytest
```

### Code Style

The project follows PEP 8 guidelines. To format your code:

```bash
black .
```

To run type checks:
```bash
mypy .
```

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Submit a pull request

## Docker Support

Coming soon!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. Command not found after installation:
   - Make sure your Python scripts directory is in your PATH
   - Try running `pip install --user sortfiles` if installing globally
   - In a virtual environment, ensure it's activated

2. Permission issues:
   - Use `sudo pip install sortfiles` for system-wide installation
   - Or install for current user with `pip install --user sortfiles`

3. Web interface not opening:
   - Check if port 8080 is available
   - Use `--port` option to specify a different port
   - Ensure no firewall is blocking the connection

### Getting Help

- Check the [GitHub Issues](https://github.com/atomicdsolutions/sortfiles/issues) for known problems
- Create a new issue if you find a bug
- Join our community for support (coming soon)

## Project Status

The project is actively maintained and in stable release. Check the [GitHub repository](https://github.com/atomicdsolutions/sortfiles) for the latest updates and releases.