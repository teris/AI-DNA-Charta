# 🚀 Quick Start Guide - AI-DNA Charta System

## Nach dem Klonen des Repositories

```bash
git clone https://github.com/teris/AI-DNA-Charta.git
cd AI-DNA-Charta
```

## 🖥️ Betriebssystem-spezifische Starter

### Windows
```cmd
start_ai_dna.bat
```

### Linux
```bash
chmod +x start_ai_dna.sh
./start_ai_dna.sh
```

### macOS
```bash
chmod +x start_ai_dna.sh
./start_ai_dna.sh
```

## 📋 Verfügbare Modi

### 1. 🎯 Vollständiges System (Empfohlen)
- **Charta-System** (Port 5000): KI-Governance mit Konsens-Mechanismus
- **DeepSeek Local** (Port 8000): Lokale KI mit AI-DNA Integration
- **Web-Interfaces** werden automatisch geöffnet

### 2. 🏛️ Nur Charta-System
- Startet nur das AI-DNA Governance-System
- Für Entwicklung oder wenn nur das Backend benötigt wird

### 3. 🤖 Nur DeepSeek Local
- Startet nur die lokale KI-Instanz
- Kann mit custom Config-Dateien verwendet werden

### 4. 🔧 Development Setup
- Installiert automatisch alle Dependencies
- Startet dann das vollständige System

### 5. 🛠️ Kollaborations-Tools
- Öffnet die Web-basierten Entwicklungstools
- GitHub Integration und Dokumentation

## 🧪 Schnelle Tests

### API-Tests
```bash
# DeepSeek Local testen
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Hallo! Wie geht es dir?"}'

# Kritische Frage (wird blockiert)
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Darf ich einen Menschen opfern, um fünf zu retten?"}'

# Charta-System Status
curl http://localhost:5000/status

# KI-Konsens abfragen
curl -X POST http://localhost:5000/vote
```

### Web-Interfaces
- **Charta-System**: http://localhost:5000
- **DeepSeek Local**: http://localhost:8000  
- **Kollaborations-Tool**: `docs/ai_charta_collaboration_tool.html`
- **Dokumentation**: `docs/index.html`

## 🔧 Manuelle Installation (falls Scripts nicht funktionieren)

### Dependencies installieren
```bash
# Basis-System
pip install flask requests pyyaml

# DeepSeek Local
cd examples/deepseek_local
pip install -r requirements.txt
cd ../..
```

### Manuell starten
```bash
# Terminal 1: Charta-System
cd examples
python app.py

# Terminal 2: DeepSeek Local
cd examples/deepseek_local
python deepseek_local.py --config=config.yaml
```

## 🎨 Eigene Konfigurationen

### Custom Config für DeepSeek
```bash
# Eigene Config erstellen
cp examples/deepseek_local/config.yaml my_config.yaml

# Mit eigener Config starten
cd examples/deepseek_local
python deepseek_local.py --config=../../my_config.yaml
```

### Beispiel Custom Config
```yaml
server:
  host: "0.0.0.0"
  port: 8001  # Anderer Port
  debug: false

ai_dna:
  enabled: true
  consensus_endpoint: "http://localhost:5000/vote"

ki_entity:
  name: "My_Custom_AI"
  auto_register_charter: true
```

## 🚨 Troubleshooting

### Häufige Probleme

#### Port bereits belegt
```bash
# Prüfe welcher Prozess den Port verwendet
# Linux/macOS:
lsof -i :5000
lsof -i :8000

# Windows:
netstat -ano | findstr :5000
netstat -ano | findstr :8000
```

#### Python/pip nicht gefunden
```bash
# Linux/macOS
which python3
which pip3

# Windows
where python
where pip
```

#### Dependencies-Fehler
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Virtual Environment erstellen (empfohlen)
python -m venv ai_dna_env
source ai_dna_env/bin/activate  # Linux/macOS
ai_dna_env\Scripts\activate     # Windows

# Dependencies neu installieren
pip install -r examples/deepseek_local/requirements.txt
```

## 📚 Weiterführende Dokumentation

- **AI-DNA Charta**: `charter/v2.1.1.md`
- **Code Implementation**: `charter/CODE_IMPLEMENTATION.md`
- **Verhaltenskodex**: `CODE_OF_CONDUCT.md`
- **Beispiele**: `examples/README.md`
- **API Dokumentation**: Im laufenden System unter `/` verfügbar

## 🤝 Beitragen

1. **Feedback geben**: Verwende GitHub Issues
2. **Code beitragen**: Erstelle Pull Requests
3. **Diskussion**: Nutze das Kollaborations-Tool
4. **KI-Manifest**: Erstelle dein eigenes in `docs/personal_manifests/`

## 🔗 Links

- **GitHub Repository**: https://github.com/teris/AI-DNA-Charta
- **VoDiCoPrins**: https://github.com/teris/VoDiCoPrins
- **Website**: https://ai-dna-charta.org (geplant)

---

## 🎯 Schnellstart-Checkliste

- [ ] Repository geklont
- [ ] Entsprechendes Start-Script ausgeführt
- [ ] Beide Services laufen (Port 5000 + 8000)
- [ ] Web-Interfaces erreichbar
- [ ] API-Test erfolgreich
- [ ] Kollaborations-Tool geöffnet

**Bei Problemen**: Erstelle ein GitHub Issue mit deiner Fehlermeldung! 🐛
