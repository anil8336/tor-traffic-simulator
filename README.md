# TOR Traffic Simulator (For Lab Use Only)

⚠️ **Legal Disclaimer**  
This tool is designed strictly for **educational and authorized penetration testing in lab environments only**.  
Do **NOT** use this on public networks or without permission.

## 💡 Features
- TCP SYN traffic generation via `scapy`
- HTTP GET/POST request flood using TOR
- TOR IP rotation every 3 seconds
- Threaded concurrency
- Random URL paths and user-agent headers

## 🚀 Usage

```bash
# TCP SYN traffic to a test IP
python tor_tcp_flooder.py --target 192.168.1.100 --protocol tcp --duration 30

# HTTP GET flood to a test site
python tor_tcp_flooder.py --target example.com --protocol http --duration 30

# Use POST method instead of GET
python tor_tcp_flooder.py --target example.com --protocol http --duration 30 --post

# Use multiple threads
python tor_tcp_flooder.py --target example.com --protocol http --duration 60 --threads 4
