#!/bin/bash

# ========================================
# AI-DNA Charta System Starter (Linux)
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
    echo "🧬 AI-DNA Charta System Starter"
    echo "================================"
    echo -e "${NC}"
}

# Prüfe ob tmux verfügbar ist (für bessere Terminal-Verwaltung)
command -v tmux >/dev/null 2>&1
TMUX_AVAILABLE=$?

# Header anzeigen
clear
print_header

# Prüfe Python Installation
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        print_error "Python ist nicht installiert oder nicht im PATH"
        echo "Installiere Python:"
        echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip"
        echo "  CentOS/RHEL:   sudo yum install python3 python3-pip"
        echo "  Arch:          sudo pacman -S python python-pip"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

print_status "Python gefunden: $($PYTHON_CMD --version)"

# Prüfe pip
if ! command -v pip3 &> /dev/null; then
    if ! command -v pip &> /dev/null; then
        print_error "pip ist nicht installiert"
        echo "Installiere pip: sudo apt install python3-pip"
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

# Funktion: Dependencies installieren
install_dependencies() {
    print_info "Installiere Abhängigkeiten..."
    
    # Basis-Abhängigkeiten
    $PIP_CMD install flask requests pyyaml --user
    
    # DeepSeek Local Abhängigkeiten
    if [[ -f "examples/deepseek_local/requirements.txt" ]]; then
        $PIP_CMD install -r examples/deepseek_local/requirements.txt --user
    fi
    
    print_status "Abhängigkeiten installiert"
}

# Funktion: Vollständiges System starten
start_full_system() {
    print_info "Starte vollständiges AI-DNA System..."
    
    if [[ $TMUX_AVAILABLE -eq 0 ]]; then
        # Mit tmux (empfohlen)
        print_info "Verwende tmux für bessere Terminal-Verwaltung"
        
        # Neue tmux Session
        tmux new-session -d -s ai_dna_system
        
        # Charta-System (Fenster 0)
        tmux send-keys -t ai_dna_system:0 "cd examples && $PYTHON_CMD app.py" Enter
        tmux rename-window -t ai_dna_system:0 "Charta-System"
        
        # DeepSeek Local (Fenster 1)
        tmux new-window -t ai_dna_system -n "DeepSeek-Local"
        tmux send-keys -t ai_dna_system:1 "cd examples/deepseek_local && $PYTHON_CMD deepseek_local.py --config=config.yaml" Enter
        
        # Status-Fenster (Fenster 2)
        tmux new-window -t ai_dna_system -n "Status"
        tmux send-keys -t ai_dna_system:2 "sleep 10 && curl http://localhost:5000/status && echo && curl http://localhost:8000/status" Enter
        
        # Attach zu Session
        echo ""
        print_status "System gestartet in tmux Session 'ai_dna_system'"
        print_info "Verwende 'tmux attach -t ai_dna_system' um zur Session zu wechseln"
        print_info "Fenster wechseln: Ctrl+B dann 0/1/2"
        print_info "Session beenden: 'tmux kill-session -t ai_dna_system'"
        
        tmux attach -t ai_dna_system
        
    else
        # Ohne tmux (fallback)
        print_warning "tmux nicht verfügbar - starte in separaten Background-Prozessen"
        
        # Charta-System
        cd examples
        $PYTHON_CMD app.py &
        CHARTA_PID=$!
        cd ..
        
        # Kurz warten
        sleep 3
        
        # DeepSeek Local
        cd examples/deepseek_local
        $PYTHON_CMD deepseek_local.py --config=config.yaml &
        DEEPSEEK_PID=$!
        cd ../..
        
        print_status "Prozesse gestartet:"
        echo "  Charta-System: PID $CHARTA_PID (Port 5000)"
        echo "  DeepSeek Local: PID $DEEPSEEK_PID (Port 8000)"
        
        # Cleanup-Funktion registrieren
        trap "kill $CHARTA_PID $DEEPSEEK_PID 2>/dev/null" EXIT
        
        # Warte auf Benutzer-Eingabe
        echo ""
        print_info "Drücke Ctrl+C um beide Prozesse zu beenden"
        wait
    fi
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

# Funktion: Browser öffnen (falls möglich)
open_browser() {
    if command -v xdg-open &> /dev/null; then
        xdg-open "$1"
    elif command -v firefox &> /dev/null; then
        firefox "$1" &
    elif command -v google-chrome &> /dev/null; then
        google-chrome "$1" &
    elif command -v chromium-browser &> /dev/null; then
        chromium-browser "$1" &
    else
        print_warning "Kein Browser gefunden - öffne manuell: $1"
    fi
}

# Funktion: Kollaborations-Tools öffnen
open_collab_tools() {
    print_info "Öffne Kollaborations-Tools..."
    
    if [[ -f "docs/ai_charta_collaboration_tool.html" ]]; then
        open_browser "file://$(pwd)/docs/ai_charta_collaboration_tool.html"
    fi
    
    if [[ -f "docs/index.html" ]]; then
        open_browser "file://$(pwd)/docs/index.html"
    fi
    
    print_status "Kollaborations-Tools geöffnet"
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
    echo "  [q] Beenden"
    echo ""
}

# Funktion: System Status
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
        q|Q)
            print_info "Auf Wiedersehen!"
            exit 0
            ;;
        *)
            print_error "Ungültige Auswahl"
            ;;
    esac
    
    echo ""
    echo "================================"
done
