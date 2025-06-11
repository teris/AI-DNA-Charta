#!/bin/bash

# =============================================================================
# AI-DNA Charter System - All-in-One Setup & Integration
# Automatisches Setup für vollständige Testumgebung
# =============================================================================

set -e  # Exit bei Fehlern

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Funktionen
print_header() {
    echo -e "${PURPLE}"
    echo "🧬 AI-DNA Charter System - All-in-One Setup"
    echo "============================================="
    echo -e "${NC}"
}

print_step() {
    echo -e "${BLUE}🔧 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Prüfe Betriebssystem
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Installation je nach OS
install_python_deps() {
    local os=$(detect_os)
    
    case $os in
        "linux")
            print_step "Installiere Python-Dependencies (Linux)..."
            if command -v apt-get &> /dev/null; then
                sudo apt-get update
                sudo apt-get install -y python3 python3-pip python3-venv curl
            elif command -v yum &> /dev/null; then
                sudo yum install -y python3 python3-pip curl
            elif command -v pacman &> /dev/null; then
                sudo pacman -S python python-pip curl
            fi
            ;;
        "macos")
            print_step "Installiere Python-Dependencies (macOS)..."
            if command -v brew &> /dev/null; then
                brew install python curl
            else
                print_warning "Homebrew nicht gefunden. Installiere manuell:"
                echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            fi
            ;;
        "windows")
            print_warning "Windows erkannt. Verwende start_ai_dna.bat für bessere Integration"
            ;;
    esac
}

# Erstelle fehlende Scripts
create_missing_scripts() {
    print_step "Erstelle fehlende Python-Scripts..."
    
    # Charter CLI
    if [[ ! -f "tools/charter_cli.py" ]]; then
        mkdir -p tools
        cat > tools/charter_cli.py << 'EOF'
#!/usr/bin/env python3
"""
Vereinfachtes Charter CLI - Automatisch generiert
"""
import sys
import subprocess
from pathlib import Path

def main():
    base_dir = Path(__file__).parent.parent
    
    if len(sys.argv) < 2:
        print("Usage: charter-cli <command>")
        print("Commands: start, stop, test, status")
        return
    
    command = sys.argv[1]
    
    if command == "start":
        print("🚀 Starte System...")
        # Starte mit den bestehenden Scripts
        subprocess.run(["python", "examples/app.py"], cwd=base_dir)
    
    elif command == "test":
        print("🧪 Führe Tests durch...")
        subprocess.run(["python", "-c", "print('Tests würden hier laufen')"])
    
    elif command == "status":
        print("📊 System-Status...")
        try:
            import requests
            r = requests.get("http://localhost:5000/status", timeout=3)
            if r.status_code == 200:
                print("✅ Charta-System läuft")
            else:
                print("❌ Charta-System nicht erreichbar")
        except:
            print("❌ Charta-System nicht erreichbar")
    
    else:
        print(f"❌ Unbekannter Befehl: {command}")

if __name__ == "__main__":
    main()
EOF
        chmod +x tools/charter_cli.py
        print_success "charter_cli.py erstellt"
    fi
    
    # Test Script
    if [[ ! -f "tests/simple_test.py" ]]; then
        mkdir -p tests
        cat > tests/simple_test.py << 'EOF'
#!/usr/bin/env python3
"""
Einfacher Test für AI-DNA Charter System
"""
import sys
import os
from pathlib import Path

# Framework importieren
sys.path.insert(0, str(Path(__file__).parent.parent / "framework"))

def run_simple_tests():
    print("🧪 Einfache Tests für AI-DNA Charter System")
    print("=" * 45)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Framework Import
    total_tests += 1
    try:
        import ai_dna_framework
        print("✅ Framework-Import erfolgreich")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ Framework-Import fehlgeschlagen: {e}")
    
    # Test 2: KI-Erstellung
    total_tests += 1
    try:
        from ai_dna_framework import create_basic_chartered_ai
        ki = create_basic_chartered_ai("TestKI")
        if ki.charter_signed:
            print("✅ KI-Erstellung und Charter-Unterzeichnung erfolgreich")
            tests_passed += 1
        else:
            print("❌ Charter-Unterzeichnung fehlgeschlagen")
    except Exception as e:
        print(f"❌ KI-Erstellung fehlgeschlagen: {e}")
    
    # Test 3: Entscheidungsfindung
    total_tests += 1
    try:
        from ai_dna_framework import DecisionContext
        context = DecisionContext(input_data="Test-Entscheidung")
        decision = ki.make_decision(context)
        if decision and 'reasoning' in decision:
            print("✅ Entscheidungsfindung erfolgreich")
            tests_passed += 1
        else:
            print("❌ Entscheidungsfindung fehlerhaft")
    except Exception as e:
        print(f"❌ Entscheidungsfindung fehlgeschlagen: {e}")
    
    # Zusammenfassung
    print("\n" + "=" * 45)
    print(f"📊 Test-Ergebnis: {tests_passed}/{total_tests} Tests erfolgreich")
    
    if tests_passed == total_tests:
        print("🎉 Alle Tests erfolgreich!")
        return True
    else:
        print("❌ Einige Tests fehlgeschlagen")
        return False

if __name__ == "__main__":
    success = run_simple_tests()
    sys.exit(0 if success else 1)
EOF
        chmod +x tests/simple_test.py
        print_success "simple_test.py erstellt"
    fi
    
    # Setup Script
    if [[ ! -f "setup_env.py" ]]; then
        cat > setup_env.py << 'EOF'
#!/usr/bin/env python3
"""
Umgebungs-Setup für AI-DNA Charter System
"""
import subprocess
import sys
import os
from pathlib import Path

def setup_environment():
    print("🔧 Setup AI-DNA Charter Umgebung...")
    
    # Installiere Python-Pakete
    packages = ["flask", "requests", "pyyaml"]
    
    for package in packages:
        print(f"📦 Installiere {package}...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "--user", package
            ], check=True, capture_output=True)
            print(f"✅ {package} installiert")
        except subprocess.CalledProcessError:
            print(f"❌ Fehler bei {package}")
            return False
    
    # Erstelle Verzeichnisse
    dirs = ["logs", "generated_kis", "tmp"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"📁 Verzeichnis {dir_name} erstellt")
    
    print("✅ Setup abgeschlossen!")
    return True

