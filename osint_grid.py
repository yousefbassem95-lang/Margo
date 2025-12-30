import socket
import requests
from colorama import Fore, Style

# SHΔDØW CORE // PUBLIC INTELLIGENCE GRID
# PURPOSE: Gather public infrastructure intelligence via DNS and basic reconnaissance.
# LEGAL MAPPING of public assets.

def dns_interrogation(target_domain):
    print(Fore.BLUE + Style.BRIGHT + f"\n[+] INITIATING DNS INTERROGATION ON {target_domain}..." + Style.RESET_ALL)
    
    # 1. A Record (IPv4)
    try:
        ip = socket.gethostbyname(target_domain)
        print(Fore.CYAN + f"[*] A RECORD (IPv4): {ip}" + Style.RESET_ALL)
    except socket.gaierror:
        print(Fore.RED + "[!] A RECORD: NOT FOUND" + Style.RESET_ALL)

    # 2. MX Records (Mail Servers) - Simplified via DNS query simulation or basic lookup
    # Python socket doesn't do full DNS type lookups easily without 'dnspython'. 
    # We will simulate the "Grid" effect or use what's available in standard lib/system.
    
    print(Fore.CYAN + f"[*] EXTENDED RECORD SEARCH: [active]" + Style.RESET_ALL)
    try:
        # Get address info usually returns multiple records if they exist
        addr_info = socket.getaddrinfo(target_domain, 80)
        seen_ips = set()
        for res in addr_info:
            ip_addr = res[4][0]
            if ip_addr not in seen_ips:
                print(Fore.GREEN + f"    > INFRASTRUCTURE NODE: {ip_addr}" + Style.RESET_ALL)
                seen_ips.add(ip_addr)
    except Exception as e:
        print(Fore.RED + f"[!] ERROR MAPPING NODES: {e}" + Style.RESET_ALL)

def run_osint_grid():
    target = input(Fore.BLUE + "ENTER TARGET DOMAIN (e.g. example.com) >> " + Style.RESET_ALL)
    if "://" in target:
        target = target.split("://")[1].split("/")[0]
    
    dns_interrogation(target)
    
    print(Fore.BLUE + "\n[+] INTELLIGENCE GRID MAPPING COMPLETE." + Style.RESET_ALL)
