import datetime

class Renkler:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    WHITE = "\033[37m"

LOG_DOSYASI = "strikescan.log"

def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S")

def log_yaz(seviye, mesaj):
    with open(LOG_DOSYASI, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp()}] [{seviye}] {mesaj}\n")

def bilgi(msg):
    print(f"{Renkler.BLUE}[BİLGİ]{Renkler.RESET} {msg}")
    log_yaz("BİLGİ", msg)

def başarı(msg):
    print(f"{Renkler.GREEN}[BAŞARI]{Renkler.RESET} {msg}")
    log_yaz("BAŞARI", msg)

def uyarı(msg):
    print(f"{Renkler.YELLOW}[UYARI]{Renkler.RESET} {msg}")
    log_yaz("UYARI", msg)

def hata(msg):
    print(f"{Renkler.RED}[HATA]{Renkler.RESET} {msg}")
    log_yaz("HATA", msg)

def get_logger(name):
    class LoggerWrapper:
        def bilgi(self, msg):
            bilgi(f"[{name}] {msg}")
        def başarı(self, msg):
            başarı(f"[{name}] {msg}")
        def uyarı(self, msg):
            uyarı(f"[{name}] {msg}")
        def hata(self, msg):
            hata(f"[{name}] {msg}")
    return LoggerWrapper()