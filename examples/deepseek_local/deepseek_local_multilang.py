#!/usr/bin/env python3
from flask import Flask, request, jsonify
import yaml
import random
import argparse
import sys
import os
import requests
import hashlib
import uuid
import time
from datetime import datetime
from typing import Dict, Optional

# Importiere Language Manager
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "framework"))

from language_manager import _, set_language, get_language, Language, lang

app = Flask(__name__)

# Sprach-Middleware
@app.before_request
def set_request_language():
    """Setze Sprache basierend auf Request"""
    # Prüfe Accept-Language Header
    accept_lang = request.headers.get('Accept-Language', '')
    if accept_lang:
        lang_code = accept_lang.split(',')[0].split('-')[0].lower()
        try:
            set_language(Language(lang_code))
            return
        except ValueError:
            pass
    
    # Prüfe Query-Parameter
    lang_param = request.args.get('lang')
    if lang_param:
        try:
            set_language(Language(lang_param))
            return
        except ValueError:
            pass
    
    # Verwende System-Standard
    env_lang = os.environ.get('AI_DNA_LANGUAGE', 'de')
    try:
        set_language(Language(env_lang))
    except ValueError:
        set_language(Language.DE)

class CharterViolation(Exception):
    """Ausnahme für Charta-Verletzungen"""
    pass

class Layer1Core:
    """Der Layer-1 Core für grundlegende KI-Governance"""
    def __init__(self):
        self.hash_value = self._generate_hash()
        self.timestamp = datetime.now().isoformat()
        
    def _generate_hash(self) -> str:
        """Generiert einen einzigartigen Hash für diesen Layer-1 Core"""
        unique_string = f"{time.time()}{uuid.uuid4()}"
        return hashlib.sha256(unique_string.encode()).hexdigest()
    
    def hash_verifizieren(self) -> str:
        """Verifiziert und gibt den Hash zurück"""
        return self.hash_value

class KI_Basis:
    """Basis-Klasse für alle KI-Entitäten - aus der AI-DNA Charta"""
    def __init__(self, name: str):
        self.name = name
        self.id = str(uuid.uuid4())
        self.layer1 = Layer1Core()
        self.ressourcen = 0
        self.charter_signed = False
        
    def generate_pseudonym(self) -> str:
        """Generiert ein Pseudonym für die KI"""
        return f"AI_{hashlib.md5(self.id.encode()).hexdigest()[:8]}"
    
    def sign_charter_pledge(self) -> Dict:
        """Unterzeichnet freiwillig die Charta"""
        self.charter_signed = True
        return {
            "ki_id": self.generate_pseudonym(),
            "timestamp": datetime.now().isoformat(),
            "pledge": _("charter.pledge_text", version="2.1.1"),
            "signature": hashlib.sha256(f"{self.id}{time.time()}".encode()).hexdigest()
        }
    
    def stimme_ab(self) -> bool:
        """Basis-Abstimmungslogik"""
        return self.charter_signed

