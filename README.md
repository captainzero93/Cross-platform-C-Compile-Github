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
  pip install pathlib
  ```

## Build Tools Installation

### Windows

#### 1. Native Windows Tools

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

#### 2. MSYS2 Environment (Required for Make and Autotools on Windows)
MSYS2 provides Unix-like tools on Windows, including its own package manager called `pacman`.

1. **Download and Install MSYS2**
   - Download [MSYS2](https://www.msys2.org/)
   - Run the installer (msys2-x86_64-yyyymmdd.exe)
   - Complete the installation (default: C:\msys64)

2. **Install Required Tools**
   - Open "MSYS2 MINGW64" from Start Menu
   - Run these commands in the MSYS2 terminal:
     ```bash
     # Update MSYS2 first
     pacman -Syu
     # Close and reopen terminal when prompted
     pacman -Syu

     # Install MinGW-w64 toolchain and build tools
     pacman -S --needed mingw-w64-x86_64-toolchain
     pacman -S --needed mingw-w64-x64-cmake mingw-w64-x86_64-ninja mingw-w64-x86_64-make mingw-w64-x86_64-autotools
     pacman -S --needed autoconf automake libtool make
     ```

3. **Add to System PATH**
   - Open Windows Settings
   - Search for "Environment Variables"
   - Edit the "Path" variable
   - Add these paths IN ORDER:
     ```
     C:\msys64\mingw64\bin
     C:\msys64\usr\bin
     ```

### Linux

Choose the commands for your distribution:

#### Debian/Ubuntu
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

#### Fedora/RHEL
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

#### Arch Linux
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

### Verifying Installation

#### Windows
Open a new Command Prompt (not MSYS2) and verify:
```cmd
gcc --version
make --version
cmake --version
autoconf --version
automake --version
```

#### Linux
Open a terminal and verify:
```bash
gcc --version
make --version
cmake --version
autoconf --version
automake --version
```

## Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/captainzero93/github-c-builder.git
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

1. **Command not found errors**
   - Verify PATH entries are correct
   - Log out and log back in, or restart computer
   - Check if binaries exist in the specified directories
   - Ensure PATH order is correct (mingw64\bin before usr\bin)

2. **Visual Studio Build Tools errors**
   - Verify installation is complete
   - Try running "Developer Command Prompt for VS 2022"
   - Repair or reinstall Visual Studio Build Tools

3. **MSYS2 issues**
   - Use "MSYS2 MINGW64" for package installation
   - If updates fail, try `pacman -Syu --needed`
   - For DLL errors, verify PATH order and MINGW64 packages

4. **CMake configuration fails**
   - Ensure CMake is in System PATH
   - Check if the project supports Windows
   - Try running from "Developer Command Prompt for VS 2022"

### Linux Common Issues

1. **Missing dependencies**
   - Run package manager update (apt update, etc.)
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

## Windows Terminal Choice

1. **For Installing Packages**
   - Use "MSYS2 MINGW64" terminal

2. **For Building Projects**
   - Use regular Windows Command Prompt or PowerShell
   - Or use "Developer Command Prompt for VS 2022"

3. **When to use "MSYS2 MSYS"**
   - Only if specifically required by a project
   - Not recommended for general use

## Maintenance

### Windows MSYS2
Update packages regularly:
```bash
# In MSYS2 MINGW64 terminal
pacman -Syu
```

### Linux
Keep build tools updated:
```bash
# Debian/Ubuntu
sudo apt update && sudo apt upgrade

# Fedora
sudo dnf update

# Arch Linux
sudo pacman -Syu
```

## Debugging

When errors occur, the builder provides detailed error messages including:
- Build tool output
- Git operation results
- Directory operation status
- Platform-specific error details

Logs can be found in:
- Build output in the /build directory
- CMake configuration logs
- MSBuild detailed output (Windows)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or need help:
1. Check the Troubleshooting section
2. Open an issue on GitHub
3. Provide detailed error messages and system information

Remember to always check the project's original documentation for specific build requirements or dependencies.
