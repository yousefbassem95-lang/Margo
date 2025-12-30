import math
from colorama import Fore, Style
import string

# SHΔDØW CORE // ACCESS AUDITOR
# PURPOSE: Analyze password complexity and estimate entropy.
# EDUCATIONAL DEFENSE against Brute Force.

def calculate_entropy(password):
    pool_size = 0
    if any(c.islower() for c in password): pool_size += 26
    if any(c.isupper() for c in password): pool_size += 26
    if any(c.isdigit() for c in password): pool_size += 10
    if any(c in string.punctuation for c in password): pool_size += 32
    
    if pool_size == 0 or len(password) == 0:
        return 0
        
    entropy = len(password) * math.log2(pool_size)
    return entropy

def estimate_crack_time(entropy):
    # Assumption: Attacker can try 10 billion guesses per second (High-end GPU rig)
    guesses_per_sec = 10_000_000_000
    combinations = 2 ** entropy
    seconds = combinations / guesses_per_sec
    
    if seconds < 60: return f"{seconds:.4f} seconds"
    if seconds < 3600: return f"{seconds/60:.2f} minutes"
    if seconds < 86400: return f"{seconds/3600:.2f} hours"
    if seconds < 31536000: return f"{seconds/86400:.2f} days"
    return f"{seconds/31536000:.2f} years"

def audit_password():
    print(Fore.BLUE + Style.BRIGHT + "\n[+] ACCESS SECURITY AUDITOR (BRUTE FORCE DEFENSE)" + Style.RESET_ALL)
    password = input(Fore.BLUE + "ENTER PASSWORD TO AUDIT >> " + Style.RESET_ALL)
    
    if not password:
        print(Fore.RED + "[!] Input empty." + Style.RESET_ALL)
        return

    entropy = calculate_entropy(password)
    time_to_crack = estimate_crack_time(entropy)
    
    print(Fore.CYAN + "-"*40 + Style.RESET_ALL)
    print(Fore.CYAN + f"LENGTH: {len(password)} chars" + Style.RESET_ALL)
    print(Fore.CYAN + f"ENTROPY: {entropy:.2f} bits" + Style.RESET_ALL)
    print(Fore.CYAN + f"EST. CRACK TIME (10B/s): {time_to_crack}" + Style.RESET_ALL)
    print(Fore.CYAN + "-"*40 + Style.RESET_ALL)
    
    if entropy < 40:
        print(Fore.RED + Style.BRIGHT + "[!] STATUS: VERY WEAK (Instant Breach Likely)" + Style.RESET_ALL)
    elif entropy < 60:
        print(Fore.YELLOW + Style.BRIGHT + "[!] STATUS: WEAK (Vulnerable to dedicated GPU attacks)" + Style.RESET_ALL)
    elif entropy < 80:
        print(Fore.BLUE + Style.BRIGHT + "[+] STATUS: MODERATE (Residential Security)" + Style.RESET_ALL)
    else:
        print(Fore.BLUE + Style.BRIGHT + "[+] STATUS: STRONG (High-Grade Encryption Standard)" + Style.RESET_ALL)

    print(Fore.BLUE + "\n[INFO] High entropy increases the cost and time for brute-force attacks." + Style.RESET_ALL)
