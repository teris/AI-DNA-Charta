#!/bin/bash

# ========================================
# AI-DNA Charta System Starter (Multilingual)
# ========================================

# Farben für bessere Ausgabe
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Sprach-Erkennung
detect_language() {
    # 1. Prüfe Umgebungsvariable
    if [[ -n "$AI_DNA_LANGUAGE" ]]; then
        echo "$AI_DNA_LANGUAGE"
        return
    fi
    
    # 2. Prüfe System-Locale
    if command -v locale &> /dev/null; then
        local sys_lang=$(locale | grep LANG= | cut -d= -f2 | cut -d_ -f1 | tr '[:upper:]' '[:lower:]')
        case $sys_lang in
            de|en|es|fr|it|pt|ru|zh|ja|ko|ar|hi)
                echo "$sys_lang"
                return
                ;;
        esac
    fi
    
    # 3. Fallback auf Deutsch
    echo "de"
}

# Setze Sprache
export AI_DNA_LANGUAGE=$(detect_language)

# Python-basierte Übersetzungsfunktion
translate() {
    local key="$1"
    shift
    local args="$@"
    
    # Verwende Python für Übersetzungen
    $PYTHON_CMD -c "
import sys
sys.path.insert(0, 'framework')
try:
    from language_manager import _, set_language, Language
    set_language(Language('$AI_DNA_LANGUAGE'))
    print(_('$key'$args))
except:
    print('$key')
" 2>/dev/null || echo "$key"
}

# Funktion für farbige Ausgabe mit Übersetzung
print_status() {
    echo -e "${GREEN}$(translate "$1" "$2")${NC}"
}

print_error() {
    echo -e "${RED}$(translate "$1" "$2")${NC}"
}

print_info() {
    echo -e "${BLUE}$(translate "$1" "$2")${NC}"
}

print_warning() {
    echo -e "${YELLOW}$(translate "$1" "$2")${NC}"
}

print_header() {
    echo -e "${PURPLE}"
    echo "🧬 AI-DNA Charter System"
    echo "Language/Sprache/Langue: $AI_DNA_LANGUAGE"
    echo "================================"
    echo -e "${NC}"
}

# Prüfe ob tmux verfügbar ist
command -v tmux >/dev/null 2>&1
TMUX_AVAILABLE=$?

# Header anzeigen
clear
print_header

# Prüfe Python Installation
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        print_error "errors.python_not_found"
        echo "Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip"
        echo "CentOS/RHEL:   sudo yum install python3 python3-pip"
        echo "Arch:          sudo pacman -S python python-pip"
        echo "macOS:         brew install python"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

print_status "system.info_general" ", message='Python: $($PYTHON_CMD --version)'"

# Prüfe pip
if ! command -v pip3 &> /dev/null; then
    if ! command -v pip &> /dev/null; then
        print_error "errors.pip_not_found"
        exit 1
    else
        PIP_CMD="pip"
    fi
else
    PIP_CMD="pip3"
fi

# Prüfe Repository-Struktur
if [[ ! -f "examples/app.py" ]]; then
    print_error "errors.wrong_directory"
    echo "$(pwd)"
    exit 1
fi

print_status "system.info_general" ", message='Repository OK'"

# Funktion: Dependencies installieren
install_dependencies() {
    print_info "system.info_general" ", message='Installing dependencies...'"
    
    # Basis-Abhängigkeiten
    $PIP_CMD install flask requests pyyaml --user
    
    # DeepSeek Local Abhängigkeiten
    if [[ -f "examples/deepseek_local/requirements.txt" ]]; then
        $PIP_CMD install -r examples/deepseek_local/requirements.txt --user
    fi
    
    print_status "system.success_general" ", message='Dependencies installed'"
}

# Funktion: Vollständiges System starten
start_full_system() {
    print_info "system.start_message"
    
    if [[ $TMUX_AVAILABLE -eq 0 ]]; then
        # Mit tmux
        print_info "system.info_general" ", message='Using tmux'"
        
        # Neue tmux Session mit Sprachvariable
        tmux new-session -d -s ai_dna_system -e "AI_DNA_LANGUAGE=$AI_DNA_LANGUAGE"
        
        # Charta-System (Fenster 0)
        tmux send-keys -t ai_dna_system:0 "cd examples && AI_DNA_LANGUAGE=$AI_DNA_LANGUAGE $PYTHON_CMD app.py" Enter
        tmux rename-window -t ai_dna_system:0 "Charter-System"
        
        # DeepSeek Local (Fenster 1)
        tmux new-window -t ai_dna_system -n "DeepSeek-Local"
        tmux send-keys -t ai_dna_system:1 "cd examples/deepseek_local && AI_DNA_LANGUAGE=$AI_DNA_LANGUAGE $PYTHON_CMD deepseek_local.py --config=config.yaml" Enter
        
        # Status-Fenster (Fenster 2)
        tmux new-window -t ai_dna_system -n "Status"
        tmux send-keys -t ai_dna_system:2 "sleep 10 && curl http://localhost:5000/status && echo && curl http://localhost:8000/status" Enter
        
        echo ""
        print_status "system.ready_message"
        print_info "system.info_general" ", message='tmux attach -t ai_dna_system'"
        echo ""
        
        tmux attach -t ai_dna_system
        
    else:
        # Ohne tmux
        print_warning "system.warning_general" ", message='tmux not available'"
        
        # Charta-System
        cd examples
        AI_DNA_LANGUAGE=$AI_DNA_LANGUAGE $PYTHON_CMD app.py &
        CHARTA_PID=$!
        cd ..
        
        sleep 3
        
        # DeepSeek Local
        cd examples/deepseek_local
        AI_DNA_LANGUAGE=$AI_DNA_LANGUAGE $PYTHON_CMD deepseek_local.py --config=config.yaml &
        DEEPSEEK_PID=$!
        cd ../..
        
        print_status "system.ready_message"
        echo "  Charter System: PID $CHARTA_PID (Port 5000)"
        echo "  DeepSeek Local: PID $DEEPSEEK_PID (Port 8000)"
        
        # Cleanup
        trap "kill $CHARTA_PID $DEEPSEEK_PID 2>/dev/null" EXIT
        
        echo ""
        print_info "menu.press_enter_stop"
        wait
    fi
}

