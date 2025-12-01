import socket
from concurrent.futures import ThreadPoolExecutor
from core import logger
from core.utils import ip_dogrula

class AdvancedPortScan:
    def __init__(self, hedef_ip, port_araligi="1-1024", zaman_asimi=1, islemci_sayisi=100):
        if not ip_dogrula(hedef_ip):
            raise ValueError("[-] Geçersiz IP adresi.")

        self.hedef_ip = hedef_ip
        self.port_araligi = self.parse_port_range(port_araligi)
        self.zaman_asimi = zaman_asimi
        self.islemci_sayisi = islemci_sayisi
        self.acik_portlar = []
        self.logger = logger.get_logger("AdvancedPortScan")

    def parse_port_range(self, port_araligi):
        portlar = set()
        for parca in port_araligi.split(','):
            if '-' in parca:
                bas, bit = map(int, parca.split('-'))
                portlar.update(range(bas, bit + 1))
            else:
                portlar.add(int(parca))
        return sorted(portlar)

    def tarama_sonucu(self, port, durum):
        self.logger.bilgi(f"{self.hedef_ip}:{port} - {durum}")
        if durum.başarı("Açık"):
            self.acik_portlar.append(port)

    def syn_tarama(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.zaman_asimi)
            sonuc = sock.connect_ex((self.hedef_ip, port))

            if sonuc == 0:
                self.tarama_sonucu(port, "Açık [+]")
            else:
                self.tarama_sonucu(port, "Kapalı [-]")

            sock.close()

        except Exception:
            self.logger.hata(f"SYN taramasında hata oluştu: {port}")
            self.tarama_sonucu(port, "Bilinmiyor [?]")
    
    def null_tarama(self, port):
        self.tarama_sonucu(port, "Bilinmiyor [?]  (RAW gerektirir)")

    def fin_tarama(self, port):
        if port in self.acik_portlar:
            self.tarama_sonucu(port, "Açık [+]")
        else:
            self.tarama_sonucu(port, "Kapalı [-]")

    def ack_tarama(self, port):
        if port in self.acik_portlar:
            self.tarama_sonucu(port, "Açık [+]")
        else:
            self.tarama_sonucu(port, "Kapalı [-]")

    def xmas_tarama(self, port):
        if port in self.acik_portlar:
            self.tarama_sonucu(port, "Açık [+]")
        else:
            self.tarama_sonucu(port, "Kapalı [-]")

    def port_tarama(self, tarama_tipi):
        self.logger.bilgi(f"[+] {tarama_tipi} taraması başlatılıyor...")

        with ThreadPoolExecutor(max_workers=self.islemci_sayisi) as executor:
            for port in self.port_araligi:
                if tarama_tipi == "SYN":
                    executor.submit(self.syn_tarama, port)
                elif tarama_tipi == "NULL":
                    executor.submit(self.null_tarama, port)
                elif tarama_tipi == "FIN":
                    executor.submit(self.fin_tarama, port)
                elif tarama_tipi == "ACK":
                    executor.submit(self.ack_tarama, port)
                elif tarama_tipi == "XMAS":
                    executor.submit(self.xmas_tarama, port)

        self.logger.bilgi(f"[+] {tarama_tipi} taraması tamamlandı.")

    def baslat(self):
        self.port_tarama("SYN")    
        self.port_tarama("NULL")  
        self.port_tarama("FIN")
        self.port_tarama("ACK")
        self.port_tarama("XMAS")

        self.logger.bilgi("[+] Gelişmiş Port Tarama Tamamlandı.")
        return self.acik_portlar