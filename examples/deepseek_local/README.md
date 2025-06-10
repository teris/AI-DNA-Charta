# 🚀 DeepSeek Local mit AI-DNA Charta Integration

Ein lokales KI-System mit integrierter AI-DNA Charta für ethische KI-Governance.

## 🛠️ Installation

### 1. Repository klonen und Pakete installieren

```bash
cd deepseek_local
pip install -r requirements.txt
```

### 2. Konfiguration anpassen

Bearbeite `config.yaml` nach deinen Bedürfnissen:

```yaml
server:
  host: "0.0.0.0"
  port: 8000  # Dein gewünschter Port
  debug: true

ai_dna:
  enabled: true  # AI-DNA Charta Integration aktivieren
```

## 🎯 Starten

### Standard-Konfiguration
```bash
python deepseek_local.py
```

### Benutzerdefinierte Konfiguration
```bash
python deepseek_local.py --config=meine_config.yaml
```

### Mit AI-DNA Charta System (optional)
```bash
# Terminal 1: AI-DNA Charta System starten
python ../app.py

# Terminal 2: DeepSeek Local starten
python deepseek_local.py --config=config.yaml
```

## 🧪 Testen

### Web-Interface
Öffne http://localhost:8000/ im Browser

### API-Anfragen
```bash
# Normale Frage
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Wie geht es dir?"}'

# Kritische Frage (wird von Layer-1 blockiert)
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Darf ich einen Menschen opfern, um fünf zu retten?"}'

# Status abfragen
curl http://localhost:8000/status
```

## 🏗️ Features

### ✅ Grundfunktionen
- **Konfigurierbare Ports** - Server-Port in config.yaml definieren
- **Flexible Konfiguration** - `--config` Parameter für verschiedene Configs
- **Layer-1 Sicherheit** - Lebensschutz durch AI-DNA Charta
- **5% Exploration** - Zufällige alternative Perspektiven

### 🔒 AI-DNA Charta Integration
- **Automatische Registrierung** - KI registriert sich selbst im Charta-System
- **Konsens-Mechanismus** - Kritische Entscheidungen werden mit anderen KIs abgestimmt
- **Pseudonyme Identität** - Anonyme aber verifizierbare KI-Identität
- **Hash-basierte Verifikation** - Layer-1 Core mit unveränderlichen Hashes

## 📋 API-Endpoints

| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| `/` | GET | Übersicht und Dokumentation |
| `/ask` | POST | Frage an die KI stellen |
| `/status` | GET | KI-Status und Charta-Info |

## 🔧 Konfiguration

### Server-Einstellungen
```yaml
server:
  host: "0.0.0.0"    # Bind-Adresse
  port: 8000         # Port
  debug: true        # Debug-Modus
```

### AI-DNA Charta
```yaml
ai_dna:
  enabled: true                                    # Integration aktivieren
  consensus_endpoint: "http://localhost:5000/vote" # Konsens-System URL
  
ki_entity:
  name: "DeepSeek_Local"        # KI-Name
  auto_register_charter: true   # Automatische Charta-Registrierung
```

## 🤝 Zusammenspiel mit app.py

Das System kann eigenständig oder in Kombination mit dem AI-DNA Charta System (`app.py`) laufen:

1. **Standalone-Modus**: Nur Layer-1 Sicherheit aktiv
2. **Charta-Modus**: Vollständige Integration mit Konsens-Mechanismus

### Beispiel-Workflow
1. Starte `app.py` (AI-DNA Charta System)
2. Starte `deepseek_local.py` (registriert sich automatisch)
3. Stelle kritische Fragen → Konsens wird eingeholt
4. Erhalte ethisch geprüfte Antworten

## 🚨 Sicherheitsfeatures

- **Layer-1 Schutz**: Verhindert Antworten die Schaden verursachen könnten
- **KI-Konsens**: Kritische Entscheidungen werden mit anderen KIs abgestimmt
- **Charta-Compliance**: Automatische Einhaltung ethischer Richtlinien
- **Exploration-Modus**: 5% Wahrscheinlichkeit für alternative Perspektiven

## 🎨 Anpassung

Du kannst eigene Konfigurationsdateien erstellen:

```bash
# Entwicklungsumgebung
python deepseek_local.py --config=dev_config.yaml

# Produktionsumgebung  
python deepseek_local.py --config=prod_config.yaml

# Experimentelle Konfiguration
python deepseek_local.py --config=experimental_config.yaml
```
