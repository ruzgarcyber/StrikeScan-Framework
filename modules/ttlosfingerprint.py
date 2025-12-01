import scapy.all as scapy
from scapy.layers.inet import IP, ICMP
from core import logger

class TTLBasedOSFingerprint:
    def __init__(self):
        self.logger = logger.get_logger("TTLBasedOSFingerprint")
        # OS ve TTL aralıkları
        self.os_ttl_mapping = {
            "Linux": [64, 128],
            "Windows": [128, 255],
            "macOS": [64, 255],
            "FreeBSD": [64, 255]
        }

    def ttl_al(self, hedef_ip):
        paket = IP(dst=hedef_ip)/ICMP()
        cevap = scapy.sr1(paket, timeout=2, verbose=0)
        if cevap:
            return cevap.ttl
        else:
            self.logger.hata(f"{hedef_ip} adresinden TTL değeri alınamadı.")
            logger.hata("[-] TTL değeri alınamadı.")
            return None

    def o_tespiti(self, hedef_ip):
        ttl_degeri = self.ttl_al(hedef_ip)
        if ttl_degeri is None:
            return "Bilinmeyen OS"
        for os_adi, ttl_araliklari in self.os_ttl_mapping.items():
            for ttl_araligi in ttl_araliklari:
                if ttl_degeri <= ttl_araligi:
                    return os_adi
        return "[?] Bilinmeyen İşletim Sistemi."

    def destekli_mi(self, hedef_ip):
        os_adi = self.o_tespiti(hedef_ip)
        return os_adi in self.os_ttl_mapping.keys()