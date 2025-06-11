#!/usr/bin/env python3
"""
tools/create_language.py - Tool zum Erstellen neuer Sprachdateien
Hilft beim Hinzufügen neuer Sprachen zum AI-DNA Charter System
"""

import argparse
import sys
from pathlib import Path
from typing import Dict

# Füge framework zum Path hinzu
sys.path.insert(0, str(Path(__file__).parent.parent / "framework"))

from language_manager import Language, LanguageManager, lang

def create_new_language(lang_code: str, lang_name: str, native_name: str):
    """Erstelle neue Sprachdatei basierend auf Template"""
    
    # Prüfe ob Sprache bereits existiert
    try:
        language = Language(lang_code)
    except ValueError:
        print(f"❌ Ungültiger Sprachcode: {lang_code}")
        print(f"   Gültige Codes: {', '.join([l.value for l in Language])}")
        return False
    
    # Hole alle Keys aus der Fallback-Sprache (EN)
    if Language.EN.value not in lang.translations:
        print("❌ Englische Sprachdatei (Fallback) nicht gefunden!")
        return False
    
    # Kopiere englische Übersetzungen als Template
    template_translations = dict(lang.translations[Language.EN.value])
    
    # Setze Meta-Informationen
    template_translations["meta.language_name"] = lang_name
    template_translations["meta.language_native_name"] = native_name
    template_translations["meta.language_code"] = lang_code
    
    # Erstelle Sprachdatei
    lang.create_language_file(language, template_translations)
    
    print(f"✅ Sprachdatei erstellt: lang_{lang_code}.xml")
    print(f"   Sprache: {lang_name} ({native_name})")
    print(f"   Übersetzungen: {len(template_translations)} Keys")
    print(f"\n📝 Nächste Schritte:")
    print(f"   1. Öffne framework/languages/lang_{lang_code}.xml")
    print(f"   2. Übersetze alle <item> Texte")
    print(f"   3. Teste mit: python tools/test_language.py {lang_code}")
    
    return True

def export_missing_translations(target_lang_code: str):
    """Exportiere fehlende Übersetzungen für eine Sprache"""
    try:
        target_language = Language(target_lang_code)
    except ValueError:
        print(f"❌ Ungültiger Sprachcode: {target_lang_code}")
        return False
    
    missing = lang.export_missing_keys(target_language)
    
    if not missing:
        print(f"✅ Keine fehlenden Übersetzungen für {target_lang_code}")
        return True
    
    # Speichere fehlende Übersetzungen
    output_file = Path(f"missing_translations_{target_lang_code}.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Fehlende Übersetzungen für {target_lang_code}\n")
        f.write(f"# Insgesamt: {len(missing)} Keys\n\n")
        
        for key, english_text in sorted(missing.items()):
            f.write(f"# {key}\n")
            f.write(f"EN: {english_text}\n")
            f.write(f"{target_lang_code.upper()}: \n\n")
    
    print(f"✅ Fehlende Übersetzungen exportiert: {output_file}")
    print(f"   Anzahl: {len(missing)} Keys")
    
    return True

def list_languages():
    """Liste alle verfügbaren Sprachen auf"""
    available = lang.get_available_languages()
    
    print("🌍 Verfügbare Sprachen:")
    print("=" * 50)
    
    for lang_info in available:
        print(f"  {lang_info['code']:5} - {lang_info['name']:20} ({lang_info['native_name']})")
    
    print(f"\n📊 Gesamt: {len(available)} Sprachen")
    
    # Zeige welche Sprachen noch fehlen
    available_codes = [l['code'] for l in available]
    missing_codes = [l.value for l in Language if l.value not in available_codes]
    
    if missing_codes:
        print(f"\n⚠️ Noch nicht implementiert: {', '.join(missing_codes)}")

def validate_language(lang_code: str):
    """Validiere eine Sprachdatei"""
    try:
        language = Language(lang_code)
    except ValueError:
        print(f"❌ Ungültiger Sprachcode: {lang_code}")
        return False
    
    if language.value not in lang.translations:
        print(f"❌ Sprachdatei nicht gefunden: lang_{lang_code}.xml")
        return False
    
    # Prüfe Vollständigkeit
    if Language.EN.value not in lang.translations:
        print("❌ Englische Referenz-Datei nicht gefunden")
        return False
    
    en_keys = set(lang.translations[Language.EN.value].keys())
    target_keys = set(lang.translations[language.value].keys())
    
    missing = en_keys - target_keys
    extra = target_keys - en_keys
    
    print(f"🔍 Validiere Sprache: {lang_code}")
    print("=" * 50)
    print(f"  Referenz-Keys (EN): {len(en_keys)}")
    print(f"  Übersetzte Keys: {len(target_keys)}")
    
    if missing:
        print(f"\n❌ Fehlende Übersetzungen: {len(missing)}")
        for key in sorted(list(missing)[:10]):  # Zeige max 10
            print(f"    - {key}")
        if len(missing) > 10:
            print(f"    ... und {len(missing) - 10} weitere")
    
    if extra:
        print(f"\n⚠️ Zusätzliche Keys (nicht in EN): {len(extra)}")
        for key in sorted(list(extra)[:5]):
            print(f"    - {key}")
    
    if not missing and not extra:
        print("\n✅ Sprachdatei ist vollständig und konsistent!")
        return True
    
    return False

def main():
    parser = argparse.ArgumentParser(
        description="Tool zum Verwalten von Sprachen im AI-DNA Charter System",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Verfügbare Befehle')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Erstelle neue Sprachdatei')
    create_parser.add_argument('code', help='Sprachcode (z.B. es, fr, it)')
    create_parser.add_argument('name', help='Sprachname auf Englisch (z.B. Spanish)')
    create_parser.add_argument('native', help='Sprachname in der Sprache selbst (z.B. Español)')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Exportiere fehlende Übersetzungen')
    export_parser.add_argument('code', help='Ziel-Sprachcode')
    
    # List command
    subparsers.add_parser('list', help='Liste alle Sprachen auf')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validiere Sprachdatei')
    validate_parser.add_argument('code', help='Sprachcode zu validieren')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'create':
            success = create_new_language(args.code, args.name, args.native)
            sys.exit(0 if success else 1)
            
        elif args.command == 'export':
            success = export_missing_translations(args.code)
            sys.exit(0 if success else 1)
            
        elif args.command == 'list':
            list_languages()
            
        elif args.command == 'validate':
            success = validate_language(args.code)
            sys.exit(0 if success else 1)
            
    except Exception as e:
        print(f"❌ Fehler: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
