# SHΔDØW MØDE V99 // PROJECT MARGO

![Margo Icon](icon.txt)

> [!WARNING]
> **LEGAL DISCLAIMER**: This tool is designed for **EDUCATIONAL AND DEFENSIVE PURPOSES ONLY**.
> The author (Youssef Bassem) and the creators of this software take NO responsibility for misuse.
> It is illegal to scan, attack, or analyze systems you do not own or have explicit permission to test.
> By downloading or using this tool, you agree to these terms.

## OVERVIEW
Margo is a high-performance Security Assessment Toolkit designed with a "Shadow Core" aesthetic. It combines the ease of Python with the raw speed of C++ for network reconnaissance.

### FEATURES
- **Hybrid Core**: Python CLI + C++ Scanning Engine.
- **Vulnerability Analysis**: Detects missing security headers & SQLi flaws.
- **Access Security**: Password strength auditor to prevent brute force.
- **Crypto Engine**: Hashing utility (MD5, SHA256) for file integrity.
- **Service Enumeration**: Banner Grabber for identifying running services.
- **Intelligence Grid**: OSINT module for DNS/Infrastructure mapping.
- **Stealth Simulation**: Random User-Agent rotation and header spoofing logic.
- **Shadow UI**: Custom Dark Blue terminal theme.

## INSTALLATION & SETUP

### 1. Requirements
- Python 3.x
- G++ Compiler (for the scanner module)
- Linux/Mac Environment (recommended)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Compilation
The tool automatically attempts to compile the C++ scanner on first run. To compile manually:
```bash
g++ scanner.cpp -o scanner
```

## USAGE
Launch the Shadow Console:
```bash
python3 margo.py
```

### COMMANDS
1. **RECONNAISSANCE**: Enter Target IP and Port Range to identify open services.
2. **VULNERABILITY ANALYSIS**: Enter a URL to scan for HTTP security weaknesses.
3. **SQL INJECTION**: Scan URLs for error-based SQL vulnerabilities (Defensive).
4. **TRAFFIC DEFENSE**: Learn about DoS protection mechanisms.
5. **ACCESS AUDITOR**: Test password entropy and estimated crack time.
6. **CRYPTO HASHING**: Generate hashes for text or files.
7. **BANNER GRABBER**: Identify service versions on open ports.
8. **OSINT GRID**: Map public DNS and Infrastructure.
9. **DEFENSE EDU**: Learn about Search/Social manipulation detection.
10. **SHADOW MODE**: Activate stealth protocols (simulation).

---
**STATUS**: SHΔDØW_ACTIVE
**VERSION**: V99
**CORE**: ONLINE
