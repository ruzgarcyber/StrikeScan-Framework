#!/usr/bin/env python3
import argparse

from core.tcp import tcp_scan
from modules.subdomain import subdomain_taraması
from modules.vulnscan import tarama as vuln_tarama
from modules.dirscan import calıstır_dirscan
from modules.wafscan import waftarama
from modules.hostdiscovery import host_keşifi
from modules.advancedportscan import AdvancedPortScan
from modules.servicedetection import ServiceDetection
from modules.osdetection import OSDetection
from modules.bannergraber import BannerGrabbing
from modules.inputmutator import InputMutator
from modules.scriptengine import ScriptEngine
from modules.ttlosfingerprint import TTLBasedOSFingerprint   

from core import logger
from core import utils

LOGO_DOSYASI = "assets/logo.txt"


def logo_goster():
    try:
        with open(LOGO_DOSYASI, "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        logger.uyarı("Logo dosyası bulunamadı.")


def main():
    utils.temizle()
    logo_goster()
    logger.bilgi("StrikeScan-Framework başlatılıyor...")

    parser = argparse.ArgumentParser(description="StrikeScan-Framework")

    parser.add_argument("--modul", required=True,
                        help="tcp, subdomain, vuln, dirscan, waf, host, advport, service, os, ttl, banner, inputmutator, script")

    # Ortak parametreler
    parser.add_argument("--ip", help="Hedef IP")
    parser.add_argument("--domain", help="Hedef domain")
    parser.add_argument("--ports", help="Port listesi (örn: 21,22,80)")
    parser.add_argument("--port", type=int, help="Banner için port")
    parser.add_argument("--url", help="Hedef URL")
    parser.add_argument("--target", help="Dirscan hedef URL")
    parser.add_argument("--wordlist", help="Wordlist yolu")
    parser.add_argument("--protokol", help="Host keşfi protokolü: Arp, TCP, UDP, ICMP")
    parser.add_argument("--range", default="1-1024", help="Port aralığı (örn: 1-1000)")
    parser.add_argument("--timeout", type=float, default=1, help="Timeout süresi")
    parser.add_argument("--threads", type=int, default=100, help="Thread sayısı")

    parser.add_argument("--value", help="Input Mutator için değer")

    # Script engine argümanları
    parser.add_argument("--script", help="Çalıştırılacak script dosyası")
    parser.add_argument("--sargs", nargs="*", help="Script argümanları")

    args = parser.parse_args()
    modul = args.modul.lower()

    # ============================================================
    # MODULE SEÇİMLERİ
    # ============================================================

    # ---------------- TCP SCAN ----------------
    if modul == "tcp":
        if not args.ip:
            logger.hata("TCP taraması için --ip gerekli!")
            return
        logger.bilgi(f"TCP taraması: {args.ip}")
        tcp_scan(args.ip)
        logger.başarı("Tamamlandı.")

    # ---------------- SUBDOMAIN ----------------
    elif modul == "subdomain":
        if not args.domain:
            logger.hata("Subdomain için --domain gerekli!")
            return
        logger.bilgi(f"Subdomain: {args.domain}")
        subdomain_taraması(args.domain)
        logger.başarı("Tamamlandı.")

    # ---------------- VULN SCAN ----------------
    elif modul == "vuln":
        if not args.ip or not args.ports:
            logger.hata("Vuln taraması için --ip ve --ports gerekli!")
            return
        try:
            port_list = [int(x.strip()) for x in args.ports.split(",")]
        except:
            logger.hata("Port formatı hatalı!")
            return

        logger.bilgi("Vuln taraması başlıyor...")
        vuln_tarama(args.ip, port_list)
        logger.başarı("Tamamlandı.")

    # ---------------- DIRSCAN ----------------
    elif modul == "dirscan":
        if not args.target or not args.wordlist:
            logger.hata("Dirscan için --target ve --wordlist gerekli!")
            return

        logger.bilgi(f"Dirscan başlıyor: {args.target}")
        results = calıstır_dirscan(args.target, args.wordlist)
        for r in results:
            print(f"[FOUND] {r}")
        logger.başarı("Tamamlandı.")

    # ---------------- WAF DETECTION ----------------
    elif modul == "waf":
        if not args.url:
            logger.hata("WAF analizi için --url gerekli!")
            return
        waftarama(args.url)
        logger.başarı("Tamamlandı.")

    # ---------------- HOST DISCOVERY ----------------
    elif modul == "host":
        if not args.ip or not args.protokol:
            logger.hata("Host keşfi için --ip ve --protokol gerekli!")
            return
        host_keşifi(args.ip, args.protokol)
        logger.başarı("Tamamlandı.")

    # ---------------- ADVANCED PORT SCAN ----------------
    elif modul == "advport":
        if not args.ip:
            logger.hata("Advanced port scan için --ip gerekli!")
            return

        scanner = AdvancedPortScan(
            hedef_ip=args.ip,
            port_araligi=args.range,
            zaman_asimi=args.timeout,
            islemci_sayisi=args.threads
        )

        aciklar = scanner.baslat()
        logger.başarı(f"Açık portlar: {aciklar}")

    # ---------------- SERVICE DETECTION ----------------
    elif modul == "service":
        if not args.ip or not args.ports:
            logger.hata("Service için --ip ve --ports gerekli!")
            return

        try:
            port_list = [int(x.strip()) for x in args.ports.split(",")]
        except:
            logger.hata("Port formatı hatalı!")
            return

        tespitci = ServiceDetection(args.ip, port_list)
        tespitci.algıla()

        for port, service in tespitci.services.items():
            print(f"[{port}] -> {service}")

    # ---------------- OS DETECTION ----------------
    elif modul == "os":
        analiz = OSDetection()
        logger.başarı(f"İşletim Sistemi: {analiz.algıla()}")
        logger.bilgi(f"Versiyon: {analiz.versiyon()}")
        logger.bilgi(f"Destekli mi? {'Evet' if analiz.destekli_mi() else 'Hayır'}")

    # ---------------- TTL OS FINGERPRINTING ----------------
    elif modul == "ttl":
        if not args.ip:
            logger.hata("TTL OS fingerprinting için --ip gerekli!")
            return

        ttl_f = TTLBasedOSFingerprint()
        os_adi = ttl_f.o_tespiti(args.ip)
        logger.başarı(f"[TTL] Tespit edilen OS: {os_adi}")

    # ---------------- BANNER GRAB ----------------
    elif modul == "banner":
        if not args.ip or not args.port:
            logger.hata("Banner grabbing için --ip ve --port gerekli!")
            return

        grabber = BannerGrabbing(args.ip, args.port)
        banner = grabber.yakala()

        if banner:
            logger.başarı(f"[Banner] {banner}")
        else:
            logger.uyarı("Banner alınamadı.")

    # ---------------- INPUT MUTATOR ----------------
    elif modul == "inputmutator":
        if not args.value:
            logger.hata("Input Mutator için --value gerekli!")
            return

        mutator = InputMutator()
        sonuc = mutator.calistir(args.value)
        logger.başarı(f"Mutasyon: {sonuc}")

    # ---------------- SCRIPT ENGINE ----------------
    elif modul == "script":
        if not args.script:
            logger.hata("Script Engine için --script gerekli!")
            return

        engine = ScriptEngine()
        sonuc = engine.calıştır_script(args.script, *(args.sargs or []))

        if sonuc is not None:
            logger.başarı(f"Script çıktısı: {sonuc}")
        else:
            logger.uyarı("Script çıktı vermedi.")

    else:
        logger.hata(f"Bilinmeyen modül: {modul}")

if __name__ == "__main__":
    main()