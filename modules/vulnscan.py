import socket
import json
import re
import threading
from concurrent.futures import ThreadPoolExecutor

from core import logger
from core.utils import ip_dogrula

def signatures_yukle(path="signatures.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            signatures = json.load(f)
            logger.bilgi(f"{len(signatures)} signature yüklendi.")
            return signatures
    except Exception as e:
        logger.hata(f"signatures.json yüklenemedi: {e}")
        return {}

SIGNATURES = signatures_yukle()

def banner_grab(ip, port, timeout=1):
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((ip, port))
        banner = s.recv(2048).decode(errors="ignore")
        s.close()
        return banner.strip()
    except:
        return None

def http_probe(ip, port, timeout=1.2):
    try:
        s = socket.create_connection((ip, port), timeout=timeout)
        req = b"GET / HTTP/1.1\r\nHost: %b\r\nUser-Agent: VulnScan\r\n\r\n" % ip.encode()
        s.send(req)
        data = s.recv(2048).decode(errors="ignore")
        s.close()
        return data.strip()
    except:
        return None

def signature_kontrol(data):
    if not data:
        return None

    for sig in SIGNATURES:
        pattern = SIGNATURES[sig]["pattern"]
        vuln = SIGNATURES[sig]["vulnerability"]

        if re.search(pattern, data, re.IGNORECASE):
            return vuln

    return None

def port_acik_mi(ip, port, timeout=0.8):
    try:
        s = socket.create_connection((ip, port), timeout=timeout)
        s.close()
        return True
    except:
        return False

def port_tara(ip, port):
    if not port_acik_mi(ip, port):
        return

    banner = banner_grab(ip, port)
    http_data = None

    if port in [80, 443, 8080, 8443, 8000]:
        http_data = http_probe(ip, port)

    combined_data = ""
    if banner:
        combined_data += banner + "\n"
    if http_data:
        combined_data += http_data

    if not combined_data:
        logger.bilgi(f"[{ip}:{port}] Açık fakat banner yok.")
        return

    vuln = signature_kontrol(combined_data)

    if vuln:
        logger.başarı(f"[{ip}:{port}] Zafiyet Tespit Edildi → {vuln}")
    else:
        logger.bilgi(f"[{ip}:{port}] Güvenli — Servis: {banner[:60] if banner else 'N/A'}")

def tarama(ip, port_list, threads=80):
    if not ip_dogrula(ip):
        logger.hata("IP formatı geçersiz.")
        return

    logger.bilgi(f"{ip} hedefinde {len(port_list)} port taranıyor...")
    logger.bilgi(f"Kullanılan thread: {threads}")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for port in port_list:
            executor.submit(port_tara, ip, port)

    logger.başarı("Vulnscan taraması tamamlandı.")