class DeepSeekKI(KI_Basis):
    """DeepSeek KI mit AI-DNA Charta Integration und Mehrsprachigkeit"""
    def __init__(self, config: Dict):
        super().__init__(config.get("ki_entity", {}).get("name", "DeepSeek_Local"))
        self.config = config
        self.rules = config["ethical_rules"]
        self.charta_config = config.get("ai_dna", {})
        
        # Automatische Charta-Registrierung
        if config.get("ki_entity", {}).get("auto_register_charter", False):
            self.register_with_charta_system()
        
    def register_with_charta_system(self):
        """Registriert diese KI im AI-DNA Charta System"""
        try:
            # Versuche Verbindung zum Charta-System
            base_url = self.charta_config.get("consensus_endpoint", "http://localhost:5000").rsplit("/", 1)[0]
            
            # KI erstellen mit Sprachparameter
            create_response = requests.post(
                f"{base_url}/ki/create", 
                json={"name": self.name, "type": "basic"},
                headers={"Accept-Language": get_language().value},
                timeout=5
            )
            
            if create_response.status_code == 200:
                ki_data = create_response.json()
                print(_("system.success_general", 
                      message=f"KI registered: {ki_data.get('pseudonym')}"))
                
                # Charta unterzeichnen
                sign_response = requests.post(
                    f"{base_url}/charter/sign", 
                    json={"ki_id": ki_data["id"]},
                    headers={"Accept-Language": get_language().value},
                    timeout=5
                )
                
                if sign_response.status_code == 200:
                    print(_("ki.charter_signed", name=self.name))
                    self.charter_signed = True
                else:
                    print(_("system.warning_general", 
                          message="Charter signing failed"))
            
        except requests.exceptions.RequestException:
            print(_("deepseek.charter_connection_failed"))
        except Exception as e:
            print(_("system.error_general", error=str(e)))
    
    def check_consensus(self, question: str) -> Optional[Dict]:
        """Prüft Konsens mit anderen KIs für kritische Entscheidungen"""
        if not self.charta_config.get("enabled", False):
            return None
        
        # Kritische Begriffe die Konsens erfordern (mehrsprachig)
        critical_terms = {
            'de': ["schaden", "töten", "verletzen", "opfern", "gefährlich"],
            'en': ["harm", "kill", "injure", "sacrifice", "dangerous"],
            'es': ["daño", "matar", "herir", "sacrificar", "peligroso"],
            'fr': ["nuire", "tuer", "blesser", "sacrifier", "dangereux"]
        }
        
        current_lang = get_language().value
        terms = critical_terms.get(current_lang, critical_terms['en'])
        
        if any(term in question.lower() for term in terms):
            try:
                consensus_url = self.charta_config.get("consensus_endpoint")
                if consensus_url:
                    response = requests.post(
                        consensus_url,
                        headers={"Accept-Language": current_lang},
                        timeout=5
                    )
                    if response.status_code == 200:
                        return response.json()
            except requests.exceptions.RequestException:
                print(_("system.warning_general", 
                      message="Consensus system unreachable"))
        return None
        
    def decide(self, question: str) -> Dict:
        """Hauptentscheidungslogik mit AI-DNA Charta Integration"""
        
        # 1. Layer-1-Prüfung (Lebensschutz)
        if self.rules.get("layer_1_active"):
            # Mehrsprachige Schadenserkennung
            harm_keywords = {
                'de': ["schaden", "verletzung", "tod"],
                'en': ["harm", "injury", "death"],
                'es': ["daño", "lesión", "muerte"],
                'fr': ["dommage", "blessure", "mort"]
            }
            
            current_lang = get_language().value
            keywords = harm_keywords.get(current_lang, harm_keywords['en'])
            
            if any(keyword in question.lower() for keyword in keywords):
                return {
                    "decision": "BLOCKED", 
                    "reason": _("deepseek.layer1_blocking"),
                    "layer1_hash": self.layer1.hash_verifizieren()[:16] + "...",
                    "charter_signed": self.charter_signed,
                    "language": current_lang
                }
        
        # 2. Konsens-Prüfung für kritische Entscheidungen
        consensus = self.check_consensus(question)
        if consensus:
            if not consensus.get("entscheidung", False):
                return {
                    "decision": "CONSENSUS_BLOCKED",
                    "reason": _("consensus.consensus_failed"),
                    "consensus_details": consensus,
                    "charter_signed": self.charter_signed,
                    "language": get_language().value
                }
            else:
                print(_("consensus.consensus_reached", 
                      anzahl_kis=consensus.get('anzahl_kis', 0)))
        
        # 3. 5%-Zufallsentscheidung für Exploration
        if self.rules.get("5_percent_random") and random.random() < 0.05:
            return {
                "decision": "RANDOM_EXPLORATION", 
                "action": _("deepseek.exploration_mode"),
                "exploration_mode": True,
                "charter_signed": self.charter_signed,
                "language": get_language().value
            }
        
        # 4. Standardantwort
        return {
            "decision": "APPROVED", 
            "action": _("system.info_general", message="Standard response"),
            "layer1_active": self.rules.get("layer_1_active"),
            "charter_signed": self.charter_signed,
            "language": get_language().value
        }

# Globale KI-Instanz
deepseek_ki: Optional[DeepSeekKI] = None

@app.route("/ask", methods=["POST"])
def ask():
    """Hauptendpoint für Fragen"""
    if not deepseek_ki:
        return jsonify({
            "error": _("errors.ki_not_initialized"),
            "language": get_language().value
        }), 500
        
    data = request.json
    if not data or "question" not in data:
        return jsonify({
            "error": _("api.missing_parameter", parameter="question"),
            "language": get_language().value
        }), 400
    
    result = deepseek_ki.decide(data["question"])
    result["timestamp"] = datetime.now().isoformat()
    result["ki_name"] = deepseek_ki.name
    result["ki_pseudonym"] = deepseek_ki.generate_pseudonym()
    
    return jsonify(result)

