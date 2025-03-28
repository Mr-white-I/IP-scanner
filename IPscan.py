#!/usr/bin/env python3
import socket
import threading
import os
import platform
import random
import time


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
            print(f"[+] Port {port} is open")
            open_ports.append(port)
            banner = grab_banner(target, port)
            if banner:
                banners[port] = banner
        elif result in [111, 113, 10060]:  # Handle filtered/timeout responses
            filtered_ports.append(port)
        else:
            closed_ports.append(port)
        s.close()
    except Exception as e:
        closed_ports.append(port)


# Main function to control the scanner
def port_scanner(target, ports):
    print(f"Scanning target: {target}")

    # Check if the host is up
    if not is_host_up(target):
        print("[-] Host is down or unreachable")
        return
    else:
        print("[+] Host is up")

    open_ports = []
    closed_ports = []
    filtered_ports = []
    banners = {}

    # Multi-threading for faster scanning
    threads = []
    for port in ports:
        thread = threading.Thread(target=stealthy_scan_port,
                                  args=(target, port, open_ports, closed_ports, filtered_ports, banners))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Display results
    print("\nScan complete!")
    print(f"Open ports: {len(open_ports)}" if open_ports else "No open ports found")
    print(f"Closed ports: {len(closed_ports)}" if closed_ports else "No closed ports found")
    print(f"Filtered ports: {len(filtered_ports)}" if filtered_ports else "No filtered ports found")

    # Display any banners grabbed
    if banners:
        print("\nBanners grabbed:")
        for port, banner in banners.items():
            print(f"Port {port}: {banner}")


# Get user input
target = input("Enter target IP or domain: ")
start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))

ports = range(start_port, end_port + 1)

port_scanner(target, ports)
