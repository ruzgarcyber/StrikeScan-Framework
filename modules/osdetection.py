import platform
from core import logger

DESTEKLENEN_İŞLETİMSİSTEMLERİ = ["Linux", "Windows", "macOS", "FreeBSD"]

class OSDetection:
    def __init__(self):
        self.logger = logger.get_logger("OSDetection")

    def algıla(self):
        os_name = platform.system()

        if os_name == "Linux":
            return "Linux"
        elif os_name == "Windows":
            return "Windows"
        elif os_name == "Darwin":
            return "macOS"
        elif os_name == "FreeBSD":
            return "FreeBSD"
        else:
            self.logger.hata(f"Desteklenmeyen işletim sistemi: {os_name}")
            return "Bilinmeyen OS"

    def versiyon(self):
        os_name = self.algıla()

        if os_name == "Linux":
            return platform.release()
        elif os_name == "Windows":
            return platform.version()
        elif os_name == "macOS":
            return platform.mac_ver()[0]
        elif os_name == "FreeBSD":
            return platform.release()
        else:
            return "Versiyon tespit edilemedi"

    def destekli_mi(self):
        return self.algıla() in DESTEKLENEN_İŞLETİMSİSTEMLERİ