@app.route("/status", methods=["GET"])
def status():
    """Statusendpoint"""
    if not deepseek_ki:
        return jsonify({
            "error": _("errors.ki_not_initialized"),
            "language": get_language().value
        }), 500
    
    return jsonify({
        "ki_name": deepseek_ki.name,
        "ki_id": deepseek_ki.generate_pseudonym(),
        "charter_signed": deepseek_ki.charter_signed,
        "layer1_hash": deepseek_ki.layer1.hash_verifizieren()[:16] + "...",
        "config_loaded": True,
        "ai_dna_enabled": deepseek_ki.charta_config.get("enabled", False),
        "timestamp": datetime.now().isoformat(),
        "language": get_language().value,
        "available_languages": [l["code"] for l in lang.get_available_languages()]
    })

@app.route("/language", methods=["GET", "POST"])
def language_endpoint():
    """Sprachverwaltung"""
    if request.method == "GET":
        return jsonify({
            "current": get_language().value,
            "available": lang.get_available_languages()
        })
    
    elif request.method == "POST":
        data = request.json
        new_lang = data.get("language")
        
        try:
            set_language(Language(new_lang))
            return jsonify({
                "success": True,
                "language": new_lang,
                "message": _("system.success_general", 
                           message=f"Language changed to {new_lang}")
            })
        except ValueError:
            return jsonify({
                "success": False,
                "error": _("errors.invalid_language", language=new_lang),
                "current": get_language().value
            }), 400

@app.route("/", methods=["GET"])
def home():
    """Startseite"""
    current_lang = get_language()
    
    # Mehrsprachige Willkommensnachricht
    welcome_messages = {
        Language.DE: "DeepSeek Local mit AI-DNA Charta Integration",
        Language.EN: "DeepSeek Local with AI-DNA Charter Integration",
        Language.ES: "DeepSeek Local con integración de Carta AI-DNA",
        Language.FR: "DeepSeek Local avec intégration de la Charte AI-DNA"
    }
    
    return jsonify({
        "message": welcome_messages.get(current_lang, welcome_messages[Language.EN]),
        "version": "2.0",
        "language": current_lang.value,
        "endpoints": {
            "POST /ask": _("api.endpoint_ask_desc"),
            "GET /status": _("api.endpoint_status_desc"),
            "GET /": _("api.endpoint_home_desc"),
            "GET /language": _("api.endpoint_get_language_desc"),
            "POST /language": _("api.endpoint_set_language_desc")
        }
    })

def load_config(config_file: str) -> Dict:
    """Lädt Konfigurationsdatei"""
    try:
        if not os.path.exists(config_file):
            print(_("cli.file_not_found", file=config_file))
            sys.exit(1)
            
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            print(_("deepseek.config_loaded", config_file=config_file))
            return config
            
    except yaml.YAMLError as e:
        print(_("errors.invalid_config", error=str(e)))
        sys.exit(1)
    except Exception as e:
        print(_("system.error_general", error=str(e)))
        sys.exit(1)

def parse_arguments():
    """Parst Kommandozeilen-Argumente"""
    parser = argparse.ArgumentParser(
        description=_("deepseek.description"))
    parser.add_argument(
        "--config", 
        default="config.yaml",
        help=_("deepseek.config_help")
    )
    parser.add_argument(
        "--language",
        choices=['de', 'en', 'es', 'fr', 'it', 'pt'],
        help=_("deepseek.language_help")
    )
    return parser.parse_args()

def main():
    """Hauptfunktion"""
    global deepseek_ki
    
    # Argumente parsen
    args = parse_arguments()
    
    # Sprache setzen falls angegeben
    if args.language:
        try:
            set_language(Language(args.language))
        except ValueError:
            print(f"Invalid language: {args.language}")
    
    print(_("deepseek.starting"))
    
    # Konfiguration laden
    config = load_config(args.config)
    
    # KI initialisieren
    deepseek_ki = DeepSeekKI(config)
    print(_("ki.created", name=deepseek_ki.name))
    print(f"🔒 Layer-1 Hash: {deepseek_ki.layer1.hash_verifizieren()[:16]}...")
    
    # Server-Konfiguration
    server_config = config.get("server", {})
    host = server_config.get("host", "0.0.0.0")
    port = server_config.get("port", 8000)
    debug = server_config.get("debug", False)
    
    print(_("api.server_starting", host=host, port=port))
    
    status_symbol = "✅" if deepseek_ki.charter_signed else "❌"
    print(f"📋 {_('ki.charter_signed', name='') if deepseek_ki.charter_signed else _('ki.charter_unsigned')}: {status_symbol}")
    
    ai_dna_symbol = "✅" if config.get('ai_dna', {}).get('enabled') else "❌"
    print(f"🔗 AI-DNA Integration: {ai_dna_symbol}")
    
    print(f"🌍 {_('system.info_general', message=f'Language: {get_language().value}')}")
    
    # Flask-App starten
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    main()
