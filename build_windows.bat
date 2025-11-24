@echo off
echo ================================================
echo    Building CTF Tool Selector for Windows
echo ================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [!] Python is not installed or not in PATH
    pause
    exit /b 1
)

:: Install PyInstaller if not present
echo Checking for PyInstaller...
pip show pyinstaller >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

:: Create build directory
if not exist "dist" mkdir dist
if not exist "build" mkdir build

:: Build the executable
echo.
echo Building executable...
echo This may take a few minutes...
echo.

pyinstaller --onefile ^
    --name "CTF_Tool_Selector" ^
    --console ^
    --add-data "ai_providers.sql;." ^
    --hidden-import=requests ^
    --hidden-import=subprocess ^
    --hidden-import=shutil ^
    --hidden-import=platform ^
    --hidden-import=os ^
    --hidden-import=shlex ^
    --hidden-import=textwrap ^
    --hidden-import=typing ^
    --clean ^
    --noconfirm ^
    ctf_tool_selector.py

IF %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo    Build Successful!
    echo ================================================
    echo Executable location: dist\CTF_Tool_Selector.exe
    echo.
    echo You can now distribute this .exe file to Windows users.
    echo They don't need Python installed to run it.
) ELSE (
    echo.
    echo [!] Build failed. Check the error messages above.
)

pause