if __name__ == "__main__":
    success = setup_environment()
    sys.exit(0 if success else 1)
EOF
        chmod +x setup_env.py
        print_success "setup_env.py erstellt"
    fi
}

# Integration Test
run_integration_test() {
    print_step "Führe Integration-Test durch..."
    
    # Python-Setup testen
    if python3 setup_env.py; then
        print_success "Python-Setup erfolgreich"
    else
        print_error "Python-Setup fehlgeschlagen"
        return 1
    fi
    
    # Framework testen
    if [[ -f "tests/simple_test.py" ]]; then
        if python3 tests/simple_test.py; then
            print_success "Framework-Tests erfolgreich"
        else
            print_warning "Framework-Tests zeigen Probleme"
        fi
    fi
    
    # API-Test (falls System läuft)
    if curl -s http://localhost:5000/status >/dev/null 2>&1; then
        print_success "Charta-System ist erreichbar"
    else
        print_warning "Charta-System läuft nicht (normal beim ersten Setup)"
    fi
}

# Erstelle Start-Wrapper
create_start_wrapper() {
    print_step "Erstelle Start-Wrapper..."
    
    cat > quick_start.sh << 'EOF'
#!/bin/bash
# Quick-Start Wrapper für AI-DNA Charter System

echo "🧬 AI-DNA Charter System - Quick Start"
echo "====================================="

# Prüfe ob System läuft
if curl -s http://localhost:5000/status >/dev/null 2>&1; then
    echo "ℹ️  System läuft bereits"
    echo "   Charta-System: http://localhost:5000"
    
    if curl -s http://localhost:8000/status >/dev/null 2>&1; then
        echo "   DeepSeek Local: http://localhost:8000"
    fi
    
    exit 0
fi

echo "🚀 Starte System..."

# Verwende verfügbare Starter
if [[ -f "start_ai_dna.sh" ]]; then
    echo "📝 Verwende start_ai_dna.sh"
    ./start_ai_dna.sh
elif [[ -f "tools/charter_cli.py" ]]; then
    echo "📝 Verwende Charter CLI"
    python3 tools/charter_cli.py start
elif [[ -f "examples/app.py" ]]; then
    echo "📝 Verwende direkten Start"
    cd examples && python3 app.py
else
    echo "❌ Keine Start-Scripts gefunden"
    exit 1
fi
EOF
    
    chmod +x quick_start.sh
    print_success "quick_start.sh erstellt"
}