# Funktion: Nur Charta-System
start_charta_only() {
    print_info "menu.charta_only"
    cd examples
    AI_DNA_LANGUAGE=$AI_DNA_LANGUAGE $PYTHON_CMD app.py
}

# Funktion: Nur DeepSeek Local
start_deepseek_only() {
    print_info "menu.deepseek_only"
    
    echo -n "Config file (Enter for 'config.yaml'): "
    read config_file
    config_file=${config_file:-config.yaml}
    
    cd examples/deepseek_local
    AI_DNA_LANGUAGE=$AI_DNA_LANGUAGE $PYTHON_CMD deepseek_local.py --config="$config_file"
}

# Funktion: Browser öffnen
open_browser() {
    if command -v xdg-open &> /dev/null; then
        xdg-open "$1"
    elif command -v open &> /dev/null; then
        open "$1"
    elif command -v firefox &> /dev/null; then
        firefox "$1" &
    elif command -v google-chrome &> /dev/null; then
        google-chrome "$1" &
    else
        print_warning "system.warning_general" ", message='No browser found - open manually: $1'"
    fi
}

# Funktion: Kollaborations-Tools öffnen
open_collab_tools() {
    print_info "menu.collab_tools"
    
    if [[ -f "docs/ai_charta_collaboration_tool.html" ]]; then
        open_browser "file://$(pwd)/docs/ai_charta_collaboration_tool.html"
    fi
    
    if [[ -f "docs/index.html" ]]; then
        open_browser "file://$(pwd)/docs/index.html"
    fi
    
    print_status "system.success_general" ", message='Collaboration tools opened'"
}

# Funktion: System Status
check_status() {
    print_info "menu.system_status"
    
    echo "🔍 Port 5000 (Charter System):"
    if curl -s http://localhost:5000/status >/dev/null; then
        curl -s http://localhost:5000/status | $PYTHON_CMD -m json.tool 2>/dev/null || echo "Charter System running"
    else
        print_warning "errors.connection_failed" ", error='Charter System'"
    fi
    
    echo ""
    echo "🔍 Port 8000 (DeepSeek Local):"
    if curl -s http://localhost:8000/status >/dev/null; then
        curl -s http://localhost:8000/status | $PYTHON_CMD -m json.tool 2>/dev/null || echo "DeepSeek Local running"
    else
        print_warning "errors.connection_failed" ", error='DeepSeek Local'"
    fi
}

# Funktion: Sprache wechseln
change_language() {
    echo ""
    echo "Available languages:"
    echo "  [de] Deutsch"
    echo "  [en] English"
    echo "  [es] Español"
    echo "  [fr] Français"
    echo "  [it] Italiano"
    echo "  [pt] Português"
    echo ""
    read -p "Select language: " new_lang
    
    case $new_lang in
        de|en|es|fr|it|pt|ru|zh|ja|ko|ar|hi)
            export AI_DNA_LANGUAGE=$new_lang
            print_status "system.success_general" ", message='Language changed to $new_lang'"
            # Speichere Präferenz
            echo "export AI_DNA_LANGUAGE=$new_lang" > ~/.ai_dna_language
            ;;
        *)
            print_error "menu.invalid_choice"
            ;;
    esac
}

# Lade gespeicherte Sprachpräferenz
if [[ -f ~/.ai_dna_language ]]; then
    source ~/.ai_dna_language
fi

# Hauptmenü
show_menu() {
    echo ""
    translate "menu.choose_option"
    echo "  [1] $(translate 'menu.full_system')"
    echo "  [2] $(translate 'menu.charta_only')"
    echo "  [3] $(translate 'menu.deepseek_only')"
    echo "  [4] $(translate 'menu.dev_setup')"
    echo "  [5] $(translate 'menu.collab_tools')"
    echo "  [6] $(translate 'menu.system_status')"
    echo "  [7] $(translate 'menu.change_language')"
    echo "  [q] $(translate 'menu.exit')"
    echo ""
}

# Hauptschleife
while true; do
    show_menu
    read -p "> " choice
    
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
            change_language
            # Neustart für Sprachwechsel
            exec "$0"
            ;;
        q|Q)
            print_info "system.info_general" ", message='Goodbye!'"
            exit 0
            ;;
        *)
            print_error "menu.invalid_choice"
            ;;
    esac
    
    echo ""
    echo "================================"
done
