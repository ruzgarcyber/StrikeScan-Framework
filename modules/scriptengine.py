# Script Motoru.

import os
import sys
import importlib
import traceback
from core import logger

class ScriptEngine:
    def __init__(self, script_dosyası="scripts"):
        self.script_dosyası = script_dosyası
        self.logger = logger  
        self.scripts = {}
        self.yükle_scriptler()

    def yükle_scriptler(self):
        self.logger.bilgi(f"Scriptler '{self.script_dosyası}' dizininden yükleniyor...")
        if not os.path.isdir(self.script_dosyası):
            self.logger.hata(f"Script dizini bulunamadı: {self.script_dosyası}")
            return

        if self.script_dosyası not in sys.path:
            sys.path.append(self.script_dosyası)

        for dosya in os.listdir(self.script_dosyası):
            if dosya.endswith(".py") and not dosya.startswith("__"):
                modül_adı = dosya[:-3]
                try:
                    modül = importlib.import_module(modül_adı)
                    self.scripts[modül_adı] = modül
                    self.logger.başarı(f"Yüklendi: {modül_adı}")
                except Exception as e:
                    self.logger.hata(f"Script yüklenemedi: {modül_adı} - {e}")
                    traceback.print_exc()

    def çalıştır_script(self, modül_adı, *args, **kwargs):
        if modül_adı not in self.scripts:
            self.logger.uyarı(f"Script bulunamadı: {modül_adı}")
            return None

        modül = self.scripts[modül_adı]
        if hasattr(modül, "çalıştır"):
            try:
                self.logger.bilgi(f"Script çalıştırılıyor: {modül_adı}")
                return modül.çalıştır(*args, **kwargs)
            except Exception as e:
                self.logger.hata(f"Script çalıştırılamadı: {modül_adı} - {e}")
                traceback.print_exc()
                return None
        else:
            self.logger.uyarı(f"Script 'çalıştır' fonksiyonu bulunamadı: {modül_adı}")
            return None
