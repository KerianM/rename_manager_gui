# File Rename Manager

[English](README.md) | [简体中文](README_CN.md)

A GUI tool for batch renaming files and folders with support for recursive operations.

## Features

- Add prefix to files/folders
- Add suffix to files/folders (before extension)
- Remove specific strings from filenames
- Replace strings in filenames
- Undo last operation
- Support for recursive operations in subdirectories
- Option to process current directory files only
- Option to include/exclude folders in rename operations
- Directory selection for operations
- Real-time file list preview
- Operation history tracking
- Remember last opened directory

## Usage

1. Run the application:
```bash
python rename_manager_gui.py
```

2. Select working directory:
   - Click "Select Directory" to choose the directory you want to work with
   - The current directory path is displayed at the top of the window
   - The program remembers your last opened directory

3. Configure options:
   - Check "Current directory only" to process files in the current directory only
   - Check "Include folders" to include folders in rename operations
   - Uncheck both to process files in all subdirectories recursively

4. Choose an operation:
   - **Add Prefix**: Add text to the beginning of filenames
   - **Add Suffix**: Add text before the file extension
   - **Remove String**: Remove specific text from filenames
   - **Replace String**: Replace text in filenames
   - **Undo**: Revert the last rename operation
   - **Refresh**: Update the file list

5. Enter the required text in the dialog box and confirm.

## Requirements

- Python 3.12.0 or higher
- tkinter (usually comes with Python)

## Configuration Files

The program maintains two configuration files in its installation directory:
- `settings.ini`: Stores program settings like the last opened directory
- `.rename_history`: Keeps track of rename operations for the undo feature

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.