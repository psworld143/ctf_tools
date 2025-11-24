# CTF Tools Toolkit

A comprehensive toolkit for Capture The Flag (CTF) competitions with intelligent challenge analysis and cross-platform tool installation.

## Features

- 🛠️ **13+ CTF Tools**: ExifTool, Binwalk, zsteg, Hashcat, John the Ripper, Ghidra, radare2, Wireshark, Burp Suite, CyberChef, and more
- 🤖 **Intelligent Challenge Analyzer**: Automatically determines challenge type and recommends tools
- 🖥️ **Cross-Platform Support**: Works on Windows, Linux, and macOS
- 📦 **Auto-Installation**: One-click installation for all CTF tools
- 🔍 **Tool Detection**: Automatically detects installed tools across platforms

## Installation

### Prerequisites

- Python 3.7+
- Git

### Setup

1. Clone the repository:
```bash
git clone https://github.com/psworld143/ctf_tools.git
cd ctf_tools
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the tool selector:
```bash
python3 ctf_tool_selector.py
```

## Building Executables

### Automated Builds (GitHub Actions)

**Windows builds are automatically created** on every push to the main branch using GitHub Actions!

1. **Download Latest Build**: Go to the [Actions](https://github.com/psworld143/ctf_tools/actions) tab
2. Click on the latest workflow run
3. Download the `CTF_Tool_Selector-Windows` artifact

**Builds are triggered on:**
- Every push to `main` branch
- Pull requests
- Tags starting with `v*` (creates releases)
- Manual workflow dispatch

### Manual Build (Local)

#### On Windows:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the build script:
```bash
build_windows.bat
```

Or manually with PyInstaller:
```bash
pyinstaller --onefile --name "CTF_Tool_Selector" --console --add-data "ai_providers.sql;." ctf_tool_selector.py
```

The executable will be created in the `dist` folder as `CTF_Tool_Selector.exe`.

#### On Linux/macOS:

Use the same PyInstaller command but with Linux/macOS path separators:
```bash
pyinstaller --onefile --name "CTF_Tool_Selector" --console --add-data "ai_providers.sql:." ctf_tool_selector.py
```

### Build Options:

- **One-file executable**: Single executable file (larger size, easier distribution)
- **Console mode**: Shows command-line interface
- **Includes data files**: Automatically bundles `ai_providers.sql`

### Distribution:

The generated executables can be distributed to users without requiring Python installation. All dependencies are bundled into the executable.

### Creating Releases:

To create a release with pre-built executables:
1. Create a tag: `git tag v1.0.0`
2. Push the tag: `git push origin v1.0.0`
3. GitHub Actions will automatically build and create a release with Windows, Linux, and macOS executables

## Usage

### Interactive Tool Selector

Run `python3 ctf_tool_selector.py` to access:
- **Tool Menu**: Browse and launch CTF tools
- **Challenge Analyzer**: Analyze files to determine challenge type
- **Tool Installer**: Install all CTF tools automatically

### Windows Installation

For Windows users, you can also use the batch installer:
```bash
CTF_Toolkit_FullInstaller.bat
```

Or use the Python installer (option `I` in the menu).

## Supported Platforms

- **Windows**: Uses winget and Chocolatey
- **Linux**: Supports apt, yum, dnf, and pacman
- **macOS**: Uses Homebrew

## Tools Included

### Forensics & Steganography
- ExifTool - Metadata extraction
- Binwalk - Binary analysis and embedded file extraction
- zsteg - PNG/BMP steganography detection

### Cryptography
- Hashcat - GPU-accelerated hash cracking
- John the Ripper - Password/hash cracking

### Reverse Engineering
- Ghidra - Full-featured reverse engineering suite
- radare2 - Lightweight reversing framework

### Network Analysis
- Wireshark - Packet capture and analysis
- Nmap/ncat - Network utilities

### Web Security
- Burp Suite Community - Web proxy/interceptor
- CyberChef - Data manipulation and encoding

### Utilities
- GNU Coreutils (strings, xxd, base64, etc.)
- curl - HTTP client

## Challenge Analyzer

The intelligent challenge analyzer can:
- Determine challenge category (Forensics, Steganography, Crypto, Reversing, etc.)
- Identify file types and formats
- Recommend appropriate tools
- Suggest initial analysis steps
- Identify potential flag locations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for educational purposes.

## Disclaimer

This toolkit is intended for legitimate CTF competitions and educational purposes only. Users are responsible for ensuring they have proper authorization before using these tools on any system.

