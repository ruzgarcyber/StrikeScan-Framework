import socket
from core import logger

class BannerGrabbing:
    def __init__(self, target: str, port: int):
        self.target = target
        self.port = port
        self.logger = logger.get_logger("BannerGrabbing")

    def yakala(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)

            self.logger.bilgi(f"Bağlanılıyor: {self.target}:{self.port}")
            sock.connect((self.target, self.port))

            sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")

            banner = sock.recv(2048).decode("utf-8", errors="ignore")
            sock.close()

            if banner.strip():
                self.logger.başarı("Banner başarıyla yakalandı!")
                return banner
            
            return None

        except Exception as e:
            self.logger.hata(f"Banner grabbing hatası: {e}")
            return None

    def calistir(self):
        self.logger.bilgi(f"Banner grabbing başlatılıyor: {self.target}:{self.port}")
        banner = self.yakala()

        if banner:
            print("\n===== YAKALANAN BANNER =====")
            print(banner)
            print("============================\n")
        else:
            self.logger.uyarı("Banner yakalanamadı.")