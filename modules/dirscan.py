import requests
from core import logger
from core.utils import wordlist_oku

def yukle_wordlist(path="assets/dirs.txt"):
    logger.bilgi(f"Wordlist yükleniyor → {path}")
    return wordlist_oku(path)


def tekli_tarama(url, word):
    word = word.strip()
    if not word:
        return None

    target = f"{url.rstrip('/')}/{word}"

    try:
        r = requests.get(target, timeout=5)

        if r.status_code == 200:
            logger.başarı(f"[200] Found → {target}")
            return target

        elif r.status_code in (301, 302):
            logger.bilgi(f"[REDIRECT] {target}")
        elif r.status_code == 403:
            logger.uyarı(f"[403] Forbidden → {target}")
        else:
            logger.bilgi(f"[{r.status_code}] {target}")

    except requests.exceptions.RequestException:
        pass

    return None

def calıstır_dirscan(url, wordlist_path="assets/dirs.txt"):
    logger.bilgi("Directory Scan başlatılıyor...")

    wl = yukle_wordlist(wordlist_path)

    if not wl:
        logger.hata("Wordlist boş veya bulunamadı!")
        return []

    bulundu = []

    for word in wl:
        result = tekli_tarama(url, word)
        if result:
            bulundu.append(result)

    logger.başarı(f"Tarama tamamlandı! Bulunan: {len(bulundu)} adet path.")
    return bulundu