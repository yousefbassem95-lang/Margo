import socket
from colorama import Fore, Style

# SHΔDØW CORE // SERVICE BANNER GRABBER
# PURPOSE: Identify running service versions on open ports.
# TACTICAL USE: Reconnaissance for vulnerability assessment (e.g., outdated SSH).

def grab_banner(target, port):
    print(Fore.BLUE + Style.BRIGHT + f"\n[+] INITIATING BANNER GRAB ON {target}:{port}..." + Style.RESET_ALL)
    
    try:
        # Create a socket connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3) # Short timeout to avoid hanging
        
        # Connect
        s.connect((target, int(port)))
        
        # Send a dummy byte to trigger a response (often needed for some services)
        # Note: Some services send a banner immediately on connect (SSH, SMTP), others wait for input.
        try:
             s.send(b'HEAD / HTTP/1.0\r\n\r\n')
        except:
             pass

        # Receive data
        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        
        s.close()
        
        if banner:
            print(Fore.CYAN + "-"*50 + Style.RESET_ALL)
            print(Fore.GREEN + Style.BRIGHT + f"[!] BANNER CAPTURED:\n{banner}" + Style.RESET_ALL)
            print(Fore.CYAN + "-"*50 + Style.RESET_ALL)
            print(Fore.BLUE + "[INFO] Search this version in CVE databases for specific vulnerabilities." + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "[!] CONNECTION ESTABLISHED, BUT NO BANNER RECEIVED." + Style.RESET_ALL)

    except socket.timeout:
        print(Fore.RED + "[!] CONNECTION TIMED OUT." + Style.RESET_ALL)
    except ConnectionRefusedError:
        print(Fore.RED + "[!] CONNECTION REFUSED (PORT CLOSED)." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[!] ERROR: {e}" + Style.RESET_ALL)
