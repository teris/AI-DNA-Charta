# 🌍 Integration des Mehrsprachigkeitssystems

Diese Anleitung zeigt, wie du das neue Mehrsprachigkeitssystem in dein bestehendes AI-DNA Charter Framework integrierst.

## 📁 1. Dateien hinzufügen

Kopiere die folgenden neuen Dateien in dein Projekt:

```bash
# Sprachverwaltung
framework/language_manager.py

# Sprachdateien-Verzeichnis
framework/languages/
├── lang_de.xml    # Deutsch
├── lang_en.xml    # Englisch
└── lang_es.xml    # Spanisch (optional)

# Tools
tools/create_language.py
tools/integrate_languages.py

# Dokumentation
framework/languages/README.md
```

## 🔧 2. Framework aktualisieren

### framework/__init__.py aktualisieren

Ersetze die bestehende `__init__.py` mit der mehrsprachigen Version oder füge die Language-Imports hinzu:

```python
from .language_manager import (
    Language,
    LanguageManager,
    lang,
    _,
    set_language,
    get_language
)

# In __all__ hinzufügen:
__all__ = [
    # ... bestehende Exports ...
    "Language",
    "LanguageManager", 
    "lang",
    "_",
    "set_language",
    "get_language"
]
```

## 🔄 3. Bestehenden Code migrieren

### Automatische Migration

Verwende das Integrationstool für automatische Migration:

```bash
# Vorschau der Änderungen
python tools/integrate_languages.py examples/

# Migrationsbericht erstellen
python tools/integrate_languages.py --report

# Änderungen anwenden
python tools/integrate_languages.py examples/ --apply
```

### Manuelle Migration

Ersetze deutsche Strings mit Übersetzungsschlüsseln:

```python
# Vorher:
print("🧬 AI-DNA Charta System wird gestartet...")

# Nachher:
from language_manager import _
print(_("system.start_message"))
```

Für Strings mit Variablen:

```python
# Vorher:
print(f"🤖 Erstelle KI: {name}")

# Nachher:
print(_("ki.creating", name=name))
```

## 🌐 4. API-Endpoints erweitern

Füge Sprach-Endpoints zu deiner Flask-App hinzu:

```python
@app.before_request
def before_request():
    """Setze Sprache für jeden Request"""
    # Aus Accept-Language Header
    accept_lang = request.headers.get('Accept-Language', '')
    if accept_lang:
        lang_code = accept_lang.split(',')[0].split('-')[0].lower()
        try:
            set_language(Language(lang_code))
        except ValueError:
            pass  # Verwende Standardsprache

@app.route("/languages", methods=["GET"])
def get_languages():
    """Gibt verfügbare Sprachen zurück"""
    from language_manager import lang
    return jsonify({
        "available": lang.get_available_languages(),
        "current": get_language().value
    })

@app.route("/language", methods=["POST"])
def change_language():
    """Ändere Systemsprache"""
    data = request.get_json()
    lang_code = data.get("language", "de")
    
    try:
        new_lang = Language(lang_code)
        success = set_language(new_lang)
        return jsonify({"success": success})
    except ValueError:
        return jsonify({"error": "Invalid language"}), 400
```

## 🧪 5. Testen

### Basis-Test

```python
# test_languages.py
from language_manager import _, set_language, Language

# Test Deutsch
set_language(Language.DE)
assert "wird gestartet" in _("system.start_message")

# Test English
set_language(Language.EN)
assert "starting" in _("system.start_message")

print("✅ Sprachtests erfolgreich!")
```

### CLI-Test

```bash
# Deutsch (Standard)
python examples/app.py

# Englisch
AI_DNA_LANGUAGE=en python examples/app.py

# Spanisch
AI_DNA_LANGUAGE=es python examples/app.py
```

### API-Test

```bash
# Status in verschiedenen Sprachen
curl http://localhost:5000/status -H "Accept-Language: en"
curl http://localhost:5000/status -H "Accept-Language: es"
curl http://localhost:5000/status -H "Accept-Language: de"
```

## 🆕 6. Neue Sprachen hinzufügen

```bash
# Französisch hinzufügen
python tools/create_language.py create fr French Français

# Übersetzen
# Bearbeite framework/languages/lang_fr.xml

# Validieren
python tools/create_language.py validate fr
```

## 📝 7. Best Practices

### 1. Konsistente Schlüssel

Verwende ein konsistentes Schema für Übersetzungsschlüssel:
- `category.subcategory.specific_key`
- Beispiel: `ki.reproduction.success`

### 2. Variablen-Benennung

Verwende sprechende Variablennamen:
```python
_("ki.created", name=ki_name)  # Gut
_("ki.created", n=ki_name)     # Schlecht
```

### 3. Fallback-Strategie

Das System verwendet automatisch Englisch als Fallback:
- DE nicht gefunden → EN verwenden
- EN nicht gefunden → Schlüssel anzeigen

### 4. Kontext beachten

Füge bei Bedarf Kontext-spezifische Übersetzungen hinzu:
```xml
<item key="save_button">Speichern</item>
<item key="save_action">speichern</item>
<item key="save_command">Speichere</item>
```

## 🚀 8. Deployment

### Umgebungsvariablen

```bash
# .env Datei
AI_DNA_LANGUAGE=de  # Standardsprache
```

### Docker

```dockerfile
# In Dockerfile
ENV AI_DNA_LANGUAGE=en
```

### Systemd Service

```ini
# In ai-dna-charter.service
Environment="AI_DNA_LANGUAGE=de"
```

## ❓ Troubleshooting

### Problem: Übersetzung wird nicht gefunden

1. Prüfe ob die Sprachdatei existiert
2. Prüfe XML-Syntax: `xmllint --noout framework/languages/lang_*.xml`
3. Prüfe Schlüssel-Schreibweise

### Problem: Variablen-Fehler

```python
# Fehler: KeyError: 'name'
_("ki.created")  # Variable fehlt

# Richtig:
_("ki.created", name="TestKI")
```

### Problem: Sprache wird nicht geladen

```python
# Debug-Ausgabe aktivieren
import logging
logging.basicConfig(level=logging.DEBUG)

from language_manager import lang
print(lang.translations.keys())  # Zeigt geladene Sprachen
```

## 🎉 Fertig!

Das Mehrsprachigkeitssystem ist jetzt integriert. Das Framework unterstützt nun:

- ✅ Mehrere Sprachen (DE, EN, ES, ...)
- ✅ Automatische Spracherkennung
- ✅ API-basierter Sprachwechsel
- ✅ Einfaches Hinzufügen neuer Sprachen
- ✅ Konsistente Übersetzungen
- ✅ Fallback-Mechanismus

Bei Fragen oder Problemen, erstelle ein Issue im GitHub Repository!
