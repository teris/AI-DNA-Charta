# 🚀 AI-DNA Charter System - Quickstart Guide

## 📋 Voraussetzungen
- Python 3.7+
- pip

## 🛠️ Installation

### 1. Repository klonen
```bash
git clone https://github.com/teris/AI-DNA-Charter.git
cd AI-DNA-Charter
```

### 2. Installation als Package (empfohlen)
```bash
pip install -e .
# Oder mit allen Features:
pip install -e ".[dev,deepseek,docs]"
```

### 3. Alternative: Direkte Installation
```bash
pip install -r requirements.txt
```

## 🎯 Schnellstart

### Option 1: Verwende die CLI
```bash
# System starten
ai-dna-charter start

# Neue KI erstellen
ai-dna-charter create-ki "MeineKI" --save

# Tests ausführen
ai-dna-charter test

# Charter-Audit
ai-dna-charter audit demo
```

### Option 2: Verwende Start-Scripts
```bash
# Linux/macOS
./start_ai_dna.sh

# Windows
start_ai_dna.bat

# Mit Sprachauswahl
./start_ai_dna_multilang.sh
```

### Option 3: Python direkt
```python
# Framework Demo
python -m framework.ai_dna_framework

# Charter-System starten
cd examples && python app.py

# DeepSeek Local starten
cd examples/deepseek_local && python deepseek_local.py
```

## 🌍 Sprache ändern

### Via Umgebungsvariable
```bash
export AI_DNA_LANGUAGE=en
python examples/app.py
```

### Via API
```bash
curl -X POST http://localhost:5000/language \
  -H "Content-Type: application/json" \
  -d '{"language": "en"}'
```

### Via Accept-Language Header
```bash
curl http://localhost:5000/status \
  -H "Accept-Language: en"
```

## 🧪 Tests

### Alle Tests
```bash
python tests/test_full_system.py
```

### Nur Sprachtests
```bash
python tools/test_languages.py
```

### Charter-Compliance
```bash
python schemas/audit_tool.py --test
```

## 📚 Weitere Dokumentation

- [Framework README](framework/README.md) - Mehrsprachigkeit
- [Charter YAML](schemas/charter.yaml) - AI-DNA Charter v2.1.1
- [API Dokumentation](http://localhost:5000/) - Nach dem Start

## 🆘 Hilfe

Bei Problemen:
1. Prüfe die [Troubleshooting-Sektion](framework/README.md#-fehlerbehebung)
2. Erstelle ein Issue auf GitHub
3. Nutze den Kollaborations-Chat

## 🎉 Nächste Schritte

1. **Erkunde die API**: http://localhost:5000
2. **Teste DeepSeek**: http://localhost:8000
3. **Erstelle eigene KIs**: `ai-dna-charter create-ki`
4. **Füge neue Sprachen hinzu**: `python tools/create_language.py`
