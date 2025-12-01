import requests
from core import logger

def subdomain_taraması(domain, wordlist_path="assets/subdomains.txt"):
    logger.bilgi(f"Subdomain taraması başlatıldı: {domain}")

    try:
        with open(wordlist_path, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logger.hata(f"Wordlist bulunamadı: {wordlist_path}")
        return

    for word in words:
        sub = f"{word}.{domain}"
        url = f"http://{sub}"

        try:
            r = requests.get(url, timeout=2)
            if r.status_code < 400:
                logger.başarı(f"[+] Bulundu: {sub}")
        except:
            pass  

    logger.bilgi("Subdomain taraması tamamlandı.")