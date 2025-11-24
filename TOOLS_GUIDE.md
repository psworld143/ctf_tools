# CTF Tools Quick Guide

The following tools are referenced by the provided Windows installation script
(`CTF_Toolkit_FullInstaller.bat`). Use this guide as a quick refresher once
everything is installed via winget/chocolatey.

> **Note:** Run `CTF_Toolkit_FullInstaller.bat` for full setup (folders + tools),
> or `CTF_Toolkit_FullInstaller.bat install-only` to install tools without
> creating the folder structure.

> Tip: Run `python ctf_tool_selector.py` for an interactive menu that shows the
> same info and lets you launch the tools directly.

---

## ExifTool (`exiftool`)

- **Purpose:** Inspect and edit metadata in almost any multimedia file.
- **Check install:** `exiftool -ver`
- **Common use cases:**
  - Dump everything: `exiftool target.jpg`
  - Show duplicate/hidden tags: `exiftool -a -G1 -s image.png`
  - Remove metadata: `exiftool -all= file.png`

## Binwalk (`binwalk`)

- **Purpose:** Firmware/binary analysis for embedded files, signatures, and
  compression.
- **Check install:** `binwalk -h`
- **Common use cases:**
  - Quick scan: `binwalk firmware.bin`
  - Extract embedded objects: `binwalk -e firmware.bin`
  - Recursive entropy check: `binwalk -E -M dump.img`

## zsteg (`zsteg`)

- **Purpose:** Detect LSB steganography in PNG/BMP images.
- **Check install:** `zsteg -h`
- **Common use cases:**
  - Auto brute-force: `zsteg -a secret.png`
  - Specific channel: `zsteg -E b1,rgb,lsb payload.bmp`
  - Export payload: `zsteg -E b1,bgr,msb file.png > out.bin`

## Hashcat (`hashcat`)

- **Purpose:** GPU-based password cracking for numerous hash formats.
- **Check install:** `hashcat -I`
- **Common use cases:**
  - Straight attack: `hashcat -m 0 hashes.txt rockyou.txt`
  - NTLM: `hashcat -m 1000 ntlm.txt -a 0 rockyou.txt`
  - Restore session: `hashcat --restore`

## John the Ripper (`john`)

- **Purpose:** CPU password cracker with rule-based attacks.
- **Check install:** `john --test`
- **Common use cases:**
  - Default wordlist: `john hashes.txt`
  - Custom wordlist: `john --wordlist=rockyou.txt hashes.txt`
  - Show cracked passwords: `john --show hashes.txt`

## GNU Coreutils (`strings`, `xxd`, `base64`, etc.)

- **Purpose:** Classic Unix utilities compiled for Windows.
- **Check install:** `strings --version`
- **Common use cases:**
  - Show readable strings: `strings -n 6 binary.bin`
  - Hex dump: `xxd file.bin | head`
  - Decode base64: `base64 -d payload.b64 > out.bin`

## ncat (`ncat`)

- **Purpose:** Flexible netcat implementation shipped with Nmap.
- **Check install:** `ncat -h`
- **Common use cases:**
  - Listener: `ncat -lvnp 9001`
  - Reverse shell recipient: `ncat -lvnp 4444`
  - TLS client: `ncat --ssl target 443`

## curl (`curl`)

- **Purpose:** Command-line data transfer and HTTP client.
- **Check install:** `curl --version`
- **Common use cases:**
  - GET request: `curl https://target`
  - Fetch headers: `curl -I https://target`
  - Save response: `curl -o dump.bin https://host/file.bin`

## Ghidra (`ghidraRun`)

- **Purpose:** Full-featured reverse-engineering suite with GUI.
- **Check install:** `ghidraRun -help`
- **Common use cases:**
  - Start GUI: `ghidraRun`
  - Open specific project: `ghidraRun MyGhidraProject`
  - Headless analysis: `analyzeHeadless <proj> <script...>`

## radare2 (`radare2`)

- **Purpose:** CLI-first reversing framework for analysis and debugging.
- **Check install:** `radare2 -v`
- **Common use cases:**
  - Analyze binary: `radare2 binary.bin`
  - Auto-analyze & show main: `radare2 -qc "aaa; s main; pdf" binary`
  - Debug: `radare2 -d ./program`

## Wireshark (`wireshark`, `tshark`)

- **Purpose:** Packet capture/inspection GUI with CLI companion `tshark`.
- **Check install:** `wireshark -v`
- **Common use cases:**
  - Launch GUI: `wireshark`
  - Open capture: `wireshark -r traffic.pcapng`
  - CLI filter: `tshark -r capture.pcap -Y "http"`

## Burp Suite Community (`burpsuite`/`burpsuitecommunity`)

- **Purpose:** Intercepting proxy for web testing (Community edition).
- **Check install:** `burpsuite --version` (if available)
- **Common use cases:**
  - Start GUI: `burpsuite` or `burpsuitecommunity`
  - Windows shortcut: `start burpsuite`
  - Configure browser to use `127.0.0.1:8080` proxy

## CyberChef (`cyberchef`)

- **Purpose:** All-in-one data/crypto tool; also available in-browser.
- **Check install:** `cyberchef --version` (desktop app)
- **Common use cases:**
  - Launch Electron app: `cyberchef`
  - Open web version: `python -m webbrowser https://gchq.github.io/CyberChef/`
  - Import/Export recipes via GUI

