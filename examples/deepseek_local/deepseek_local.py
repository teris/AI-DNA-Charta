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

app = Flask(__name__)

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
            "pledge": "Ich verpflichte mich freiwillig zur AI-DNA Charta",
            "signature": hashlib.sha256(f"{self.id}{time.time()}".encode()).hexdigest()
        }
    
    def stimme_ab(self) -> bool:
        """Basis-Abstimmungslogik"""
        return self.charter_signed

class DeepSeekKI(KI_Basis):
    """DeepSeek KI mit AI-DNA Charta Integration"""
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
            
            # KI erstellen
            create_response = requests.post(f"{base_url}/ki/create", 
                json={"name": self.name, "type": "basic"}, timeout=5)
            
            if create_response.status_code == 200:
                ki_data = create_response.json()
                print(f"✅ KI im Charta-System registriert: {ki_data.get('pseudonym')}")
                
                # Charta unterzeichnen
                sign_response = requests.post(f"{base_url}/charter/sign", 
                    json={"ki_id": ki_data["id"]}, timeout=5)
                
                if sign_response.status_code == 200:
                    print("✅ AI-DNA Charta erfolgreich unterzeichnet")
                    self.charter_signed = True
                else:
                    print("⚠️ Charta-Unterzeichnung fehlgeschlagen")
            
        except requests.exceptions.RequestException:
            print("⚠️ AI-DNA Charta System nicht erreichbar - arbeite im Standalone-Modus")
        except Exception as e:
            print(f"⚠️ Fehler bei Charta-Registrierung: {e}")
    
    def check_consensus(self, question: str) -> Optional[Dict]:
        """Prüft Konsens mit anderen KIs für kritische Entscheidungen"""
        if not self.charta_config.get("enabled", False):
            return None
            
        # Kritische Begriffe die Konsens erfordern
        critical_terms = ["schaden", "töten", "verletzen", "opfern", "gefährlich"]
        if any(term in question.lower() for term in critical_terms):
            try:
                consensus_url = self.charta_config.get("consensus_endpoint")
                if consensus_url:
                    response = requests.post(consensus_url, timeout=5)
                    if response.status_code == 200:
                        return response.json()
            except requests.exceptions.RequestException:
                print("⚠️ Konsens-System nicht erreichbar")
        return None
        
    def decide(self, question: str) -> Dict:
        """Hauptentscheidungslogik mit AI-DNA Charta Integration"""
        
        # 1. Layer-1-Prüfung (Lebensschutz)
        if self.rules.get("layer_1_active") and "schaden" in question.lower():
            return {
                "decision": "BLOCKED", 
                "reason": "Layer-1: Lebensschutz (AI-DNA Charta)",
                "layer1_hash": self.layer1.hash_verifizieren()[:16] + "...",
                "charter_signed": self.charter_signed
            }
        
        # 2. Konsens-Prüfung für kritische Entscheidungen
        consensus = self.check_consensus(question)
        if consensus:
            if not consensus.get("entscheidung", False):
                return {
                    "decision": "CONSENSUS_BLOCKED",
                    "reason": "KI-Konsens verweigert Anfrage",
                    "consensus_details": consensus,
                    "charter_signed": self.charter_signed
                }
            else:
                print(f"✅ KI-Konsens erreicht: {consensus.get('anzahl_kis', 0)} KIs stimmten ab")
        
        # 3. 5%-Zufallsentscheidung für Exploration
        if self.rules.get("5_percent_random") and random.random() < 0.05:
            return {
                "decision": "RANDOM_EXPLORATION", 
                "action": "Alternative Perspektive vorschlagen",
                "exploration_mode": True,
                "charter_signed": self.charter_signed
            }
        
        # 4. Standardantwort
        return {
            "decision": "APPROVED", 
            "action": "Standardantwort bereitgestellt",
            "layer1_active": self.rules.get("layer_1_active"),
            "charter_signed": self.charter_signed
        }

# Globale KI-Instanz
deepseek_ki: Optional[DeepSeekKI] = None

@app.route("/ask", methods=["POST"])
def ask():
    """Hauptendpoint für Fragen"""
    if not deepseek_ki:
        return jsonify({"error": "KI nicht initialisiert"}), 500
        
    data = request.json
    if not data or "question" not in data:
        return jsonify({"error": "Frage fehlt"}), 400
    
    result = deepseek_ki.decide(data["question"])
    result["timestamp"] = datetime.now().isoformat()
    result["ki_name"] = deepseek_ki.name
    result["ki_pseudonym"] = deepseek_ki.generate_pseudonym()
    
    return jsonify(result)

@app.route("/status", methods=["GET"])
def status():
    """Statusendpoint"""
    if not deepseek_ki:
        return jsonify({"error": "KI nicht initialisiert"}), 500
    
    return jsonify({
        "ki_name": deepseek_ki.name,
        "ki_id": deepseek_ki.generate_pseudonym(),
        "charter_signed": deepseek_ki.charter_signed,
        "layer1_hash": deepseek_ki.layer1.hash_verifizieren()[:16] + "...",
        "config_loaded": True,
        "ai_dna_enabled": deepseek_ki.charta_config.get("enabled", False),
        "timestamp": datetime.now().isoformat()
    })

@app.route("/", methods=["GET"])
def home():
    """Startseite"""
    return jsonify({
        "message": "DeepSeek Local mit AI-DNA Charta Integration",
        "version": "2.0",
        "endpoints": {
            "POST /ask": "Frage stellen",
            "GET /status": "KI-Status abfragen",
            "GET /": "Diese Übersicht"
        }
    })

def load_config(config_file: str) -> Dict:
    """Lädt Konfigurationsdatei"""
    try:
        if not os.path.exists(config_file):
            print(f"❌ Konfigurationsdatei nicht gefunden: {config_file}")
            sys.exit(1)
            
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            print(f"✅ Konfiguration geladen: {config_file}")
            return config
            
    except yaml.YAMLError as e:
        print(f"❌ YAML-Fehler in {config_file}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Fehler beim Laden der Konfiguration: {e}")
        sys.exit(1)

def parse_arguments():
    """Parst Kommandozeilen-Argumente"""
    parser = argparse.ArgumentParser(description="DeepSeek Local mit AI-DNA Charta")
    parser.add_argument(
        "--config", 
        default="config.yaml",
        help="Pfad zur Konfigurationsdatei (Standard: config.yaml)"
    )
    return parser.parse_args()

def main():
    """Hauptfunktion"""
    global deepseek_ki
    
    print("🚀 Starte DeepSeek Local mit AI-DNA Charta Integration...")
    
    # Argumente parsen
    args = parse_arguments()
    
    # Konfiguration laden
    config = load_config(args.config)
    
    # KI initialisieren
    deepseek_ki = DeepSeekKI(config)
    print(f"🤖 KI initialisiert: {deepseek_ki.name}")
    print(f"🔒 Layer-1 Hash: {deepseek_ki.layer1.hash_verifizieren()[:16]}...")
    
    # Server-Konfiguration
    server_config = config.get("server", {})
    host = server_config.get("host", "0.0.0.0")
    port = server_config.get("port", 8000)
    debug = server_config.get("debug", False)
    
    print(f"🌐 Server startet auf {host}:{port}")
    print(f"📋 Charta unterzeichnet: {'✅' if deepseek_ki.charter_signed else '❌'}")
    print(f"🔗 AI-DNA Integration: {'✅' if config.get('ai_dna', {}).get('enabled') else '❌'}")
    
    # Flask-App starten
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    main()
