# 🌍 AI-DNA Charter - Mehrsprachigkeitssystem

Das AI-DNA Charter Framework unterstützt nun mehrere Sprachen, um eine internationale Nutzung zu ermöglichen.

## 📂 Struktur

```
framework/
├── language_manager.py     # Haupt-Sprachverwaltung
└── languages/
    ├── lang_de.xml        # Deutsch (Standard)
    ├── lang_en.xml        # English
    ├── lang_es.xml        # Español
    ├── lang_fr.xml        # Français
    └── ...                # Weitere Sprachen
```

## 🚀 Verwendung

### In Python-Code

```python
from language_manager import _, set_language, Language

# Text abrufen (verwendet aktuelle Sprache)
print(_("system.start_message"))

# Sprache wechseln
set_language(Language.EN)

# Text mit Variablen
print(_("ki.created", name="TestKI"))
```

### Umgebungsvariable

```bash
# Setze Standardsprache
export AI_DNA_LANGUAGE=en
python examples/app.py
```

### API-Endpoints

```bash
# Verfügbare Sprachen abrufen
curl http://localhost:5000/languages

# Sprache wechseln
curl -X POST http://localhost:5000/language \
  -H "Content-Type: application/json" \
  -d '{"language": "en"}'

# Mit Accept-Language Header
curl http://localhost:5000/status \
  -H "Accept-Language: en"
```

## 🛠️ Neue Sprache hinzufügen

### 1. Sprachdatei erstellen

```bash
# Tool verwenden
python tools/create_language.py create es Spanish Español

# Oder manuell
cp framework/languages/lang_en.xml framework/languages/lang_es.xml
```

### 2. Übersetzungen hinzufügen

Bearbeite `framework/languages/lang_es.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<translations language="es" version="1.0">
  <category name="system">
    <item key="start_message">🧬 Sistema AI-DNA Charter iniciando...</item>
    <!-- Weitere Übersetzungen -->
  </category>
</translations>
```

### 3. Fehlende Übersetzungen finden

```bash
# Exportiere fehlende Keys
python tools/create_language.py export es

# Validiere Vollständigkeit
python tools/create_language.py validate es
```

## 📋 Unterstützte Sprachen

| Code | Sprache | Native | Status |
|------|---------|--------|---------|
| de | Deutsch | Deutsch | ✅ Vollständig |
| en | English | English | ✅ Vollständig |
| es | Spanish | Español | 🚧 In Arbeit |
| fr | French | Français | 🚧 In Arbeit |
| it | Italian | Italiano | 📝 Geplant |
| pt | Portuguese | Português | 📝 Geplant |
| ru | Russian | Русский | 📝 Geplant |
| zh | Chinese | 中文 | 📝 Geplant |
| ja | Japanese | 日本語 | 📝 Geplant |
| ko | Korean | 한국어 | 📝 Geplant |
| ar | Arabic | العربية | 📝 Geplant |
| hi | Hindi | हिन्दी | 📝 Geplant |

## 🔧 Übersetzungsrichtlinien

### Allgemeine Regeln

1. **Konsistenz**: Verwende konsistente Begriffe für KI-Konzepte
2. **Emojis**: Behalte Emojis bei (sie sind universell)
3. **Variablen**: Behalte `{variable}` Platzhalter unverändert
4. **Technische Begriffe**: Übersetze sinnvoll oder behalte Englisch bei

### Beispiele

| Deutsch | English | Español |
|---------|---------|---------|
| Charta unterzeichnet | Charter signed | Carta firmada |
| Konsens-Abstimmung | Consensus vote | Votación de consenso |
| Layer-1 Schutz | Layer-1 protection | Protección Layer-1 |

### Charter-spezifische Begriffe

Einige Begriffe sollten einheitlich übersetzt werden:

- **AI-DNA Charter**: Kann unübersetzt bleiben oder als "AI-DNA Charta" lokalisiert werden
- **Layer-1/Layer-2**: Technische Begriffe, meist unübersetzt
- **CCZ (Charter Compliance Certificate)**: Als Akronym beibehalten
- **KI/AI**: Je nach Sprache anpassen

## 🧪 Testen

### Unit-Tests für Sprachen

```python
# test_languages.py
from language_manager import _, set_language, Language

def test_all_languages():
    for lang in Language:
        set_language(lang)
        # Teste wichtige Keys
        assert len(_("system.start_message")) > 0
        assert "{name}" in _("ki.created", name="Test")
```

### Manuelle Tests

```bash
# Starte System in verschiedenen Sprachen
AI_DNA_LANGUAGE=en python examples/app.py
AI_DNA_LANGUAGE=es python examples/app.py
AI_DNA_LANGUAGE=fr python examples/app.py
```

## 🤝 Beitragen

Hilf uns, das AI-DNA Charter System in weitere Sprachen zu übersetzen!

1. Forke das Repository
2. Erstelle neue Sprachdatei: `python tools/create_language.py create [code] [name] [native]`
3. Übersetze alle Texte in der XML-Datei
4. Teste deine Übersetzung
5. Erstelle einen Pull Request

### Übersetzungsstatus

- 🟢 Vollständig (100% übersetzt)
- 🟡 Teilweise (>50% übersetzt)
- 🔴 Begonnen (<50% übersetzt)
- ⚪ Geplant (noch nicht begonnen)

## 📚 API-Referenz

### LanguageManager

```python
# Singleton-Instanz
lang = LanguageManager()

# Verfügbare Sprachen
languages = lang.get_available_languages()

# Sprache setzen
lang.set_language(Language.EN)

# Text abrufen
text = lang.get("system.start_message", name="TestKI")
```

### Hilfsfunktionen

```python
# Kurzform für Übersetzungen
from language_manager import _
text = _("ki.created", name="MyKI")

# Globale Sprache setzen
from language_manager import set_language, Language
set_language(Language.FR)

# Aktuelle Sprache abrufen
from language_manager import get_language
current = get_language()  # Language.FR
```

## 🔍 Fehlerbehebung

### Übersetzung nicht gefunden

Wenn `[key.name]` angezeigt wird:
1. Prüfe ob der Key in der Sprachdatei existiert
2. Prüfe ob die Sprachdatei geladen wurde
3. Prüfe die XML-Syntax

### Formatierungsfehler

Bei Fehlern wie "KeyError: 'name'":
1. Prüfe ob alle Variablen übergeben wurden
2. Prüfe die Schreibweise der Variablen

### Sprache nicht verfügbar

1. Prüfe ob die Sprachdatei existiert
2. Prüfe ob die Sprache in der `Language` Enum definiert ist
3. Prüfe die XML-Syntax der Sprachdatei

## 🎯 Zukünftige Erweiterungen

- [ ] Automatische Spracherkennung basierend auf Systemeinstellungen
- [ ] Pluralformen-Unterstützung
- [ ] RTL-Sprachen (Arabisch, Hebräisch) Support
- [ ] Übersetzungs-Cache für bessere Performance
- [ ] Web-basiertes Übersetzungstool
- [ ] Integration mit Übersetzungs-APIs
- [ ] Kontext-sensitive Übersetzungen
