import sys
import time
import os
import subprocess
import random
import configparser

# Check dependencies from requirements.txt
try:
    import colorama
    from colorama import Fore, Back, Style
    import requests
except ImportError:
    print("Missing dependencies. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama", "requests"])
    import colorama
    from colorama import Fore, Back, Style
    import requests

# Import new modules
import sqli_scanner
import traffic_edu
import access_auditor
import crypto_utils
import banner_grabber
import osint_grid
import manipulation_edu
import reporter
import re
import threading
import itertools

colorama.init()

# CONFIGURATION
VERSION = "3.4 [OPTIMIZED]"
AUTHOR = "Youssef Bassem"
PROJECT = "MARGO"

# COLORS (DARKER BLUE THEME)
THEME_COLOR = Fore.BLUE + Style.BRIGHT 
TEXT_COLOR = Fore.BLUE 
ALERT_COLOR = Fore.RED + Style.BRIGHT
RESET = Style.RESET_ALL

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_icon():
    try:
        with open("icon.txt", "r") as f:
            print(THEME_COLOR + f.read() + RESET)
    except FileNotFoundError:
        print(THEME_COLOR + f"[{PROJECT}] ICON NOT FOUND" + RESET)

def slow_print(text, speed=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

# --- VALIDATION UTILS ---
def validate_ip(ip):
    # Regex for IPv4
    pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    if re.match(pattern, ip):
        return True
    return False

def validate_url(url):
    # Basic URL regex
    pattern = r"^(http|https)://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[a-zA-Z0-9._~:/?#[\]@!$&'()*+,;=-]*)?$"
    if re.match(pattern, url):
        return True
    return False

# --- ASYNC UI UTILS ---
class Spinner:
    def __init__(self, message="PROCESSING"):
        self.spinner = itertools.cycle(['-', '/', '|', '\\'])
        self.running = False
        self.message = message
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write(f'\r{THEME_COLOR}[+] {self.message} COMPLETE.          {RESET}\n')
        sys.stdout.flush()

    def _animate(self):
        while self.running:
            sys.stdout.write(f'\r{THEME_COLOR}[*] {self.message}... {next(self.spinner)}{RESET}')
            sys.stdout.flush()
            time.sleep(0.1)

# --- CORE FUNCTIONS ---

def check_cpp_scanner():
    if not os.path.exists("./scanner"):
        slow_print(ALERT_COLOR + "[!] WARNING: C++ SCANNER MODULE NOT COMPILED." + RESET)
        slow_print(TEXT_COLOR + "[*] COMPILING scanner.cpp..." + RESET)
        try:
            subprocess.run(["g++", "scanner.cpp", "-o", "scanner"], check=True)
            slow_print(THEME_COLOR + "[+] COMPILATION SUCCESSFUL. MODULE LINKED." + RESET)
        except Exception as e:
            slow_print(ALERT_COLOR + f"[!] COMPILATION FAILED: {e}" + RESET)
            return False
    return True

def run_port_scan():
    if not check_cpp_scanner():
        return

    target = input(TEXT_COLOR + "ENTER TARGET IP >> " + RESET)
    if not validate_ip(target):
         print(ALERT_COLOR + "[!] INVALID IP ADDRESS FORMAT." + RESET)
         return

    start_port = input(TEXT_COLOR + "START PORT >> " + RESET)
    end_port = input(TEXT_COLOR + "END PORT >> " + RESET)
    
    if not (start_port.isdigit() and end_port.isdigit()):
        print(ALERT_COLOR + "[!] PORTS MUST BE INTEGERS." + RESET)
        return

    print(THEME_COLOR + "\n[+] INITIATING SCAN PROTOCOL..." + RESET)
    
    spinner = Spinner("SCANNING TARGET")
    spinner.start()
    
    try:
        # Capture output for reporting
        result = subprocess.run(
            ["./scanner", target, start_port, end_port], 
            capture_output=True, 
            text=True
        )
        spinner.stop()
        
        print(result.stdout)
        if result.stderr:
            print(ALERT_COLOR + result.stderr + RESET)
            
        # Save to report
        reporter.save_report("PORT_SCAN", target, result.stdout)
        
    except Exception as e:
        spinner.stop()
        print(ALERT_COLOR + f"[!] EXECUTION ERROR: {e}" + RESET)

def analyze_headers():
    url = input(TEXT_COLOR + "ENTER TARGET URL (http/https) >> " + RESET)
    
    if not url.startswith("http"):
         if validate_url("http://" + url):
             url = "http://" + url
         else:
             print(ALERT_COLOR + "[!] INVALID URL FORMAT." + RESET)
             return
    elif not validate_url(url):
         print(ALERT_COLOR + "[!] INVALID URL FORMAT." + RESET)
         return
    
    print(THEME_COLOR + f"\n[+] INTERCEPTING HEADERS FROM {url}..." + RESET)
    
    scan_log = ""
    
    try:
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
            "Margo_Security_Tool/3.4" 
        ]
        headers = {'User-Agent': random.choice(user_agents)}
        
        response = requests.get(url, headers=headers, timeout=5)
        
        status_msg = f"STATUS: {response.status_code}"
        print(TEXT_COLOR + status_msg + RESET)
        scan_log += status_msg + "\n"
        
        security_headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "X-XSS-Protection"
        ]
        
        missing_count = 0
        for header in security_headers:
            if header in response.headers:
                msg = f"[OK] {header}: FOUND"
                print(THEME_COLOR + msg + RESET)
                scan_log += msg + "\n"
            else:
                msg = f"[!] {header}: MISSING (VULNERABILITY DETECTED)"
                print(ALERT_COLOR + msg + RESET)
                scan_log += msg + "\n"
                missing_count += 1
                
        if missing_count == 0:
            msg = "\n[+] TARGET HARDENING: EXCELLENT."
        else:
            msg = f"\n[!] TARGET VULNERABILITY FACTOR: {missing_count} MISSING HEADERS."
        
        print(THEME_COLOR + msg + RESET)
        scan_log += msg + "\n"
        
        reporter.save_report("HEADER_ANALYSIS", url, scan_log)
            
    except Exception as e:
        print(ALERT_COLOR + f"[!] CONNECTION FAILURE: {e}" + RESET)

