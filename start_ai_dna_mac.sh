#!/bin/bash

# ========================================
# AI-DNA Charta System Starter (macOS)
# ========================================

# Farben für bessere Ausgabe
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Funktion für farbige Ausgabe
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_header() {
    echo -e "${PURPLE}"
    echo "🧬 AI-DNA Charta System Starter (macOS)"
    echo "======================================="
    echo -e "${NC}"
}

# Prüfe ob Homebrew verfügbar ist
command -v brew >/dev/null 2>&1
BREW_AVAILABLE=$?

# Header anzeigen
clear
print_header

# Prüfe Python Installation (macOS-spezifisch)
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        print_error "Python ist nicht installiert"
        echo "Installiere Python:"
        if [[ $BREW_AVAILABLE -eq 0 ]]; then
            echo "  Mit Homebrew: brew install python"
        fi
        echo "  Oder von: https://python.org/downloads/"
        echo "  Oder verwende pyenv: curl https://pyenv.run | bash"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

print_status "Python gefunden: $($PYTHON_CMD --version)"

# Prüfe pip (macOS-spezifisch)
if ! command -v pip3 &> /dev/null; then
    if ! command -v pip &> /dev/null; then
        print_error "pip ist nicht installiert"
        echo "Installiere pip:"
        if [[ $BREW_AVAILABLE -eq 0 ]]; then
            echo "  brew install python (enthält pip)"
        fi
        echo "  Oder: python3 -m ensurepip --upgrade"
        exit 1
    else
        PIP_CMD="pip"
    fi
else
    PIP_CMD="pip3"
fi

# Prüfe Repository-Struktur
if [[ ! -f "examples/app.py" ]]; then
    print_error "Skript muss im Hauptverzeichnis des AI-DNA-Charta Repos ausgeführt werden"
    echo "Aktueller Pfad: $(pwd)"
    echo "Erwartete Dateien: examples/app.py, examples/deepseek_local/"
    exit 1
fi

print_status "Repository-Struktur gefunden"

# macOS Terminal-Verwaltung
open_new_terminal() {
    local title="$1"
    local command="$2"
    
    osascript <<EOF
tell application "Terminal"
    do script "cd \"$(pwd)\" && $command"
    set custom title of front window to "$title"
end tell
EOF
}

# iTerm2-spezifische Funktion (falls verfügbar)
open_iterm_tab() {
    local title="$1"
    local command="$2"
    
    osascript <<EOF
tell application "iTerm"
    tell current session of current tab of current window
        split horizontally with default profile command "cd \"$(pwd)\" && $command"
    end tell
end tell
EOF
}

# Prüfe verfügbare Terminal-Apps
detect_terminal() {
    if pgrep -f "iTerm" > /dev/null; then
        echo "iterm"
    elif pgrep -f "Terminal" > /dev/null; then
        echo "terminal"
    else
        echo "terminal"  # Default zu Terminal.app
    fi
}

# Funktion: Dependencies installieren
install_dependencies() {
    print_info "Installiere Abhängigkeiten..."
    
    # Prüfe auf Xcode Command Line Tools (für eventuelle Kompilierung)
    if ! xcode-select -p &> /dev/null; then
        print_warning "Xcode Command Line Tools nicht gefunden"
        print_info "Installiere mit: xcode-select --install"
        read -p "Möchtest du die Installation jetzt starten? (y/N): " install_xcode
        if [[ $install_xcode =~ ^[Yy]$ ]]; then
            xcode-select --install
            print_info "Warte auf Xcode Installation..."
            read -p "Drücke Enter wenn die Installation abgeschlossen ist..."
        fi
    fi
    
    # Basis-Abhängigkeiten
    $PIP_CMD install --user flask requests pyyaml
    
    # DeepSeek Local Abhängigkeiten
    if [[ -f "examples/deepseek_local/requirements.txt" ]]; then
        print_info "Installiere DeepSeek Local Abhängigkeiten..."
        $PIP_CMD install --user -r examples/deepseek_local/requirements.txt
    fi
    
    print_status "Abhängigkeiten installiert"
}

