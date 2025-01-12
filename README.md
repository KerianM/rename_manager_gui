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
- Real-time file list preview
- Operation history tracking

## Usage

1. Run the application:
```bash
python rename_manager_gui.py
```

2. The main window will show all files and folders in the current directory and its subdirectories.

3. Choose an operation:
   - **Add Prefix**: Add text to the beginning of filenames
   - **Add Suffix**: Add text before the file extension
   - **Remove String**: Remove specific text from filenames
   - **Replace String**: Replace text in filenames
   - **Undo**: Revert the last rename operation
   - **Refresh**: Update the file list

4. Enter the required text in the dialog box and confirm.

## Requirements

- Python 3.12.0
- tkinter (usually comes with Python)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