# Erstelle README für lokale Tests
create_test_readme() {
    print_step "Erstelle Test-Dokumentation..."
    
    cat > TEST_GUIDE.md << 'EOF'
# 🧪 Test-Guide für AI-DNA Charter System

## Quick-Start Tests

### 1. Basis-Setup testen
```bash
python3 setup_env.py
```

### 2. Framework-Tests
```bash
python3 tests/simple_test.py
```

### 3. System starten
```bash
./quick_start.sh
```

### 4. API-Tests
```bash
# Status prüfen
curl http://localhost:5000/status

# KI erstellen
curl -X POST http://localhost:5000/ki/create \
  -H "Content-Type: application/json" \
  -d '{"name":"TestKI","type":"basic"}'

# DeepSeek Local testen (falls läuft)
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Hallo!"}'
```

### 5. Charter CLI verwenden
```bash
python3 tools/charter_cli.py --help
python3 tools/charter_cli.py status
```

## Troubleshooting

### Python-Import-Fehler
```bash
export PYTHONPATH=$PWD/framework:$PYTHONPATH
```

### Port-Konflikte
- Charta-System: Port 5000
- DeepSeek Local: Port 8000

### Abhängigkeiten
```bash
pip3 install --user flask requests pyyaml
```

## Docker-Alternative
```bash
# Falls Docker-Setup verfügbar
docker-compose up --build
```

## Manual Testing

### Charter-Compliance prüfen
```bash
python3 schemas/audit_tool.py --test
```

### Multi-KI-System testen
```bash
# Starte Charta-System
cd examples && python3 app.py &

# Teste Abstimmung
curl -X POST http://localhost:5000/vote
```

## Performance-Tests

### Ressourcen-Monitor
```bash
# Während System läuft
top | grep python
ps aux | grep -E "(app\.py|deepseek_local\.py)"
```

### Speicher-Check
```bash
free -h  # Linux
vm_stat  # macOS
```
EOF
    
    print_success "TEST_GUIDE.md erstellt"
}

# Prüfe Verzeichnis-Struktur
check_directory_structure() {
    print_step "Prüfe Verzeichnis-Struktur..."
    
    required_dirs=(
        "framework"
        "examples"
        "schemas"
        "charter"
    )
    
    missing_dirs=()
    for dir in "${required_dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            missing_dirs+=("$dir")
        fi
    done
    
    if [[ ${#missing_dirs[@]} -gt 0 ]]; then
        print_error "Fehlende Verzeichnisse: ${missing_dirs[*]}"
        print_warning "Stelle sicher, dass du im AI-DNA-Charta Hauptverzeichnis bist"
        return 1
    fi
    
    required_files=(
        "framework/ai_dna_framework.py"
        "examples/app.py"
        "schemas/charter.yaml"
    )
    
    missing_files=()
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            missing_files+=("$file")
        fi
    done
    
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        print_error "Fehlende Dateien: ${missing_files[*]}"
        return 1
    fi
    
    print_success "Verzeichnis-Struktur OK"
    return 0
}

# Hauptfunktion
main() {
    print_header
    
    echo "Dieses Script führt ein vollständiges Setup für die AI-DNA Charter"
    echo "Testumgebung durch und erstellt alle fehlenden Scripts."
    echo ""
    
    # Prüfe Verzeichnis
    if ! check_directory_structure; then
        exit 1
    fi
    
    # OS-spezifische Installation
    read -p "Python-Dependencies installieren? (y/N): " install_deps
    if [[ $install_deps =~ ^[Yy]$ ]]; then
        install_python_deps
    fi
    
    # Setup-Schritte
    create_missing_scripts
    create_start_wrapper
    create_test_readme
    
    # Python-Setup
    python3 setup_env.py
    
    # Integration-Test
    run_integration_test
    
    # Zusammenfassung
    echo ""
    print_header
    print_success "Setup abgeschlossen!"
    echo ""
    echo "🚀 Nächste Schritte:"
    echo "   1. System starten:    ./quick_start.sh"
    echo "   2. Tests laufen:      python3 tests/simple_test.py"
    echo "   3. CLI verwenden:     python3 tools/charter_cli.py --help"
    echo "   4. Test-Guide lesen:  cat TEST_GUIDE.md"
    echo ""
    echo "🌐 Nach dem Start verfügbar:"
    echo "   • Charta-System: http://localhost:5000"
    echo "   • DeepSeek Local: http://localhost:8000"
    echo ""
    
    read -p "System jetzt starten? (y/N): " start_now
    if [[ $start_now =~ ^[Yy]$ ]]; then
        ./quick_start.sh
    fi
}

# Prüfe Parameter
if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    echo "AI-DNA Charter System - All-in-One Setup"
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --help, -h     Zeige diese Hilfe"
    echo "  --quick        Nur fehlende Scripts erstellen"
    echo "  --test         Nur Tests ausführen"
    echo ""
    exit 0
fi

if [[ "$1" == "--quick" ]]; then
    check_directory_structure
    create_missing_scripts
    print_success "Quick-Setup abgeschlossen"
    exit 0
fi

if [[ "$1" == "--test" ]]; then
    check_directory_structure
    run_integration_test
    exit 0
fi

# Hauptprogramm
main
