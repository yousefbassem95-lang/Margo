import requests
import sys
from colorama import Fore, Style

# SHΔDØW CORE // SQLi DEFENSE MODULE
# PURPOSE: Identify potential SQL injection points for remediation.
# NOT FOR OFFENSIVE USE.

def check_sqli_vulnerability(url):
    print(Fore.BLUE + Style.BRIGHT + f"\n[+] INITIATING SQL INJECTION VULNERABILITY SCAN ON {url}..." + Style.RESET_ALL)
    
    # Common error-based SQLi payloads (Educational)
    # These are designed to trigger database errors, not to extract data.
    payloads = ["'", "\"", "1' OR '1'='1", "1\" OR \"1\"=\"1"]
    
    vulnerable = False
    
    try:
        # 1. Base Request
        original_response = requests.get(url, timeout=5)
        
        for payload in payloads:
            # Test query parameter injection (concept)
            # In a real tool, we'd parse specific params. Here we append to URL for demonstration.
            test_url = f"{url}{payload}"
            
            print(Fore.CYAN + f"[*] TESTING PAYLOAD: {payload}" + Style.RESET_ALL)
            response = requests.get(test_url, timeout=5)
            
            # Simple error detection (Text matching)
            # This is a basic educational example of how scanners detect issues.
            db_errors = [
                "SQL syntax",
                "mysql_fetch_array",
                "ORA-01756",
                "SQLite3::SQLException"
            ]
            
            for error in db_errors:
                if error in response.text:
                    print(Fore.RED + Style.BRIGHT + f"[!] VULNERABILITY DETECTED! Database Error found with payload: {payload}" + Style.RESET_ALL)
                    print(Fore.RED + f"    Error Snippet: {error}" + Style.RESET_ALL)
                    vulnerable = True
                    break
            
            if vulnerable:
                break
                
        if not vulnerable:
            print(Fore.BLUE + Style.BRIGHT + "[+] NO OBVIOUS SQL ERRORS DETECTED (Target appears hardened against basic error-based injection)." + Style.RESET_ALL)
        else:
            print(Fore.RED + "\n[!] RECOMMENDATION: Sanitize all inputs using Prepared Statements (Parameterized Queries)." + Style.RESET_ALL)

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[!] CONNECTION ERROR: {e}" + Style.RESET_ALL)
