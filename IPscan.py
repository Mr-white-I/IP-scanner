import socket
import threading
import os
import platform
import random
import time
import pyfiglet
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# Display Hacker-Style Banner
def display_banner():
    banner = pyfiglet.figlet_format("I P  S c a n n e r", font="slant")
    print(Fore.GREEn + banner)
    print(Fore.YELLOW + "[+] @Mahesh | Powered by ChatGPT\n")

# Function to check if the host is up using ping (handles Windows and Linux)
def is_host_up(target):
    param = "-n 1" if platform.system().lower() == "windows" else "-c 1"
    response = os.system(
        f"ping {param} {target} > nul 2>&1" if platform.system().lower() == "windows" else f"ping {param} {target} > /dev/null 2>&1")
    return response == 0

# Function to grab banners for system info
def grab_banner(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((target, port))
        banner = s.recv(1024).decode().strip()
        s.close()
        return banner
    except:
        return None

# Function to perform a stealthy scan with randomized timing and retries
def stealthy_scan_port(target, port, open_ports, closed_ports, filtered_ports, banners):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        # Random delay to avoid detection
        time.sleep(random.uniform(0.5, 2.5))

        result = s.connect_ex((target, port))
        if result == 0:
            print(Fore.GREEN + f"[+] Port {port} is open")
            open_ports.append(port)
            banner = grab_banner(target, port)
            if banner:
                banners[port] = banner
        elif result in [111, 113, 10060]:  # Handle filtered/timeout responses
            filtered_ports.append(port)
    except:
        closed_ports.append(port)

# Main function to control the scanner
def port_scanner(target, ports):
    print(Fore.CYAN + f"Scanning target: {target}...\n")

    if not is_host_up(target):
        print(Fore.RED + "[-] Host is down or unreachable\n")
        return
    else:
        print(Fore.GREEN + "[+] Host is up\n")

    open_ports = []
    closed_ports = []
    filtered_ports = []
    banners = {}

    threads = []
    for port in ports:
        thread = threading.Thread(target=stealthy_scan_port,
                                  args=(target, port, open_ports, closed_ports, filtered_ports, banners))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(Fore.CYAN + "\nScan complete!")
    print(Fore.GREEN + f"Open ports: {len(open_ports)}" if open_ports else Fore.YELLOW + "No open ports found")
    print(Fore.RED + f"Closed ports: {len(closed_ports)}" if closed_ports else Fore.YELLOW + "No closed ports found")
    print(Fore.MAGENTA + f"Filtered ports: {len(filtered_ports)}" if filtered_ports else Fore.YELLOW + "No filtered ports found")

    if banners:
        print(Fore.YELLOW + "\nBanners grabbed:")
        for port, banner in banners.items():
            print(Fore.YELLOW + f"Port {port}: {banner}")

# Entry point
if __name__ == "__main__":
    os.system("cls" if platform.system() == "Windows" else "clear")
    display_banner()

    target = input(Fore.CYAN + "Enter target IP or domain: ")
    start_port = int(input(Fore.CYAN + "Enter start port: "))
    end_port = int(input(Fore.CYAN + "Enter end port: "))

    ports = range(start_port, end_port + 1)
    port_scanner(target, ports)