def banner_grab_wrapper():
    target = input(TEXT_COLOR + "ENTER TARGET IP >> " + RESET)
    if not validate_ip(target):
         print(ALERT_COLOR + "[!] INVALID IP FORMAT." + RESET)
         return
         
    port = input(TEXT_COLOR + "ENTER TARGET PORT >> " + RESET)
    if not port.isdigit():
        print(ALERT_COLOR + "[!] INVALID PORT." + RESET)
        return
        
    # Redirect stdout to capture it? Or just let it print. 
    # For now, banner_grabber prints directly. We can wrap it later for logging.
    # Simple logging implementation:
    print(THEME_COLOR + "[*] EXECUTING BANNER GRAB..." + RESET)
    banner_grabber.grab_banner(target, port)

def main_menu():
    clear_screen()
    load_icon()
    print(TEXT_COLOR + "========================================" + RESET)
    print(TEXT_COLOR + "        MARGO SECURITY ARSENAL          " + RESET)
    print(TEXT_COLOR + "========================================" + RESET)
    print(TEXT_COLOR + "[1] NETWORK RECONNAISSANCE [PORT SCAN]" + RESET)
    print(TEXT_COLOR + "[2] HEADER VULNERABILITY ANALYSIS" + RESET)
    print(TEXT_COLOR + "[3] SQL INJECTION VULNERABILITY SCANNER" + RESET)
    print(TEXT_COLOR + "[4] NETWORK STRESS DEFENSE EDUCATION" + RESET)
    print(TEXT_COLOR + "[5] ACCESS SECURITY AUDITOR (BRUTE FORCE DEFENSE)" + RESET)
    print(TEXT_COLOR + "[6] CRYPTOGRAPHIC HASH UTILITY" + RESET)
    print(TEXT_COLOR + "[7] SERVICE BANNER GRABBER" + RESET)
    print(TEXT_COLOR + "[8] PUBLIC INTELLIGENCE GRID [OSINT]" + RESET)
    print(TEXT_COLOR + "[9] MANIPULATION DEFENSE EDUCATION" + RESET)
    print(TEXT_COLOR + "[10] ACTIVATE SHADOW HACKER MODE [STEALTH]" + RESET)
    print(TEXT_COLOR + "[99] EXIT SYSTEM" + RESET)
    print(TEXT_COLOR + "========================================" + RESET)
    
    choice = input(THEME_COLOR + "COMMAND >> " + RESET)
    
    if choice == '1':
        run_port_scan()
    elif choice == '2':
        analyze_headers()
    elif choice == '3':
        url = input(TEXT_COLOR + "ENTER TARGET URL >> " + RESET)
        if not url.startswith("http"): url = "http://" + url
        sqli_scanner.check_sqli_vulnerability(url)
    elif choice == '4':
        traffic_edu.explain_traffic_stress()
    elif choice == '5':
        access_auditor.audit_password()
    elif choice == '6':
        crypto_utils.generate_hash()
    elif choice == '7':
        banner_grab_wrapper()
    elif choice == '8':
        osint_grid.run_osint_grid()
    elif choice == '9':
        manipulation_edu.explain_manipulation_defense()
    elif choice == '10':
        print(THEME_COLOR + "\n[*] INVISIBILITY LAYER ENABLED." + RESET)
        print(TEXT_COLOR + "    - PROXY CHAINING: [OFF/EDUCATIONAL]" + RESET)
        print(TEXT_COLOR + "    - AGENT ROTATION: [ACTIVE]" + RESET)
    elif choice == '99':
        print(THEME_COLOR + "\n[!] SESSION TERMINATED." + RESET)
        sys.exit()
    else:
        print(ALERT_COLOR + "[!] UNKNOWN COMMAND" + RESET)
    
    input(TEXT_COLOR + "\nPRESS ENTER TO CONTINUE..." + RESET)
    main_menu()

if __name__ == "__main__":
    slow_print(THEME_COLOR + "INITIALIZING MARGO..." + RESET)
    time.sleep(1)
    main_menu()
