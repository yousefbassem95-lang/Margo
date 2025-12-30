import os
import datetime
from colorama import Fore, Style

# SHΔDØW CORE // REPORTING MODULE
# PURPOSE: Save mission intelligence to persistent storage.

REPORT_DIR = "reports"

def ensure_report_dir():
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)

def save_report(module_name, target, data):
    ensure_report_dir()
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{REPORT_DIR}/{module_name}_{timestamp}.txt"
    
    try:
        with open(filename, "w") as f:
            f.write(f"SHΔDØW CORE V3.3 // MISSION REPORT\n")
            f.write(f"========================================\n")
            f.write(f"TIMESTAMP: {timestamp}\n")
            f.write(f"MODULE:    {module_name}\n")
            f.write(f"TARGET:    {target}\n")
            f.write(f"========================================\n\n")
            f.write(data)
            f.write(f"\n========================================\n")
            f.write(f"END OF TRANSMISSION")
            
        print(Fore.GREEN + f"\n[+] INTELLIGENCE SAVED: {filename}" + Style.RESET_ALL)
        return filename
    except Exception as e:
        print(Fore.RED + f"[!] REPORT FAILURE: {e}" + Style.RESET_ALL)
        return None
