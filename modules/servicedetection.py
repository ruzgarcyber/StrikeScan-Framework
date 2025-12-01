import socket
from core import logger

class ServiceDetection:

    def __init__(self, target, ports):
        self.target = target
        self.ports = ports
        self.services = {}
        self.log = logger.get_logger("ServiceDetection")

        self.log.bilgi(f"Servis tespiti başlatıldı -> Hedef: {self.target}")

    def algıla(self):
        for port in self.ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)

                sonuc = sock.connect_ex((self.target, port))
                sock.close()

                if sonuc == 0:
                    try:
                        service_name = socket.getservbyport(port)
                    except:
                        service_name = "unknown"

                    self.services[port] = service_name
                    self.log.başarı(f"[AÇIK] {self.target}:{port} -> {service_name}")

                else:
                    self.log.uyarı(f"[KAPALI] {self.target}:{port}")

            except Exception as e:
                self.log.hata(f"Port {port} servis kontrol hatası -> {e}")

        self.log.bilgi("Servis tespiti tamamlandı.")

        return self.services