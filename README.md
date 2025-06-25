# HOIC-Style DoS Tool

A command-line, Tor-integrated DoS testing tool inspired by HOIC. Built for ethical testing in controlled environments.

## ⚠️ Legal Disclaimer
> This tool is intended **strictly for educational and authorized security testing**. Do not use it against any system or network without **explicit written permission**.

## 📦 Features
- HTTP GET flood and TCP connection flood modes
- Multi-threaded execution
- Tor IP rotation every N seconds
- User-agent randomization
- Supports target IP or domain

## 🚀 Usage
```bash
sudo python3 tor_tcp_flooder.py
```
You will be prompted for:
- Target URL/IP
- Attack mode (`HTTP` or `TCP`)
- Port (if `TCP`)
- Thread count
- Tor password
- Tor IP rotation interval (seconds)
- Whether to enable Tor integration

## 💻 Example
```text
Enter target URL or IP: https://testfire.net
Enter mode (HTTP/TCP): HTTP
Enter Tor control password: kalikali
Enter number of threads: 10
Enter Tor IP rotation interval (seconds): 3
Use Tor for IP rotation? (y/n): y
```

## 🧰 Requirements
Install required Python packages:
```bash
pip install -r requirements.txt
```

Install system tools:
```bash
sudo apt update && sudo apt install tor python3-pip
```

Ensure `/etc/tor/torrc` includes:
```
ControlPort 9051
HashedControlPassword <your-hashed-pass>
```
Generate hashed password:
```bash
tor --hash-password yourpassword
```