import os
import re
import time

def ip_dogrula(ip):
    pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    if not re.match(pattern, ip):
        return False
    return all(0 <= int(part) <= 255 for part in ip.split("."))

def wordlist_oku(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Wordlist bulunamadı: {path}")

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip() for line in f if line.strip()]

def temizle():
    os.system('cls' if os.name == 'nt' else 'clear')

class Timer:
    def __init__(self):
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if self.start_time:
            return round(time.time() - self.start_time, 2)
        return 0