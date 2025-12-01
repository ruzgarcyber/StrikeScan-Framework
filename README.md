# 🚀 StrikeScan-Framework

> StrikeScan-Framework is a modular Python scanning framework for offensive security testing.
It’s designed for red teamers, pentesters, and security enthusiasts. Scan networks, detect OS, grab banners, and run custom scripts—all in one powerful tool! 💻🔥

<img width="1622" height="768" alt="StrikeScan" src="https://github.com/user-attachments/assets/461d8f6b-7162-4257-aa19-862016ac7411" />

# ✨ Features
- 🔹 TCP - Scan	Fast and accurate port scanning
- 🔹 Subdomain Enumeration -	Discover subdomains for a domain
- 🔹 Vulnerability Scan -	Scan ports for known weaknesses
- 🔹 Directory Scan (DirScan) -	Brute-force directories using a wordlist
- 🔹 WAF Detection - Detect Web Application Firewall protections
- 🔹 Host Discovery -	Discover hosts using ARP, ICMP, TCP, UDP
- 🔹 Advanced Port Scan -	Multi-threaded scanning over custom port ranges
- 🔹 Service Detection -	Detect services running on open ports
- 🔹 OS Detection -	Identify OS using TTL-based fingerprinting
- 🔹 TTL OS Fingerprinting -	Detect OS by analyzing TTL values directly
- 🔹 Banner Grabbing -	Fetch service banners for recon
- 🔹 Input Mutator -	Mutate input strings for fuzzing & testing
- 🔹 Script Engine -	Dynamically load and run custom scripts

# 🛠 Installation
- 1. git clone https://github.com/ruzgarcyber/StrikeScan-Framework.git
- 2. cd StrikeScan-Framework
- 3. pip install -r requirements.txt

# ⚡ Usage
- Run the main script with the desired module:
> python3 main.py --modul <module> [options]

 **🔹 Module Examples**
- TCP Scan
> python3 main.py --modul tcp --ip 192.168.1.1

- Subdomain Enumeration
> python3 main.py --modul subdomain --domain example.com

- Vulnerability Scan
> python3 main.py --modul vuln --ip 192.168.1.1 --ports 22,80,443

- Directory Scan
> python3 main.py --modul dirscan --target http://example.com --wordlist assets/dirs.txt

- WAF Detection
> python3 main.py --modul waf --url http://example.com

- Host Discovery
> python3 main.py --modul host --ip 192.168.1.1 --protokol ICMP

- Advanced Port Scan
> python3 main.py --modul advport --ip 192.168.1.1 --range 1-1024 --threads 100

- Service Detection
> python3 main.py --modul service --ip 192.168.1.1 --ports 22,80

- OS Detection
> python3 main.py --modul os

- TTL OS Fingerprinting 
> python3 main.py --modul ttl --ip 192.168.1.1

- Banner Grabbing
> python3 main.py --modul banner --ip 192.168.1.1 --port 22

- Input Mutator
> python3 main.py --modul inputmutator --value "admin"

- Script Engine
> python3 main.py --modul script --script example_script --sargs arg1 arg2

# 🤝 Contributing
> **Contributions, bug reports, and feature requests are welcome!
Create an issue or submit a pull request. 🌟**

## Scripts Directory
The `scripts/` folder is currently empty and reserved for future modules and custom scanning scripts that will be added in later releases.

# 📝 License
- MIT License.

# ✨ Author
> **Developed by Rüzgar Umut Gündoğan, an independent offensive security learner & developer, continuously improving skills while building custom security tools and frameworks.**

# 🧪 Tested Environment
- *Tested on:* **Windows 11 (PowerShell)**