# Funktion: Vollständiges System starten
start_full_system() {
    print_info "Starte vollständiges AI-DNA System..."
    
    local terminal_type=$(detect_terminal)
    
    case $terminal_type in
        "iterm")
            print_info "Verwende iTerm2 für bessere Terminal-Verwaltung"
            
            # Charta-System
            open_iterm_tab "Charta-System" "cd examples && $PYTHON_CMD app.py"
            sleep 2
            
            # DeepSeek Local
            open_iterm_tab "DeepSeek-Local" "cd examples/deepseek_local && $PYTHON_CMD deepseek_local.py --config=config.yaml"
            ;;
            
        "terminal"|*)
            print_info "Verwende Terminal.app"
            
            # Charta-System
            open_new_terminal "AI-DNA Charta System" "cd examples && $PYTHON_CMD app.py"
            sleep 2
            
            # DeepSeek Local
            open_new_terminal "DeepSeek Local" "cd examples/deepseek_local && $PYTHON_CMD deepseek_local.py --config=config.yaml"
            ;;
    esac
    
    # Kurz warten dann Browser öffnen
    sleep 5
    print_info "Öffne Web-Interfaces..."
    open http://localhost:5000
    open http://localhost:8000
    
    # Kollaborations-Tool öffnen
    if [[ -f "docs/ai_charta_collaboration_tool.html" ]]; then
        open "docs/ai_charta_collaboration_tool.html"
    fi
    
    print_status "System gestartet!"
    print_info "Charta-System: http://localhost:5000"
    print_info "DeepSeek Local: http://localhost:8000"
}

# Funktion: Nur Charta-System
start_charta_only() {
    print_info "Starte nur Charta-System..."
    cd examples
    $PYTHON_CMD app.py
}

# Funktion: Nur DeepSeek Local
start_deepseek_only() {
    print_info "Starte nur DeepSeek Local..."
    
    echo -n "Config-Datei (Enter für Standard 'config.yaml'): "
    read config_file
    config_file=${config_file:-config.yaml}
    
    cd examples/deepseek_local
    $PYTHON_CMD deepseek_local.py --config="$config_file"
}

# Funktion: Kollaborations-Tools öffnen
open_collab_tools() {
    print_info "Öffne Kollaborations-Tools..."
    
    if [[ -f "docs/ai_charta_collaboration_tool.html" ]]; then
        open "docs/ai_charta_collaboration_tool.html"
    fi
    
    if [[ -f "docs/index.html" ]]; then
        open "docs/index.html"
    fi
    
    # GitHub Repository im Browser öffnen
    read -p "GitHub Repository öffnen? (y/N): " open_github
    if [[ $open_github =~ ^[Yy]$ ]]; then
        open "https://github.com/teris/AI-DNA-Charta"
    fi
    
    print_status "Kollaborations-Tools geöffnet"
}

# Funktion: System Status prüfen
check_status() {
    print_info "Prüfe System Status..."
    
    echo "🔍 Port 5000 (Charta-System):"
    if curl -s http://localhost:5000/status >/dev/null; then
        curl -s http://localhost:5000/status | $PYTHON_CMD -m json.tool 2>/dev/null || echo "Charta-System läuft"
    else
        print_warning "Charta-System nicht erreichbar"
    fi
    
    echo ""
    echo "🔍 Port 8000 (DeepSeek Local):"
    if curl -s http://localhost:8000/status >/dev/null; then
        curl -s http://localhost:8000/status | $PYTHON_CMD -m json.tool 2>/dev/null || echo "DeepSeek Local läuft"
    else
        print_warning "DeepSeek Local nicht erreichbar"
    fi
    
    echo ""
    echo "🔍 Laufende Python-Prozesse:"
    ps aux | grep python | grep -E "(app\.py|deepseek_local\.py)" | grep -v grep || echo "Keine AI-DNA Prozesse gefunden"
}

# Funktion: Homebrew-basierte Installation
install_with_homebrew() {
    if [[ $BREW_AVAILABLE -ne 0 ]]; then
        print_error "Homebrew ist nicht installiert"
        echo "Installiere Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        return 1
    fi
    
    print_info "Installiere mit Homebrew..."
    brew install python
    brew install curl
    
    install_dependencies
}

# Hauptmenü
show_menu() {
    echo ""
    echo "Wähle Startmodus:"
    echo "  [1] Vollständiges System (Charta + DeepSeek)"
    echo "  [2] Nur Charta-System (Port 5000)"
    echo "  [3] Nur DeepSeek Local (Port 8000)"
    echo "  [4] Development Setup (Dependencies installieren + Vollsystem)"
    echo "  [5] Kollaborations-Tools öffnen"
    echo "  [6] System Status prüfen"
    echo "  [7] Mit Homebrew installieren"
    echo "  [q] Beenden"
    echo ""
}

# Hauptschleife
while true; do
    show_menu
    read -p "Deine Wahl: " choice
    
    case $choice in
        1)
            start_full_system
            ;;
        2)
            start_charta_only
            ;;
        3)
            start_deepseek_only
            ;;
        4)
            install_dependencies
            start_full_system
            ;;
        5)
            open_collab_tools
            ;;
        6)
            check_status
            ;;
        7)
            install_with_homebrew
            ;;
        q|Q)
            print_info "Auf Wiedersehen! 🧬"
            exit 0
            ;;
        *)
            print_error "Ungültige Auswahl"
            ;;
    esac
    
    echo ""
    echo "================================"
done
