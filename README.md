# GitHub C Project Builder

A Python script that automatically downloads and builds C projects from GitHub repositories. Supports multiple build systems including CMake, Make, and Autotools.

## Features

- Automatic build system detection (CMake, Make, Autotools)
- Cross-platform support (Windows, Linux, macOS)
- Organized output structure
- Comprehensive dependency checking
- Detailed error reporting and troubleshooting guidance

## Prerequisites

### Python Requirements

- Python 3.8 or higher
- Required packages:
  ```bash
  pip install pathlib shutil
  ```

### Windows Build Tools

1. **Visual Studio Build Tools**
   - Download: [Visual Studio Build Tools 2022](https://aka.ms/vs/17/release/vs_buildtools.exe)
   - During installation, select:
     - "Desktop development with C++"
     - MSVC Build Tools
     - Windows 10/11 SDK
     - C++ CMake tools

2. **CMake**
   - Download: [CMake](https://cmake.org/download/)
   - Choose "Windows x64 Installer"
   - During installation, select "Add CMake to system PATH"

3. **Git**
   - Download: [Git for Windows](https://git-scm.com/download/win)
   - During installation, select "Add to PATH"

4. **MSYS2** (for Make and Autotools)
   - Download: [MSYS2](https://www.msys2.org/)
   - Install and open "MSYS2 MSYS" from Start Menu
   - Run the following commands:
     ```bash
     # Update package database and base packages
     pacman -Syu

     # Close and reopen terminal when prompted, then run:
     pacman -Syu

     # Install development tools
     pacman -S --needed base-devel mingw-w64-x86_64-toolchain autotools mingw-w64-x86_64-cmake

     # Install specific tools
     pacman -S make automake autoconf libtool
     ```
   - Add to System PATH:
     - Open "Edit the system environment variables"
     - Click "Environment Variables"
     - Edit "Path"
     - Add:
       ```
       C:\msys64\usr\bin
       C:\msys64\mingw64\bin
       ```

### Linux Build Tools

For Debian/Ubuntu:
```bash
# Update package list
sudo apt update

# Install build essentials
sudo apt install -y build-essential

# Install CMake
sudo apt install -y cmake

# Install Git
sudo apt install -y git

# Install Autotools
sudo apt install -y autoconf automake libtool
```

For Fedora/RHEL:
```bash
# Install development tools
sudo dnf groupinstall "Development Tools"

# Install CMake
sudo dnf install cmake

# Install Git
sudo dnf install git

# Install Autotools
sudo dnf install autoconf automake libtool
```

For Arch Linux:
```bash
# Install development tools
sudo pacman -S base-devel

# Install CMake
sudo pacman -S cmake

# Install Git
sudo pacman -S git

# Install Autotools
sudo pacman -S autoconf automake libtool
```

## Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/yourusername/github-c-builder.git
   cd github-c-builder
   ```

2. Make the script executable (Linux/macOS):
   ```bash
   chmod +x builder.py
   ```

## Usage

Basic usage:
```bash
python builder.py <github_url> [branch]
```

Example:
```bash
python builder.py https://github.com/username/project.git main
```

### Directory Structure

The script creates the following directory structure:
```
github-c-builder/
├── source/             # Cloned repositories
│   └── project_name/
├── build/              # Build files
│   └── project_name/
└── output/             # Compiled binaries and libraries
    └── project_name/
```

## Troubleshooting

### Windows Common Issues

1. **"'make' is not recognized..."**
   - Verify MSYS2 installation
   - Check if paths are added to System PATH
   - Log out and log back in or restart computer

2. **Visual Studio Build Tools errors**
   - Verify installation is complete
   - Try running "Developer Command Prompt for VS 2022"
   - Repair or reinstall Visual Studio Build Tools

3. **CMake configuration fails**
   - Ensure CMake is in System PATH
   - Check if the project supports Windows
   - Try running from "Developer Command Prompt for VS 2022"

### Linux Common Issues

1. **Missing dependencies**
   - Run `sudo apt update` (or equivalent)
   - Install build-essential package
   - Check project-specific dependencies

2. **Permission denied**
   - Use `sudo` for installation commands
   - Check file permissions
   - Ensure write access to output directories

### General Issues

1. **Git clone fails**
   - Verify internet connection
   - Check if repository URL is correct
   - Ensure Git is installed and in PATH

2. **Build system not detected**
   - Check if project uses supported build system
   - Verify source files are properly cloned
   - Look for specific build instructions in project README

## Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest features.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built using Python 3
- Inspired by various build automation tools
- Thanks to the open-source community

## Support

If you encounter any issues or need help:
1. Check the Troubleshooting section
2. Open an issue on GitHub
3. Provide detailed error messages and system information

Remember to always check the project's original documentation for specific build requirements or dependencies.
