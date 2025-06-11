#!/usr/bin/env python3
"""
setup_system.py - Einmaliges Setup für das AI-DNA Charter System
Installiert Dependencies, erstellt Verzeichnisse, konfiguriert System
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import List, Dict

class SystemSetup:
    """Setup für das AI-DNA Charter System"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def run_full_setup(self) -> bool:
        """Führe vollständiges Setup durch"""
        print("🧬 AI-DNA Charter System Setup")
        print("=" * 40)
        
        steps = [
            ("Prüfe Python-Version", self._check_python),
            ("Erstelle Verzeichnisse", self._create_directories),
            ("Installiere Dependencies", self._install_dependencies),
            ("Erstelle Konfigurationen", self._create_configs),
            ("Setze Executable-Rechte", self._set_executable_permissions),
            ("Prüfe Framework", self._verify_framework),
            ("Erstelle Beispiel-Daten", self._create_example_data),
            ("Führe Test-Installation durch", self._test_installation),
        ]
        
        for step_name, step_func in steps:
            print(f"\n🔧 {step_name}...")
            try:
                if not step_func():
                    self.errors.append(f"Fehler bei: {step_name}")
            except Exception as e:
                self.errors.append(f"Exception bei {step_name}: {e}")
                print(f"   ❌ {e}")
        
        self._print_summary()
        return len(self.errors) == 0
    
    def _check_python(self) -> bool:
        """Prüfe Python-Version"""
        version = sys.version_info
        
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            print(f"   ❌ Python {version.major}.{version.minor} zu alt (mindestens 3.7 erforderlich)")
            return False
        
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    
    def _create_directories(self) -> bool:
        """Erstelle notwendige Verzeichnisse"""
        directories = [
            "generated_kis",
            "logs",
            "tests",
            "tools",
            "docs",
            "docker",
            "scripts"
        ]
        
        for dir_name in directories:
            dir_path = self.base_dir / dir_name
            dir_path.mkdir(exist_ok=True)
            print(f"   📁 {dir_name}")
        
        return True
    
    def _install_dependencies(self) -> bool:
        """Installiere Python-Dependencies"""
        requirements = [
            "flask>=2.0.0",
            "requests>=2.25.0", 
            "pyyaml>=6.0",
            "psutil>=5.8.0"
        ]
        
        # Prüfe pip
        try:
            subprocess.run([sys.executable, "-m", "pip", "--version"], 
                         check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print("   ❌ pip nicht verfügbar")
            return False
        
        # Installiere Pakete
        for req in requirements:
            try:
                print(f"   📦 Installiere {req}...")
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "--user", req
                ], check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Fehler bei {req}: {e}")
                return False
        
        print("   ✅ Alle Dependencies installiert")
        return True
    
    def _create_configs(self) -> bool:
        """Erstelle Standard-Konfigurationen"""
        
        # CLI-Config
        cli_config = {
            "default_mode": "full",
            "auto_start_browser": True,
            "log_level": "INFO",
            "api_timeout": 30
        }
        
        config_file = self.base_dir / "config" / "cli_config.json"
        config_file.parent.mkdir(exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump(cli_config, f, indent=2)
        
        print(f"   📄 CLI-Konfiguration: {config_file}")
        
        # Test-Config für DeepSeek
        test_config = {
            "server": {
                "host": "127.0.0.1",
                "port": 8001,  # Test-Port
                "debug": False
            },
            "ethical_rules": {
                "layer_1_active": True,
                "5_percent_random": True,
                "required_diversity": 5
            },
            "ai_dna": {
                "enabled": True,
                "consensus_endpoint": "http://localhost:5001/vote"  # Test-Port
            },
            "ki_entity": {
                "name": "TestDeepSeek",
                "auto_register_charter": False  # Für Tests
            }
        }
        
        test_config_file = self.base_dir / "examples" / "deepseek_local" / "test_config.yaml"
        
        import yaml
        with open(test_config_file, 'w') as f:
            yaml.dump(test_config, f, default_flow_style=False)
        
        print(f"   📄 Test-Konfiguration: {test_config_file}")
        
        return True
    
    def _set_executable_permissions(self) -> bool:
        """Setze Executable-Rechte für Scripts"""
        scripts = [
            "start_ai_dna.sh",
            "start_ai_dna_mac.sh",
            "tools/charter_cli.py",
            "tools/system_manager.py"
        ]
        
        if os.name != 'nt':  # Nicht Windows
            for script in scripts:
                script_path = self.base_dir / script
                if script_path.exists():
                    os.chmod(script_path, 0o755)
                    print(f"   🔧 Executable: {script}")
        
        return True
    
    def _verify_framework(self) -> bool:
        """Prüfe Framework-Installation"""
        framework_file = self.base_dir / "framework" / "ai_dna_framework.py"
        
        if not framework_file.exists():
            print("   ❌ Framework nicht gefunden")
            return False
        
        # Versuche Framework zu importieren
        sys.path.insert(0, str(self.base_dir / "framework"))
        
        try:
            import ai_dna_framework
            print("   ✅ Framework importierbar")
            
            # Test: Erstelle Test-KI
            ki = ai_dna_framework.create_basic_chartered_ai("SetupTestKI")
            if ki.charter_signed:
                print("   ✅ KI-Erstellung funktioniert")
                return True
            else:
                print("   ❌ KI-Erstellung fehlerhaft")
                return False
                
        except ImportError as e:
            print(f"   ❌ Framework-Import fehlgeschlagen: {e}")
            return False
    
    def _create_example_data(self) -> bool:
        """Erstelle Beispiel-Daten für Tests"""
        
        # Beispiel-KI-Konfiguration
        example_ki_config = {
            "name": "ExampleKI",
            "bio_sensors": True,
            "resource_usage": 0.03,
            "cognitive_models": [
                "symbolic", "neural", "logical", "statistical", "evolutionary"
            ],
            "energy_compensation": 0.12,
            "triple_ki_approval": True,
            "human_oversight": True
        }
        
        example_file = self.base_dir / "examples" / "example_ki_config.yaml"
        
        import yaml
        with open(example_file, 'w') as f:
            yaml.dump(example_ki_config, f, default_flow_style=False)
        
        print(f"   📄 Beispiel-KI-Config: {example_file}")
        
        # Quick-Test-Script
        quick_test = '''#!/usr/bin/env python3
"""Quick-Test für AI-DNA Charter System"""

import sys
from pathlib import Path

# Framework importieren
sys.path.insert(0, str(Path(__file__).parent.parent / "framework"))

def quick_test():
    try:
        from ai_dna_framework import create_basic_chartered_ai, DecisionContext
        
        print("🧪 Quick-Test startet...")
        
        # KI erstellen
        ki = create_basic_chartered_ai("QuickTestKI")
        print(f"✅ KI erstellt: {ki.entity_id}")
        
        # Entscheidung treffen
        context = DecisionContext(input_data="Test decision")
        decision = ki.make_decision(context)
        print(f"✅ Entscheidung getroffen: {decision['type']}")
        
        # Status prüfen
        status = ki.get_status()
        print(f"✅ Status: Charter unterzeichnet = {status['charter_signed']}")
        
        print("🎉 Quick-Test erfolgreich!")
        return True
        
    except Exception as e:
        print(f"❌ Quick-Test fehlgeschlagen: {e}")
        return False

if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1)
'''
        
        quick_test_file = self.base_dir / "scripts" / "quick_test.py"
        with open(quick_test_file, 'w') as f:
            f.write(quick_test)
        
        if os.name != 'nt':
            os.chmod(quick_test_file, 0o755)
        
        print(f"   🧪 Quick-Test-Script: {quick_test_file}")
        
        return True
    
    def _test_installation(self) -> bool:
        """Teste die Installation"""
        print("   🧪 Führe Installations-Test durch...")
        
        # Teste Quick-Test-Script
        quick_test_script = self.base_dir / "scripts" / "quick_test.py"
        
        try:
            result = subprocess.run([
                sys.executable, str(quick_test_script)
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("   ✅ Installations-Test erfolgreich")
                return True
            else:
                print(f"   ❌ Installations-Test fehlgeschlagen: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("   ❌ Installations-Test Timeout")
            return False
        except Exception as e:
            print(f"   ❌ Installations-Test Fehler: {e}")
            return False
    
    def _print_summary(self):
        """Zeige Setup-Zusammenfassung"""
        print("\n" + "=" * 40)
        print("📋 Setup-Zusammenfassung:")
        
        if self.errors:
            print(f"\n❌ Fehler ({len(self.errors)}):")
            for error in self.errors:
                print(f"   - {error}")
        
        if self.warnings:
            print(f"\n⚠️ Warnungen ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   - {warning}")
        
        if not self.errors:
            print("\n✅ Setup erfolgreich abgeschlossen!")
            print("\n🚀 Nächste Schritte:")
            print("   1. Starte System: ./start_ai_dna.sh")
            print("   2. Oder verwende CLI: python tools/charter_cli.py start")
            print("   3. Quick-Test: python scripts/quick_test.py")
            print("   4. Web-Interface: http://localhost:5000")
        else:
            print(f"\n❌ Setup fehlgeschlagen ({len(self.errors)} Fehler)")
            print("   Prüfe die Fehlermeldungen und versuche es erneut")


# =============================================================================
# Docker-Integration
# =============================================================================

def create_dockerfile():
    """Erstelle Dockerfile für das System"""
    
    dockerfile_content = '''# AI-DNA Charter System Docker Image
FROM python:3.9-slim

# Metadaten
LABEL maintainer="TerisC"
LABEL description="AI-DNA Charter System - Ethical AI Framework"
LABEL version="2.1.1"

# Arbeitsverzeichnis
WORKDIR /app

# System-Dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# Python-Dependencies kopieren und installieren
COPY framework/requirements.txt /app/framework/
COPY examples/deepseek_local/requirements.txt /app/examples/deepseek_local/
RUN pip install --no-cache-dir -r framework/requirements.txt
RUN pip install --no-cache-dir -r examples/deepseek_local/requirements.txt

# Quellcode kopieren
COPY . /app/

# Executable-Rechte setzen
RUN chmod +x /app/tools/charter_cli.py
RUN chmod +x /app/tools/system_manager.py

# Ports freigeben
EXPOSE 5000 8000

# Gesundheitscheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \\
    CMD curl -f http://localhost:5000/status || exit 1

# Standard-Kommando
CMD ["python", "tools/system_manager.py", "start", "--detached"]
'''

    return dockerfile_content

def create_docker_compose():
    """Erstelle docker-compose.yml"""
    
    compose_content = '''version: '3.8'

services:
  ai-dna-charter:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5000:5000"  # Charta-System
      - "8000:8000"  # DeepSeek Local
    environment:
      - PYTHONPATH=/app/framework
      - CHARTER_MODE=docker
    volumes:
      - ./logs:/app/logs
      - ./generated_kis:/app/generated_kis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/status"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  ai-dna-test:
    build:
      context: .
      dockerfile: Dockerfile
    command: ["python", "tests/test_full_system.py"]
    environment:
      - PYTHONPATH=/app/framework
    depends_on:
      - ai-dna-charter
    profiles:
      - test

networks:
  default:
    name: ai-dna-network

volumes:
  logs:
  generated_kis:
'''

    return compose_content


# =============================================================================
# Shell-Script-Integration
# =============================================================================

def update_shell_scripts():
    """Aktualisiere Shell-Scripts für Python-Integration"""
    
    # Bash-Script-Erweiterung
    bash_integration = '''
# =============================================================================
# Python-Integration für start_ai_dna.sh
# =============================================================================

# Funktion: Prüfe Python-Tools
check_python_tools() {
    print_info "Prüfe Python-Tools..."
    
    local tools=(
        "tools/charter_cli.py"
        "tools/system_manager.py"
        "tests/test_full_system.py"
    )
    
    for tool in "${tools[@]}"; do
        if [[ -f "$tool" ]]; then
            print_status "$tool gefunden"
        else
            print_warning "$tool fehlt"
        fi
    done
}

# Funktion: Python-basierter Start
start_with_python() {
    print_info "Starte mit Python System Manager..."
    
    if [[ -f "tools/system_manager.py" ]]; then
        $PYTHON_CMD tools/system_manager.py start --detached
    else
        print_error "System Manager nicht gefunden - verwende Legacy-Start"
        start_full_system
    fi
}

# Funktion: Python-basierte Tests
run_python_tests() {
    print_info "Führe Python-Tests aus..."
    
    if [[ -f "tests/test_full_system.py" ]]; then
        $PYTHON_CMD tests/test_full_system.py
    else
        print_warning "Python-Tests nicht gefunden"
        return 1
    fi
}

# Funktion: CLI-Tool verwenden
use_cli_tool() {
    print_info "Verwende Charter-CLI..."
    
    if [[ -f "tools/charter_cli.py" ]]; then
        $PYTHON_CMD tools/charter_cli.py "$@"
    else
        print_error "Charter-CLI nicht gefunden"
        return 1
    fi
}

# Erweiterte Menü-Optionen
show_extended_menu() {
    echo ""
    echo "Erweiterte Optionen:"
    echo "  [8] Python System Manager verwenden"
    echo "  [9] Charter CLI-Tool"
    echo "  [t] Python-Tests ausführen"
    echo "  [s] Setup-System ausführen"
    echo ""
}

# Setup-System
run_setup() {
    print_info "Führe System-Setup aus..."
    
    if [[ -f "setup_system.py" ]]; then
        $PYTHON_CMD setup_system.py
    else
        print_warning "Setup-System nicht gefunden"
        print_info "Führe manuelle Installation durch..."
        install_dependencies
    fi
}

# Integration in Hauptschleife (für start_ai_dna.sh)
handle_extended_commands() {
    local choice="$1"
    
    case $choice in
        8)
            start_with_python
            ;;
        9)
            echo -n "CLI-Befehl eingeben: "
            read cli_command
            use_cli_tool $cli_command
            ;;
        t|T)
            run_python_tests
            ;;
        s|S)
            run_setup
            ;;
        *)
            return 1  # Nicht behandelt
            ;;
    esac
    
    return 0  # Behandelt
}
'''

    return bash_integration


# =============================================================================
# Haupt-Setup-Funktion
# =============================================================================

def main():
    """Haupt-Setup-Funktion"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI-DNA Charter System Setup")
    parser.add_argument('--docker', action='store_true', help='Erstelle Docker-Dateien')
    parser.add_argument('--shell', action='store_true', help='Aktualisiere Shell-Scripts')
    parser.add_argument('--quick', action='store_true', help='Schnelles Setup (nur Dependencies)')
    
    args = parser.parse_args()
    
    setup = SystemSetup()
    
    if args.docker:
        print("🐳 Erstelle Docker-Konfiguration...")
        
        # Dockerfile
        dockerfile_path = setup.base_dir / "Dockerfile"
        with open(dockerfile_path, 'w') as f:
            f.write(create_dockerfile())
        print(f"   📄 {dockerfile_path}")
        
        # docker-compose.yml
        compose_path = setup.base_dir / "docker-compose.yml"
        with open(compose_path, 'w') as f:
            f.write(create_docker_compose())
        print(f"   📄 {compose_path}")
        
        print("✅ Docker-Dateien erstellt")
        return
    
    if args.shell:
        print("🐚 Aktualisiere Shell-Script-Integration...")
        
        integration_path = setup.base_dir / "scripts" / "shell_integration.sh"
        integration_path.parent.mkdir(exist_ok=True)
        
        with open(integration_path, 'w') as f:
            f.write(update_shell_scripts())
        
        print(f"   📄 {integration_path}")
        print("   💡 Füge in start_ai_dna.sh hinzu: source scripts/shell_integration.sh")
        print("✅ Shell-Integration erstellt")
        return
    
    if args.quick:
        print("⚡ Schnelles Setup...")
        success = setup._install_dependencies() and setup._verify_framework()
    else:
        success = setup.run_full_setup()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()


# =============================================================================
# Erstelle auch ein einfaches Makefile für Linux/Mac
# =============================================================================

MAKEFILE_CONTENT = '''# AI-DNA Charter System Makefile

.PHONY: help setup install test start stop clean docker

# Default target
help:
	@echo "🧬 AI-DNA Charter System"
	@echo "========================"
	@echo ""
	@echo "Verfügbare Targets:"
	@echo "  setup     - Vollständiges System-Setup"
	@echo "  install   - Nur Dependencies installieren"
	@echo "  test      - Tests ausführen"
	@echo "  start     - System starten"
	@echo "  stop      - System stoppen"
	@echo "  clean     - Temporäre Dateien löschen"
	@echo "  docker    - Docker-Container bauen und starten"
	@echo ""

# Setup
setup:
	@echo "🔧 Führe vollständiges Setup durch..."
	python setup_system.py

# Nur Dependencies
install:
	@echo "📦 Installiere Dependencies..."
	python setup_system.py --quick

# Tests
test:
	@echo "🧪 Führe Tests durch..."
	python tests/test_full_system.py

# System starten
start:
	@echo "🚀 Starte System..."
	python tools/system_manager.py start --detached

# System stoppen
stop:
	@echo "🛑 Stoppe System..."
	python tools/system_manager.py stop

# Cleanup
clean:
	@echo "🧹 Räume auf..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	rm -f .ai_dna_pids.json
	rm -rf logs/*.log

# Docker
docker:
	@echo "🐳 Baue und starte Docker-Container..."
	python setup_system.py --docker
	docker-compose up --build -d

# Docker-Tests
docker-test:
	@echo "🧪 Führe Docker-Tests durch..."
	docker-compose --profile test up --build --abort-on-container-exit

# Status
status:
	@echo "📊 System-Status:"
	python tools/system_manager.py status

# CLI
cli:
	@echo "💻 Charter CLI:"
	@echo "Verwende: python tools/charter_cli.py --help"
'''

def create_makefile(base_dir: Path):
    """Erstelle Makefile"""
    makefile_path = base_dir / "Makefile"
    with open(makefile_path, 'w') as f:
        f.write(MAKEFILE_CONTENT)
    
    print(f"📄 Makefile erstellt: {makefile_path}")
    print("   Verwende: make help")
