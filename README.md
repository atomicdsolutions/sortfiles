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
- **Source Cleanup**: Option to delete source files after successful transfer

## Installation

1. Clone the repository:
```bash
git clone https://github.com/atomicdsolutions/sortfiles.git
cd sortfiles
```

2. Install the package:
```bash
pip install -e .
```

## Usage

### Command Line Interface

Basic usage:
```bash
python sortfiles.py [source_directory] [destination_directory] [options]
```

Options:
- `--web`: Launch with web interface
- `--port PORT`: Specify web interface port (default: 8080)
- `--delete-source`: Delete source files after successful transfer
- `--test`: Run in test mode (no actual file operations)
- `--file-type TYPE`: Filter by file type (image, video, audio)
- `--recursive`: Process subdirectories

### Web Interface

1. Start the application with the web interface:
```bash
python sortfiles.py /path/to/source /path/to/destination --web
```

2. Open your browser to `http://localhost:8080` (a browser window should open automatically)

3. Monitor and manage file operations through the web interface

## Improvement Roadmap

### Phase 1: Core Functionality Enhancements

1. **Empty Folder Cleanup**
   - Implement automatic cleanup of empty source folders after file transfers
   - Add configuration option to control cleanup behavior
   - Include cleanup status in progress monitoring

2. **Smart Duplicate Handling**
   - Enhance duplicate detection with more sophisticated algorithms
   - Add options for handling duplicate files (rename, skip, overwrite)
   - Provide duplicate file reports

3. **Extended File Type Support**
   - Add support for more file types and categories
   - Implement custom file type rules
   - Add file type detection based on content

### Phase 2: User Experience Improvements

4. **Enhanced Web Interface**
   - Add drag-and-drop file upload
   - Implement dark mode
   - Add file preview capabilities
   - Improve progress visualization

5. **Configuration Management**
   - Add GUI for configuration settings
   - Support for saving and loading configurations
   - Profile-based configurations

### Phase 3: Advanced Features

6. **File Organization Rules**
   - Custom organization rules using patterns
   - Support for complex file naming conventions
   - Automated file renaming based on metadata

7. **Metadata Processing**
   - Extract and use file metadata for organization
   - Support for custom metadata tags
   - Advanced search and filter capabilities

8. **Integration Features**
   - Cloud storage integration
   - Scheduled organization tasks
   - API for external tool integration

### Phase 4: Performance & Reliability

9. **Performance Optimizations**
   - Parallel processing improvements
   - Memory usage optimization
   - Handling of large file collections

10. **Backup & Recovery**
    - Automatic backup of file operations
    - Operation rollback capabilities
    - Recovery from interrupted operations

## Code Organization

The project follows a modular structure:

```
sortfiles/
├── sortfiles/
│   ├── core/
│   │   ├── date_utils.py
│   │   ├── file_operations.py
│   │   └── path_utils.py
│   ├── web/
│   │   ├── app.py
│   │   ├── socket_handlers.py
│   │   └── operations_utils.py
│   ├── utils/
│   │   ├── hash_utils.py
│   │   └── progress_monitor.py
│   ├── models/
│   │   ├── operations.py
│   │   ├── progress.py
│   │   └── state.py
│   └── config.py
├── tests/
│   ├── core/
│   ├── web/
│   ├── utils/
│   └── models/
└── setup.py
```

## Development Guidelines

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints for function parameters and returns
   - Include docstrings for all modules, classes, and functions

2. **Testing**
   - Write unit tests for all new features
   - Use pytest for testing
   - Maintain test coverage above 80%

3. **Version Control**
   - Create feature branches for new development
   - Write descriptive commit messages
   - Keep pull requests focused and manageable

4. **Documentation**
   - Keep README and docstrings up to date
   - Document configuration options
   - Include examples for new features

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.