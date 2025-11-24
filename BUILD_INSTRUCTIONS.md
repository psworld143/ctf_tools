# Building Windows Executable

This guide explains how to build a standalone Windows executable (.exe) from the CTF Tool Selector Python script.

## Prerequisites

- Windows 10/11
- Python 3.7 or higher
- pip (Python package manager)

## Quick Build

### Method 1: Using Build Script (Recommended)

1. Open Command Prompt or PowerShell in the project directory
2. Run:
   ```batch
   build_windows.bat
   ```

The script will:
- Check for Python installation
- Install PyInstaller if needed
- Build the executable
- Place it in the `dist` folder

### Method 2: Manual Build

1. Install PyInstaller:
   ```batch
   pip install pyinstaller
   ```

2. Build the executable:
   ```batch
   pyinstaller --onefile --name "CTF_Tool_Selector" --console --add-data "ai_providers.sql;." ctf_tool_selector.py
   ```

3. Find the executable in `dist\CTF_Tool_Selector.exe`

## Build Options Explained

- `--onefile`: Creates a single executable file (easier to distribute)
- `--name "CTF_Tool_Selector"`: Sets the output filename
- `--console`: Keeps the console window visible (for CLI interface)
- `--add-data "ai_providers.sql;."`: Bundles the SQL file with the executable
- `--clean`: Cleans PyInstaller cache before building
- `--noconfirm`: Overwrites existing build without asking

## Using the Spec File

For advanced customization, you can use the `pyinstaller.spec` file:

```batch
pyinstaller pyinstaller.spec
```

Edit `pyinstaller.spec` to customize:
- Icon file
- Additional data files
- Hidden imports
- UPX compression
- And more

## Output

After building, you'll find:
- `dist/CTF_Tool_Selector.exe` - The standalone executable
- `build/` - Temporary build files (can be deleted)
- `CTF_Tool_Selector.spec` - PyInstaller spec file (if generated)

## Distribution

The `CTF_Tool_Selector.exe` file is completely standalone:
- ✅ No Python installation required
- ✅ All dependencies bundled
- ✅ Can be run on any Windows 10/11 machine
- ✅ Can be distributed via USB, email, or download

## Troubleshooting

### "Python is not installed"
- Install Python from python.org
- Make sure Python is added to PATH during installation

### "pip is not recognized"
- Use `python -m pip` instead of just `pip`
- Or reinstall Python with "Add Python to PATH" option

### Build fails with import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that `requests` library is installed

### Executable is too large
- This is normal for PyInstaller one-file builds (includes Python runtime)
- Typical size: 15-30 MB
- Consider using `--onedir` instead of `--onefile` for smaller size (but requires folder distribution)

### Executable doesn't find ai_providers.sql
- Make sure `--add-data "ai_providers.sql;."` is included in the build command
- The semicolon (`;`) is important for Windows paths

## Advanced: Adding an Icon

1. Create or download a `.ico` file
2. Add to build command:
   ```batch
   pyinstaller --onefile --icon=icon.ico --name "CTF_Tool_Selector" ...
   ```

## File Size Optimization

To reduce executable size:
- Use `--onedir` instead of `--onefile` (creates a folder with multiple files)
- Add `--exclude-module` for unused modules
- Use UPX compression (already enabled in spec file)

## Testing the Executable

After building:
1. Navigate to `dist` folder
2. Double-click `CTF_Tool_Selector.exe`
3. Test all features:
   - Tool selection
   - Challenge analyzer
   - Tool installation

## Notes

- First run may be slower (extracting bundled files)
- Windows Defender may flag new executables (false positive - safe to allow)
- The executable includes all API keys (as per your configuration)

