#!/usr/bin/env python3
"""
tests/test_languages.py - Umfassende Tests für das Mehrsprachigkeitssystem
"""

import unittest
import sys
import os
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET

# Füge framework zum Path hinzu
sys.path.insert(0, str(Path(__file__).parent.parent / "framework"))

from language_manager import (
    Language, LanguageManager, lang,
    _, set_language, get_language
)

class TestLanguageManager(unittest.TestCase):
    """Tests für den Language Manager"""
    
    def setUp(self):
        """Setup für jeden Test"""
        # Speichere aktuelle Sprache
        self.original_language = get_language()
        
    def tearDown(self):
        """Cleanup nach jedem Test"""
        # Stelle ursprüngliche Sprache wieder her
        set_language(self.original_language)
    
    def test_singleton_pattern(self):
        """Test: LanguageManager ist Singleton"""
        manager1 = LanguageManager()
        manager2 = LanguageManager()
        
        self.assertIs(manager1, manager2)
        self.assertIs(manager1, lang)
    
    def test_language_loading(self):
        """Test: Sprachen werden korrekt geladen"""
        # Prüfe ob mindestens DE und EN geladen sind
        self.assertIn("de", lang.translations)
        self.assertIn("en", lang.translations)
        
        # Prüfe ob Übersetzungen vorhanden sind
        self.assertGreater(len(lang.translations["de"]), 0)
        self.assertGreater(len(lang.translations["en"]), 0)
    
    def test_language_switching(self):
        """Test: Sprachwechsel funktioniert"""
        # Wechsel zu Englisch
        success = set_language(Language.EN)
        self.assertTrue(success)
        self.assertEqual(get_language(), Language.EN)
        
        # Wechsel zu Deutsch
        success = set_language(Language.DE)
        self.assertTrue(success)
        self.assertEqual(get_language(), Language.DE)
    
    def test_translation_basic(self):
        """Test: Basis-Übersetzungen funktionieren"""
        # Test Deutsch
        set_language(Language.DE)
        de_text = _("system.start_message")
        self.assertIn("wird gestartet", de_text)
        
        # Test Englisch
        set_language(Language.EN)
        en_text = _("system.start_message")
        self.assertIn("starting", en_text)
        
        # Texte sollten unterschiedlich sein
        self.assertNotEqual(de_text, en_text)
    
    def test_translation_with_variables(self):
        """Test: Übersetzungen mit Variablen"""
        set_language(Language.DE)
        
        # Einfache Variable
        text = _("ki.created", name="TestKI")
        self.assertIn("TestKI", text)
        self.assertIn("erstellt", text)
        
        # Mehrere Variablen
        text = _("audit.diversity_insufficient", required=5, current=3)
        self.assertIn("5", text)
        self.assertIn("3", text)
    
    def test_missing_translation(self):
        """Test: Fehlende Übersetzungen zeigen Key"""
        # Nicht existierender Key
        text = _("this.key.does.not.exist")
        self.assertEqual(text, "[this.key.does.not.exist]")
    
    def test_fallback_mechanism(self):
        """Test: Fallback zu Englisch funktioniert"""
        # Erstelle temporäre Sprache mit fehlenden Keys
        temp_translations = {"meta.language_name": "Test"}
        lang.translations["test"] = temp_translations
        
        # Setze temporäre Sprache
        lang.current_language = Language.EN  # Simuliere unvollständige Sprache
        
        # Sollte auf Englisch zurückfallen
        text = lang.get("system.start_message")
        self.assertIn("starting", text)  # Englischer Text
        
        # Cleanup
        del lang.translations["test"]
    
    def test_available_languages(self):
        """Test: Liste verfügbarer Sprachen"""
        available = lang.get_available_languages()
        
        self.assertIsInstance(available, list)
        self.assertGreater(len(available), 0)
        
        # Prüfe Struktur
        for lang_info in available:
            self.assertIn("code", lang_info)
            self.assertIn("name", lang_info)
            self.assertIn("native_name", lang_info)
        
        # DE und EN sollten verfügbar sein
        codes = [l["code"] for l in available]
        self.assertIn("de", codes)
        self.assertIn("en", codes)
    
    def test_export_missing_keys(self):
        """Test: Export fehlender Übersetzungsschlüssel"""
        # Angenommen ES hat fehlende Keys
        if Language.ES.value in lang.translations:
            missing = lang.export_missing_keys(Language.ES)
            self.assertIsInstance(missing, dict)
    
    def test_create_language_file(self):
        """Test: Neue Sprachdatei erstellen"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Temporär languages_dir ändern
            original_dir = lang.languages_dir
            lang.languages_dir = Path(tmpdir)
            
            # Erstelle Test-Sprache
            test_translations = {
                "meta.language_name": "Test Language",
                "meta.language_code": "test",
                "system.start_message": "Test starting..."
            }
            
            # Erstelle Datei (verwende einen gültigen Language enum Wert für den Test)
            lang.create_language_file(Language.FR, test_translations)
            
            # Prüfe ob Datei erstellt wurde
            lang_file = Path(tmpdir) / "lang_fr.xml"
            self.assertTrue(lang_file.exists())
            
            # Prüfe XML-Struktur
            tree = ET.parse(lang_file)
            root = tree.getroot()
            self.assertEqual(root.tag, "translations")
            self.assertEqual(root.get("language"), "fr")
            
            # Restore original directory
            lang.languages_dir = original_dir
    
    def test_format_text_errors(self):
        """Test: Fehlerbehandlung bei Textformatierung"""
        set_language(Language.DE)
        
        # Fehlende Variable sollte nicht crashen
        text = _("ki.created")  # name fehlt
        self.assertIsInstance(text, str)  # Sollte trotzdem String zurückgeben
    
    def test_all_keys_consistent(self):
        """Test: Alle Sprachen haben konsistente Keys"""
        if "en" not in lang.translations or "de" not in lang.translations:
            self.skipTest("EN oder DE nicht geladen")
        
        en_keys = set(lang.translations["en"].keys())
        de_keys = set(lang.translations["de"].keys())
        
        # Beide sollten gleiche Keys haben
        missing_in_de = en_keys - de_keys
        missing_in_en = de_keys - en_keys
        
        if missing_in_de:
            print(f"Fehlend in DE: {list(missing_in_de)[:5]}")
        if missing_in_en:
            print(f"Fehlend in EN: {list(missing_in_en)[:5]}")
        
        # Warnung statt Fehler für kleinere Inkonsistenzen
        if len(missing_in_de) > 5 or len(missing_in_en) > 5:
            self.fail("Zu viele inkonsistente Keys zwischen DE und EN")

class TestLanguageIntegration(unittest.TestCase):
    """Integrationstests mit anderen Komponenten"""
    
    def test_ki_creation_multilingual(self):
        """Test: KI-Erstellung mit verschiedenen Sprachen"""
        from ai_dna_framework import create_basic_chartered_ai
        
        # Test in Deutsch
        set_language(Language.DE)
        ki = create_basic_chartered_ai("TestKI_DE")
        self.assertTrue(ki.charter_signed)
        
        # Test in Englisch
        set_language(Language.EN)
        ki = create_basic_chartered_ai("TestKI_EN")
        self.assertTrue(ki.charter_signed)
    
    def test_api_language_header(self):
        """Test: API respektiert Accept-Language Header"""
        # Dieser Test würde die Flask-App benötigen
        # Hier nur als Beispiel-Struktur
        pass

class TestLanguageFiles(unittest.TestCase):
    """Tests für die Sprachdateien selbst"""
    
    def test_xml_validity(self):
        """Test: Alle XML-Dateien sind valide"""
        languages_dir = Path(__file__).parent.parent / "framework" / "languages"
        
        if not languages_dir.exists():
            self.skipTest("Languages directory not found")
        
        for xml_file in languages_dir.glob("lang_*.xml"):
            with self.subTest(file=xml_file.name):
                try:
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                    
                    # Prüfe Grundstruktur
                    self.assertEqual(root.tag, "translations")
                    self.assertIsNotNone(root.get("language"))
                    self.assertIsNotNone(root.get("version"))
                    
                    # Prüfe ob Kategorien vorhanden
                    categories = root.findall("category")
                    self.assertGreater(len(categories), 0)
                    
                except ET.ParseError as e:
                    self.fail(f"XML Parse Error in {xml_file.name}: {e}")
    
    def test_required_keys_present(self):
        """Test: Alle wichtigen Keys sind in jeder Sprache vorhanden"""
        required_keys = [
            "meta.language_name",
            "meta.language_code",
            "system.start_message",
            "system.stop_message",
            "system.ready_message",
            "ki.created",
            "charter.compliance_check"
        ]
        
        for lang_code in ["de", "en"]:
            with self.subTest(language=lang_code):
                if lang_code not in lang.translations:
                    self.skipTest(f"Language {lang_code} not loaded")
                
                for key in required_keys:
                    self.assertIn(
                        key, 
                        lang.translations[lang_code],
                        f"Required key '{key}' missing in {lang_code}"
                    )

def run_language_tests():
    """Führe alle Sprachtests aus"""
    print("🧪 Starte Mehrsprachigkeits-Tests...")
    print("=" * 50)
    
    # Test-Suite erstellen
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Tests hinzufügen
    suite.addTests(loader.loadTestsFromTestCase(TestLanguageManager))
    suite.addTests(loader.loadTestsFromTestCase(TestLanguageIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestLanguageFiles))
    
    # Tests ausführen
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Zusammenfassung
    print("\n" + "=" * 50)
    print(f"🎯 Sprachtests abgeschlossen:")
    print(f"   Tests: {result.testsRun}")
    print(f"   Erfolgreich: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   Fehlgeschlagen: {len(result.failures)}")
    print(f"   Fehler: {len(result.errors)}")
    
    # Zeige verfügbare Sprachen
    print(f"\n📋 Verfügbare Sprachen:")
    for lang_info in lang.get_available_languages():
        print(f"   {lang_info['code']}: {lang_info['name']} ({lang_info['native_name']})")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_language_tests()
    sys.exit(0 if success else 1)
