# Guba-Master-Defence

**Modern Defensive Security Toolkit · 2027 Edition**

A clean, professional terminal-based defensive security tool for analyzing suspicious links, APKs, files, and hashes.  
Built for **Termux**, Linux, and macOS. **Defense only** — no offensive capabilities.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux%20%7C%20macOS-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Status](https://img.shields.io/badge/Status-Defense%20Only-red?style=flat-square)

---

## Features

| Module | Description |
|--------|-------------|
| **URL Threat Scanner** | Local heuristics + header analysis + VirusTotal |
| **File / APK Analysis** | Hashing, structure inspection, suspicious string search, VT |
| **Hash Lookup** | Instant reputation check via VirusTotal |
| **Permissions Guide** | Critical Android permissions explained |
| **Network Health** | Quick connectivity & DNS check |
| **Defense Assistant** | Lightweight local helper |
| **Secure Login** | Username + password protection |
| **History & Logs** | Tracks recent scans |

---

## Requirements

- Python **3.8+**
- Internet connection (for VirusTotal and live checks)
- Optional: free [VirusTotal API key](https://www.virustotal.com/gui/my-apikey)

No external packages required (uses only the Python standard library).

---

## Installation

### Termux
```bash
pkg update && pkg install python git
git clone https://github.com/YOUR_USERNAME/Guba-Master-Defence.git
cd Guba-Master-Defence
python guba.py
```

### Linux / macOS
```bash
git clone https://github.com/YOUR_USERNAME/Guba-Master-Defence.git
cd Guba-Master-Defence
python3 guba.py
```

---

## Default Login

```
Username : admin
Password : guba2027
```

Change them immediately from **Settings → Change Credentials**.

---

## VirusTotal Setup

1. Create a free account at [virustotal.com](https://www.virustotal.com)
2. Copy your API key from the profile page
3. Inside the tool → **[7] Settings** → paste the key

---

## Project Structure

```
Guba-Master-Defence/
├── guba.py          # Main application
├── README.md
├── LICENSE
├── .gitignore
└── requirements.txt # Empty (stdlib only)
```

---

## Disclaimer

This tool is intended **strictly for defensive and educational purposes**.  
The author is not responsible for any misuse.

---

## License

MIT License · See [LICENSE](LICENSE)
