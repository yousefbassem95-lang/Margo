import hashlib
import os
from colorama import Fore, Style

# SHΔDØW CORE // CRYPTO UTILITY
# PURPOSE: Generate and verify cryptographic hashes.

def generate_hash():
    print(Fore.BLUE + Style.BRIGHT + "\n[+] CRYPTOGRAPHIC HASH GENERATOR" + Style.RESET_ALL)
    print(Fore.BLUE + "[1] TEXT INPUT" + Style.RESET_ALL)
    print(Fore.BLUE + "[2] FILE INPUT" + Style.RESET_ALL)
    
    choice = input(Fore.BLUE + "SELECT SOURCE >> " + Style.RESET_ALL)
    
    data = b""
    if choice == '1':
        text = input(Fore.BLUE + "ENTER TEXT >> " + Style.RESET_ALL)
        data = text.encode()
    elif choice == '2':
        path = input(Fore.BLUE + "ENTER FILE PATH >> " + Style.RESET_ALL)
        try:
            with open(path, "rb") as f:
                data = f.read()
        except Exception as e:
            print(Fore.RED + f"[!] ERROR READING FILE: {e}" + Style.RESET_ALL)
            return
            
    md5_hash = hashlib.md5(data).hexdigest()
    sha1_hash = hashlib.sha1(data).hexdigest()
    sha256_hash = hashlib.sha256(data).hexdigest()
    
    print(Fore.CYAN + "-"*60 + Style.RESET_ALL)
    print(Fore.CYAN + f"MD5:    {md5_hash}" + Style.RESET_ALL)
    print(Fore.CYAN + f"SHA1:   {sha1_hash}" + Style.RESET_ALL)
    print(Fore.CYAN + f"SHA256: {sha256_hash}" + Style.RESET_ALL)
    print(Fore.CYAN + "-"*60 + Style.RESET_ALL)

def main_menu():
    generate_hash()
