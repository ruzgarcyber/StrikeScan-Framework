import socket

PORTLAR = [22, 80, 443, 21, 25, 23, 20]

def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    try:
        s.connect((ip, port))
        return True
    except:
        return False
    finally:
        s.close()

def tcp_scan(ip):
    print("Taranacak portlar:", PORTLAR)
    for port in PORTLAR:
        if scan_port(ip, port):
            print(f"[+] {port} OPEN")
        else:
            print(f"[-] {port} CLOSED")