#!/usr/bin/env python3
"""
framework/language_manager.py - Mehrsprachigkeits-System für AI-DNA Charter
Verwaltet Übersetzungen und ermöglicht dynamische Sprachwechsel
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Optional, Any
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class Language(Enum):
    """Unterstützte Sprachen"""
    DE = "de"
    EN = "en"
    ES = "es"
    FR = "fr"
    IT = "it"
    PT = "pt"
    RU = "ru"
    ZH = "zh"
    JA = "ja"
    KO = "ko"
    AR = "ar"
    HI = "hi"

class LanguageManager:
    """Zentraler Manager für Mehrsprachigkeit"""
    
    _instance = None
    
    def __new__(cls):
        """Singleton Pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialisiere Language Manager"""
        if self._initialized:
            return
            
        self.languages_dir = Path(__file__).parent / "languages"
        self.current_language = Language.DE  # Standard: Deutsch
        self.translations: Dict[str, Dict[str, str]] = {}
        self.fallback_language = Language.EN
        
        # Lade alle verfügbaren Sprachen
        self._load_all_languages()
        self._initialized = True
    
    def _load_all_languages(self):
        """Lade alle verfügbaren Sprachdateien"""
        self.languages_dir.mkdir(exist_ok=True)
        
        for lang in Language:
            lang_file = self.languages_dir / f"lang_{lang.value}.xml"
            if lang_file.exists():
                try:
                    self._load_language(lang)
                    logger.info(f"Sprache geladen: {lang.value}")
                except Exception as e:
                    logger.error(f"Fehler beim Laden von {lang.value}: {e}")
    
    def _load_language(self, language: Language):
        """Lade eine spezifische Sprachdatei"""
        lang_file = self.languages_dir / f"lang_{language.value}.xml"
        
        if not lang_file.exists():
            logger.warning(f"Sprachdatei nicht gefunden: {lang_file}")
            return
        
        try:
            tree = ET.parse(lang_file)
            root = tree.getroot()
            
            translations = {}
            
            # Parse alle Kategorien
            for category in root.findall('category'):
                cat_name = category.get('name')
                
                for item in category.findall('item'):
                    key = item.get('key')
                    value = item.text or ""
                    
                    # Unterstütze geschachtelte Keys mit Punkt-Notation
                    full_key = f"{cat_name}.{key}" if cat_name else key
                    translations[full_key] = value
            
            self.translations[language.value] = translations
            
        except ET.ParseError as e:
            logger.error(f"XML-Parse-Fehler in {lang_file}: {e}")
        except Exception as e:
            logger.error(f"Fehler beim Laden von {lang_file}: {e}")
    
    def set_language(self, language: Language):
        """Setze aktuelle Sprache"""
        if language.value not in self.translations:
            logger.warning(f"Sprache {language.value} nicht verfügbar, verwende Fallback")
            return False
        
        self.current_language = language
        logger.info(f"Sprache gewechselt zu: {language.value}")
        return True
    
    def get(self, key: str, **kwargs) -> str:
        """
        Hole übersetzten Text
        
        Args:
            key: Übersetzungsschlüssel (z.B. "system.start_message")
            **kwargs: Variablen für String-Formatierung
        
        Returns:
            Übersetzter Text oder Fallback
        """
        # Versuche aktuelle Sprache
        if self.current_language.value in self.translations:
            text = self.translations[self.current_language.value].get(key)
            if text:
                return self._format_text(text, kwargs)
        
        # Versuche Fallback-Sprache
        if self.fallback_language.value in self.translations:
            text = self.translations[self.fallback_language.value].get(key)
            if text:
                logger.debug(f"Verwende Fallback für Key: {key}")
                return self._format_text(text, kwargs)
        
        # Wenn nichts gefunden, gib Key zurück
        logger.warning(f"Übersetzung nicht gefunden: {key}")
        return f"[{key}]"
    
    def _format_text(self, text: str, variables: Dict[str, Any]) -> str:
        """Formatiere Text mit Variablen"""
        try:
            return text.format(**variables)
        except KeyError as e:
            logger.error(f"Formatierungsfehler: Variable {e} fehlt")
            return text
        except Exception as e:
            logger.error(f"Formatierungsfehler: {e}")
            return text
    
    def get_available_languages(self) -> List[Dict[str, str]]:
        """Hole Liste verfügbarer Sprachen"""
        available = []
        
        for lang in Language:
            if lang.value in self.translations:
                # Hole Sprachname aus der jeweiligen Datei
                lang_name = self.translations[lang.value].get(
                    "meta.language_name", 
                    lang.value.upper()
                )
                available.append({
                    "code": lang.value,
                    "name": lang_name,
                    "native_name": self.translations[lang.value].get(
                        "meta.language_native_name", 
                        lang_name
                    )
                })
        
        return available
    
    def export_missing_keys(self, target_language: Language) -> Dict[str, str]:
        """Exportiere fehlende Übersetzungsschlüssel"""
        if self.fallback_language.value not in self.translations:
            logger.error("Fallback-Sprache nicht geladen")
            return {}
        
        fallback_keys = set(self.translations[self.fallback_language.value].keys())
        
        if target_language.value not in self.translations:
            # Alle Keys fehlen
            return dict(self.translations[self.fallback_language.value])
        
        target_keys = set(self.translations[target_language.value].keys())
        missing_keys = fallback_keys - target_keys
        
        missing_translations = {}
        for key in missing_keys:
            missing_translations[key] = self.translations[self.fallback_language.value][key]
        
        return missing_translations
    
    def create_language_file(self, language: Language, translations: Dict[str, str]):
        """Erstelle neue Sprachdatei"""
        root = ET.Element("translations")
        root.set("language", language.value)
        root.set("version", "1.0")
        
        # Meta-Informationen
        meta = ET.SubElement(root, "category")
        meta.set("name", "meta")
        
        # Gruppiere Übersetzungen nach Kategorie
        categories = {}
        for key, value in translations.items():
            if "." in key:
                category, item_key = key.split(".", 1)
            else:
                category = "general"
                item_key = key
            
            if category not in categories:
                categories[category] = {}
            
            categories[category][item_key] = value
        
        # Erstelle XML-Struktur
        for cat_name, items in categories.items():
            if cat_name == "meta":
                category = meta
            else:
                category = ET.SubElement(root, "category")
                category.set("name", cat_name)
            
            for item_key, value in items.items():
                item = ET.SubElement(category, "item")
                item.set("key", item_key)
                item.text = value
        
        # Speichere Datei
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        
        lang_file = self.languages_dir / f"lang_{language.value}.xml"
        tree.write(lang_file, encoding="utf-8", xml_declaration=True)
        
        logger.info(f"Sprachdatei erstellt: {lang_file}")
        
        # Lade neue Sprache
        self._load_language(language)

# Globale Instanz für einfachen Zugriff
lang = LanguageManager()

# Hilfsfunktionen für direkten Zugriff
def _(key: str, **kwargs) -> str:
    """Shortcut für Übersetzungen"""
    return lang.get(key, **kwargs)

def set_language(language: Language) -> bool:
    """Setze globale Sprache"""
    return lang.set_language(language)

def get_language() -> Language:
    """Hole aktuelle Sprache"""
    return lang.current_language

# Initialisiere beim Import
lang = LanguageManager()
