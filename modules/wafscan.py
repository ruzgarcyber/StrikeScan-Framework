import requests
from core import logger

WAF_SIGNATURES = {
    "Cloudflare": ["cf-ray", "__cfduid", "cloudflare"],
    "Akamai": ["akamai", "ak_bmsc"],
    "Imperva (Incapsula)": ["incapsula", "visid_incap"],
    "Sucuri": ["sucuri"],
}

GUARD_HEADERS = [
    "X-Frame-Options",
    "X-XSS-Protection",
    "X-Content-Type-Options",
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "Referrer-Policy",
]


def waf_tespit(headers, content):
    bulunan = []
    content_lower = content.lower()

    for waf, signatures in WAF_SIGNATURES.items():
        for sig in signatures:
            if sig.lower() in str(headers).lower() or sig.lower() in content_lower:
                bulunan.append(waf)
                break

    return bulunan


def guvenlik_header_kontrol(headers):
    mevcut = []
    eksik = []

    for h in GUARD_HEADERS:
        if h in headers:
            mevcut.append(h)
        else:
            eksik.append(h)

    return mevcut, eksik


def waftarama(url):
    logger.bilgi(f"WAF & Güvenlik Analizi Başladı → {url}")

    try:
        r = requests.get(url, timeout=5)
    except Exception as e:
        logger.hata(f"İstek hatası: {e}")
        return

    headers = r.headers
    content = r.text

    wafler = waf_tespit(headers, content)

    if wafler:
        logger.başarı("WAF bulundu:")
        for w in wafler:
            print(f"   → {w}")
    else:
        logger.uyarı("WAF tespit edilemedi.")

    mevcut, eksik = guvenlik_header_kontrol(headers)

    print("\n=== Güvenlik Headerları ===")

    for h in mevcut:
        print(f"[+] Mevcut: {h}")

    for h in eksik:
        print(f"[-] Eksik: {h}")

    logger.bilgi("Analiz tamamlandı.\n")