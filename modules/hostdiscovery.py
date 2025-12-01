import socket
import subprocess
from core import logger


PROTOKOL_LİSTESİ = ["Arp", "TCP", "UDP", "ICMP"]


def host_keşifi(ip, protokol):

    if protokol not in PROTOKOL_LİSTESİ:
        logger.hata("Geçersiz yöntem seçildi.")
        return False

    logger.bilgi(f"{protokol} Protokolü ile {ip} üzerinde host keşfi yapılıyor...")

    if protokol == "Arp":
        return arp_tarama(ip)

    elif protokol == "TCP":
        return tcp_tarama(ip)

    elif protokol == "UDP":
        return udp_tarama(ip)

    elif protokol == "ICMP":
        return icmp_tarama(ip)

def arp_tarama(ip):
    try:
        sonuc = subprocess.run(
            ["arping", "-c", "1", "-w", "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if sonuc.returncode == 0:
            logger.başarı(f"{ip} — ARP CEVAP VERDİ (ALIVE)")
            return True
        else:
            logger.uyarı(f"{ip} ARP cevap vermedi.")
            return False

    except Exception as e:
        logger.hata(f"ARP taraması başarısız: {e}")
        return False

def tcp_tarama(ip, port=80):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((ip, port))
        s.close()
        logger.başarı(f"{ip}:{port} — TCP açık (ALIVE)")
        return True
    except:
        logger.uyarı(f"{ip}:{port} — TCP kapalı.")
        return False

def udp_tarama(ip, port=53):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.sendto(b"test", (ip, port))
        s.recvfrom(512)
        logger.başarı(f"{ip}:{port} — UDP cevap verdi (ALIVE)")
        return True
    except:
        logger.uyarı(f"{ip}:{port} — UDP cevap yok.")
        return False

def icmp_tarama(ip):
    try:
        sonuc = subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if sonuc.returncode == 0:
            logger.başarı(f"{ip} — ICMP cevap verdi (ALIVE)")
            return True
        else:
            logger.uyarı(f"{ip} ICMP cevap vermedi.")
            return False

    except Exception as e:
        logger.hata(f"ICMP taraması başarısız: {e}")
        return False
