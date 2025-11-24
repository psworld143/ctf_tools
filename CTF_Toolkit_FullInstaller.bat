@echo off
setlocal ENABLEDELAYEDEXPANSION

set MODE=FULL
if /I "%~1"=="install-only" set MODE=INSTALL_ONLY

set root=%USERPROFILE%\Desktop\CTF-Toolkit

if /I "%MODE%"=="INSTALL_ONLY" (
    title CTF Toolkit Installer (Tools Only)
    echo ================================================
    echo        CTF TOOLKIT INSTALLER - TOOLS ONLY
    echo ================================================
) else (
    title CTF Toolkit Installer + Folder Creator
    echo ================================================
    echo          CTF TOOLKIT FULL INSTALLER
    echo ================================================
)
echo.

if /I "%MODE%"=="FULL" (
    call :create_structure
) else (
    echo ▶ Skipping folder creation/organization (install-only mode).
    echo.
)

call :check_winget
call :ensure_choco
call :install_tools

if /I "%MODE%"=="FULL" (
    call :organize_tools
)

echo.
if /I "%MODE%"=="FULL" (
    echo ================================================
    echo     🎉 DONE! Your CTF-Toolkit is ready!
    echo     Location: %root%
    echo ================================================
) else (
    echo ================================================
    echo     ✅ Tools installed successfully!
    echo  Run this script without arguments for full setup.
    echo ================================================
)
pause
endlocal
exit /b

:create_structure
echo [1/5] Creating folder structure...
mkdir "%root%"
mkdir "%root%\01-Web\BurpSuite"
mkdir "%root%\01-Web\Headers"
mkdir "%root%\01-Web\Wordlists"
mkdir "%root%\01-Web\CyberChef"

mkdir "%root%\02-Forensics\PCAPs"
mkdir "%root%\02-Forensics\Images"
mkdir "%root%\02-Forensics\Audio"
mkdir "%root%\02-Forensics\Tools"

mkdir "%root%\03-Crypto\Encodings"
mkdir "%root%\03-Crypto\RSA"
mkdir "%root%\03-Crypto\Tools"

mkdir "%root%\04-OSINT\Screenshots"
mkdir "%root%\04-OSINT\Notes"

mkdir "%root%\05-Reversing\Ghidra"
mkdir "%root%\05-Reversing\Radare2"
mkdir "%root%\05-Reversing\Disassembled"
mkdir "%root%\05-Reversing\Strings"

mkdir "%root%\06-Misc\QR"
mkdir "%root%\06-Misc\Stego"
mkdir "%root%\06-Misc\Other"

mkdir "%root%\Tools-Binaries\exiftool"
mkdir "%root%\Tools-Binaries\binwalk"
mkdir "%root%\Tools-Binaries\zsteg"
mkdir "%root%\Tools-Binaries\hashcat"
mkdir "%root%\Tools-Binaries\john"
mkdir "%root%\Tools-Binaries\utilities"
mkdir "%root%\Tools-Binaries\ghidra"
mkdir "%root%\Tools-Binaries\radare2"
mkdir "%root%\Tools-Binaries\wireshark"

mkdir "%root%\Notes"
echo > "%root%\Notes\Flags-Found.txt"
echo > "%root%\Notes\Commands.txt"
echo > "%root%\Notes\Hints.txt"

echo Done creating directories.
echo.
goto :eof

:check_winget
echo Checking Winget...
winget --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Winget is not installed. Please update your Windows 10/11.
    pause
    exit /b
)
echo Winget OK.
echo.
goto :eof

:ensure_choco
echo Checking Chocolatey...
where choco >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo 🟡 Installing Chocolatey...
    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "Set-ExecutionPolicy Bypass -Scope Process; ^
     [System.Net.ServicePointManager]::SecurityProtocol = 3072; ^
     iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
)
echo Chocolatey OK.
echo.
goto :eof

:install_tools
echo Installing tools...
echo 🔹 Installing Exiftool...
winget install PhilHarvey.ExifTool -e --silent

echo 🔹 Installing Binwalk...
choco install binwalk -y

echo 🔹 Installing zsteg...
choco install zsteg -y

echo 🔹 Installing Hashcat...
winget install hashcat -e --silent

echo 🔹 Installing John the Ripper...
choco install john -y

echo 🔹 Installing coreutils (strings/xxd)...
winget install GnuWin32.CoreUtils -e --silent

echo 🔹 Installing ncat (nc) via Nmap...
winget install nmap -e --silent

echo 🔹 Installing curl...
winget install curl -e --silent

echo 🔹 Installing Ghidra...
winget install NSA.Ghidra -e --silent

echo 🔹 Installing radare2...
choco install radare2 -y

echo 🔹 Installing Wireshark...
winget install WiresharkFoundation.Wireshark -e --silent

echo 🔹 Installing Burp Suite Community...
winget install PortSwigger.BurpSuiteCommunity -e --silent

echo 🔹 Installing CyberChef...
winget install GCHQ.CyberChef -e --silent
echo.
goto :eof

:organize_tools
echo [5/5] Organizing installed tools into CTF Toolkit...

for %%F in ("C:\Program Files\Exiftool\exiftool.exe") do (
   if exist %%F copy "%%F" "%root%\Tools-Binaries\exiftool\" >nul
)

if exist "C:\ProgramData\chocolatey\bin\binwalk.exe" (
   copy "C:\ProgramData\chocolatey\bin\binwalk.exe" "%root%\Tools-Binaries\binwalk\" >nul
)

if exist "C:\tools\ruby31\bin\zsteg.bat" (
   copy "C:\tools\ruby31\bin\zsteg.bat" "%root%\Tools-Binaries\zsteg\" >nul
)

if exist "C:\Program Files\hashcat\hashcat.exe" (
   copy "C:\Program Files\hashcat\hashcat.exe" "%root%\Tools-Binaries\hashcat\" >nul
)

if exist "C:\Program Files\John\run\john.exe" (
   copy "C:\Program Files\John\run\john.exe" "%root%\Tools-Binaries\john\" >nul
)

copy "C:\Program Files\GnuWin32\bin\*.exe" "%root%\Tools-Binaries\utilities\" >nul
copy "C:\Program Files (x86)\Nmap\ncat.exe" "%root%\Tools-Binaries\utilities\" >nul
copy "C:\Windows\System32\curl.exe" "%root%\Tools-Binaries\utilities\" >nul

if exist "C:\Program Files\ghidra\ghidraRun.bat" (
   copy "C:\Program Files\ghidra\ghidraRun.bat" "%root%\Tools-Binaries\ghidra\" >nul
)

if exist "C:\ProgramData\chocolatey\bin\radare2.exe" (
   copy "C:\ProgramData\chocolatey\bin\radare2.exe" "%root%\Tools-Binaries\radare2\" >nul
)

if exist "C:\Program Files\Wireshark\Wireshark.exe" (
   copy "C:\Program Files\Wireshark\Wireshark.exe" "%root%\Tools-Binaries\wireshark\" >nul
)

(
   echo [InternetShortcut]
   echo URL=https://portswigger.net/burp/communitydownload
) > "%root%\01-Web\BurpSuite\BurpSuiteCommunity.url"

(
   echo [InternetShortcut]
   echo URL=https://gchq.github.io/CyberChef/
) > "%root%\01-Web\CyberChef\CyberChef.url"
goto :eof
