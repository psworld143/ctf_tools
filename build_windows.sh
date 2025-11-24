#!/bin/bash
# Build script for Windows executable (run on macOS/Linux with Wine or cross-compile)

echo "================================================"
echo "   Building CTF Tool Selector for Windows"
echo "================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 is not installed"
    exit 1
fi

# Install PyInstaller if not present
echo "Checking for PyInstaller..."
if ! pip3 show pyinstaller &> /dev/null; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
fi

# Create build directories
mkdir -p dist build

# Build the executable
echo
echo "Building executable..."
pyinstaller --onefile \
    --name "CTF_Tool_Selector" \
    --console \
    --add-data "ai_providers.sql:." \
    --hidden-import=requests \
    --hidden-import=subprocess \
    --hidden-import=shutil \
    --hidden-import=platform \
    --hidden-import=os \
    --hidden-import=shlex \
    --hidden-import=textwrap \
    --hidden-import=typing \
    --clean \
    ctf_tool_selector.py

if [ $? -eq 0 ]; then
    echo
    echo "================================================"
    echo "   Build Successful!"
    echo "================================================"
    echo "Executable location: dist/CTF_Tool_Selector"
    echo
    echo "Note: This builds for your current platform."
    echo "For Windows .exe, you need to run this on Windows"
    echo "or use Wine/cross-compilation tools."
else
    echo
    echo "[!] Build failed. Check the error messages above."
    exit 1
fi

