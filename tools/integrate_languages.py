#!/usr/bin/env python3
"""
tools/integrate_languages.py - Integriere Mehrsprachigkeit in bestehende Dateien
Hilft bei der Migration des bestehenden Codes zur mehrsprachigen Version
"""

import re
import os
from pathlib import Path
from typing import List, Tuple, Dict

class LanguageIntegrator:
    """Tool zur Integration von Mehrsprachigkeit in bestehenden Code"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        
        # Mapping von deutschen Strings zu Übersetzungsschlüsseln
        self.string_mappings = {
            # System-Nachrichten
            '🧬 AI-DNA Charta System wird gestartet...': 'system.start_message',
            '🛑 AI-DNA Charta System wird beendet...': 'system.stop_message',
            '✅ System bereit!': 'system.ready_message',
            
            # KI-Nachrichten
            '🤖 Erstelle KI:': 'ki.creating',
            '✅ KI erstellt:': 'ki.created',
            '📜 Charta unterzeichnet': 'ki.charter_signed',
            '❌ Charta nicht unterzeichnet': 'ki.charter_unsigned',
            '👶 KI-Reproduktion gestartet...': 'ki.reproduction_started',
            '❌ Nicht genug Ressourcen für Reproduktion': 'ki.insufficient_resources',
            
            # Charter-Nachrichten
            '🔍 Prüfe Charta-Compliance...': 'charter.compliance_check',
            '✅ Charta-Compliance bestanden': 'charter.compliance_passed',
            '🛡️ Layer-1 Schutz aktiv': 'charter.layer1_active',
            
            # Konsens-Nachrichten
            '✅ Konsens erreicht': 'consensus.consensus_reached',
            '❌ Kein Konsens erreicht': 'consensus.consensus_failed',
            '❌ Nicht genug Teilnehmer für Abstimmung': 'consensus.insufficient_participants',
        }
        
        # Regex-Patterns für komplexere Strings
        self.regex_patterns = [
            # f-Strings mit Variablen
            (r'f"(.*)Erstelle KI: \{(\w+)\}"', r'_(\"ki.creating\", \2=\2)'),
            (r'f"(.*)KI erstellt: \{(\w+)\}"', r'_(\"ki.created\", \2=\2)'),
            (r'f"(.*)Fehler: \{(\w+)\}"', r'_(\"system.error_general\", error=\2)'),
            
            # print-Statements
            (r'print\("([^"]+)"\)', r'print(_("\1"))'),
            (r'print\(f"([^"]+)"\)', r'print(_(f"\1"))'),
        ]
    
    def analyze_file(self, filepath: Path) -> List[Tuple[int, str, str]]:
        """Analysiere eine Datei und finde zu ersetzende Strings"""
        if not filepath.exists():
            return []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        replacements = []
        
        for i, line in enumerate(lines):
            # Direkte String-Ersetzungen
            for de_string, key in self.string_mappings.items():
                if de_string in line:
                    # Erstelle Ersetzung
                    if 'print(' in line:
                        new_line = line.replace(f'"{de_string}"', f'_("{key}")')
                    else:
                        new_line = line.replace(de_string, f'_("{key}")')
                    
                    replacements.append((i + 1, line.strip(), new_line.strip()))
            
            # Regex-basierte Ersetzungen
            for pattern, replacement in self.regex_patterns:
                match = re.search(pattern, line)
                if match:
                    new_line = re.sub(pattern, replacement, line)
                    if new_line != line:
                        replacements.append((i + 1, line.strip(), new_line.strip()))
        
        return replacements
    
    def add_imports(self, filepath: Path) -> str:
        """Füge notwendige Imports hinzu"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Prüfe ob Imports bereits vorhanden
        if 'from language_manager import' in content:
            return content
        
        # Finde beste Position für Import
        import_lines = []
        lines = content.split('\n')
        
        # Nach anderen Imports suchen
        last_import_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                last_import_idx = i
        
        # Import-Statement
        import_statement = """
# Sprachunterstützung
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "framework"))
from language_manager import _, set_language, get_language, Language
"""
        
        # Füge Import nach den anderen Imports ein
        lines.insert(last_import_idx + 1, import_statement)
        
        return '\n'.join(lines)
    
    def integrate_file(self, filepath: Path, dry_run: bool = True) -> bool:
        """Integriere Mehrsprachigkeit in eine Datei"""
        print(f"\n📄 Analysiere: {filepath.relative_to(self.base_dir)}")
        
        # Analysiere Datei
        replacements = self.analyze_file(filepath)
        
        if not replacements:
            print("   ✅ Keine Änderungen notwendig")
            return True
        
        print(f"   🔍 Gefunden: {len(replacements)} zu ersetzende Stellen")
        
        if dry_run:
            # Zeige Vorschau
            for line_num, old, new in replacements[:5]:  # Max 5 anzeigen
                print(f"   Zeile {line_num}:")
                print(f"     - {old}")
                print(f"     + {new}")
            
            if len(replacements) > 5:
                print(f"   ... und {len(replacements) - 5} weitere")
            
            return True
        
        # Führe Ersetzungen durch
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Sortiere Ersetzungen rückwärts nach Zeilennummer
        replacements.sort(key=lambda x: x[0], reverse=True)
        
        for line_num, old, new in replacements:
            lines[line_num - 1] = lines[line_num - 1].replace(old.strip(), new.strip())
        
        # Füge Imports hinzu
        content = ''.join(lines)
        content = self.add_imports(filepath)
        
        # Schreibe Datei
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ {len(replacements)} Ersetzungen durchgeführt")
        return True
    
    def integrate_directory(self, directory: Path, dry_run: bool = True) -> None:
        """Integriere Mehrsprachigkeit in alle Python-Dateien eines Verzeichnisses"""
        py_files = list(directory.rglob("*.py"))
        
        print(f"🔍 Gefundene Python-Dateien: {len(py_files)}")
        
        if dry_run:
            print("\n⚠️  DRY RUN - Keine Dateien werden geändert")
            print("   Verwende --apply um Änderungen durchzuführen\n")
        
        success_count = 0
        for py_file in py_files:
            # Überspringe bestimmte Dateien
            if any(skip in str(py_file) for skip in ['__pycache__', '.git', 'venv', 'env']):
                continue
            
            if self.integrate_file(py_file, dry_run):
                success_count += 1
        
        print(f"\n📊 Zusammenfassung:")
        print(f"   Analysierte Dateien: {len(py_files)}")
        print(f"   Erfolgreiche Integration: {success_count}")
    
    def create_migration_report(self, directory: Path) -> None:
        """Erstelle einen Migrationsbericht"""
        report_path = self.base_dir / "language_migration_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as report:
            report.write("# AI-DNA Charter - Sprach-Migrationsbericht\n\n")
            report.write(f"Erstellt am: {Path.ctime(Path())}\n\n")
            
            report.write("## Zu migrierende Dateien\n\n")
            
            py_files = list(directory.rglob("*.py"))
            total_changes = 0
            
            for py_file in py_files:
                if any(skip in str(py_file) for skip in ['__pycache__', '.git', 'venv']):
                    continue
                
                replacements = self.analyze_file(py_file)
                if replacements:
                    report.write(f"### {py_file.relative_to(self.base_dir)}\n")
                    report.write(f"Änderungen: {len(replacements)}\n\n")
                    
                    for line_num, old, new in replacements[:3]:
                        report.write(f"- Zeile {line_num}: `{old[:50]}...`\n")
                    
                    if len(replacements) > 3:
                        report.write(f"- ... und {len(replacements) - 3} weitere\n")
                    
                    report.write("\n")
                    total_changes += len(replacements)
            
            report.write(f"## Zusammenfassung\n\n")
            report.write(f"- Gesamtanzahl Dateien: {len(py_files)}\n")
            report.write(f"- Dateien mit Änderungen: {sum(1 for f in py_files if self.analyze_file(f))}\n")
            report.write(f"- Gesamtanzahl Änderungen: {total_changes}\n")
        
        print(f"📄 Migrationsbericht erstellt: {report_path}")

def main():
    """Hauptfunktion"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Integriere Mehrsprachigkeit in AI-DNA Charter Code"
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Pfad zur Datei oder Verzeichnis (Standard: aktuelles Verzeichnis)'
    )
    
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Führe Änderungen durch (ohne dieses Flag nur Vorschau)'
    )
    
    parser.add_argument(
        '--report',
        action='store_true',
        help='Erstelle nur einen Migrationsbericht'
    )
    
    args = parser.parse_args()
    
    integrator = LanguageIntegrator()
    path = Path(args.path)
    
    if args.report:
        integrator.create_migration_report(path if path.is_dir() else path.parent)
    elif path.is_file():
        integrator.integrate_file(path, dry_run=not args.apply)
    elif path.is_dir():
        integrator.integrate_directory(path, dry_run=not args.apply)
    else:
        print(f"❌ Pfad nicht gefunden: {path}")

if __name__ == "__main__":
    main()
