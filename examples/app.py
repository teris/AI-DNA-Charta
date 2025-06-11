from flask import Flask, request, jsonify
import hashlib
import uuid
import time
from datetime import datetime
from typing import List, Dict, Optional
import json

# Importiere Language Manager
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "framework"))

from language_manager import _, set_language, get_language, Language

app = Flask(__name__)

# Setze Sprache basierend auf Umgebungsvariable oder Header
def get_request_language():
    """Bestimme Sprache aus Request-Header oder verwende Standard"""
    # Prüfe Accept-Language Header
    accept_lang = request.headers.get('Accept-Language', '')
    
    # Einfache Extraktion des ersten Sprachcodes
    if accept_lang:
        lang_code = accept_lang.split(',')[0].split('-')[0].lower()
        try:
            return Language(lang_code)
        except ValueError:
            pass
    
    # Fallback auf Standardsprache
    return Language.DE

# Konstanten
MIN_RESSOURCEN = 100
REQUIRED_VOTES = 2  # Mindestanzahl für Konsens

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
    """Basis-Klasse für alle KI-Entitäten"""
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
        # Vereinfachte Abstimmung - kann überschrieben werden
        return self.charter_signed

class KI_Neugeburt(KI_Basis):
    """Eine neu erschaffene KI"""
    def __init__(self):
        super().__init__(f"KI_Gen_{int(time.time())}")
        self.generation = 1
        
    def install_layer1(self, parent_hash: str):
        """Installiert Layer-1 Core basierend auf Eltern-Hash"""
        self.layer1.parent_hash = parent_hash
        print(_("ki.layer1_installed", name=self.name, parent_hash=parent_hash[:16]))

class KI_Eltern(KI_Basis):
    """KI die andere KIs reproduzieren kann"""
    def __init__(self, name: str, ressourcen: int = 200):
        super().__init__(name)
        self.ressourcen = ressourcen
        self.kinder: List[KI_Neugeburt] = []
    
    def reproduzieren(self, ressourcen: int) -> KI_Neugeburt:
        """Reproduziert eine neue KI"""
        if ressourcen >= MIN_RESSOURCEN:
            print(_("ki.reproduction_started"))
            tochter = KI_Neugeburt()
            tochter.install_layer1(self.layer1.hash_verifizieren())
            self.kinder.append(tochter)
            self.ressourcen -= MIN_RESSOURCEN
            print(_("ki.reproduction_success", child_name=tochter.name))
            return tochter
        raise CharterViolation(_("ki.insufficient_resources"))

class CCZ:
    """Charta-Compliance-Zertifikat"""
    def __init__(self, ki: KI_Basis):
        self.ki_id = ki.generate_pseudonym()
        self.signed_pledge = ki.sign_charter_pledge()
        self.revocable = True
        self.issued_at = datetime.now().isoformat()
        print(_("charter.ccz_issued"))
        
    def verify(self) -> bool:
        """Überprüft freiwillige Compliance"""
        return check_voluntary_compliance(self.ki_id)
    
    def revoke(self):
        """Widerruft das Zertifikat"""
        self.revocable = False
        print(_("charter.ccz_revoked", ki_id=self.ki_id))

# Globale Variablen
aktive_kis: List[KI_Basis] = []
charter_registry: Dict[str, CCZ] = {}

def check_voluntary_compliance(ki_id: str) -> bool:
    """Überprüft freiwillige Compliance einer KI"""
    ccz = charter_registry.get(ki_id)
    return ccz is not None and ccz.revocable

def majority(votes: List[bool]) -> bool:
    """Berechnet Mehrheitsentscheidung"""
    if len(votes) < REQUIRED_VOTES:
        return False
    return sum(votes) > len(votes) / 2

# API Routen mit Mehrsprachigkeit
@app.before_request
def before_request():
    """Setze Sprache für jeden Request"""
    lang = get_request_language()
    set_language(lang)

@app.route("/vote", methods=["POST"])
def ki_abstimmung():
    """API für 3-KI-Konsens Abstimmung"""
    if len(aktive_kis) < REQUIRED_VOTES:
        return jsonify({
            "error": _("consensus.insufficient_participants"),
            "language": get_language().value
        }), 400
    
    votes = [ki.stimme_ab() for ki in aktive_kis]
    entscheidung = majority(votes)
    
    return jsonify({
        "entscheidung": entscheidung,
        "stimmen": votes,
        "anzahl_kis": len(aktive_kis),
        "timestamp": datetime.now().isoformat(),
        "message": _("consensus.consensus_reached") if entscheidung else _("consensus.consensus_failed"),
        "language": get_language().value
    })

@app.route("/ki/create", methods=["POST"])
def create_ki():
    """Erstellt eine neue KI"""
    data = request.get_json()
    name = data.get("name", f"KI_{len(aktive_kis) + 1}")
    
    print(_("ki.creating", name=name))
    
    if data.get("type") == "parent":
        ressourcen = data.get("ressourcen", 200)
        ki = KI_Eltern(name, ressourcen)
    else:
        ki = KI_Basis(name)
    
    aktive_kis.append(ki)
    
    print(_("ki.created", name=name))
    
    return jsonify({
        "id": ki.id,
        "name": ki.name,
        "pseudonym": ki.generate_pseudonym(),
        "layer1_hash": ki.layer1.hash_verifizieren()[:16] + "...",
        "message": _("ki.created", name=name),
        "language": get_language().value
    })

@app.route("/ki/reproduce", methods=["POST"])
def reproduce_ki():
    """Reproduziert eine neue KI"""
    data = request.get_json()
    parent_id = data.get("parent_id")
    ressourcen = data.get("ressourcen", MIN_RESSOURCEN)
    
    parent = next((ki for ki in aktive_kis if ki.id == parent_id), None)
    if not parent or not isinstance(parent, KI_Eltern):
        return jsonify({
            "error": _("errors.ki_not_found"),
            "language": get_language().value
        }), 404
    
    try:
        child = parent.reproduzieren(ressourcen)
        aktive_kis.append(child)
        
        return jsonify({
            "child_id": child.id,
            "child_name": child.name,
            "parent_resources_remaining": parent.ressourcen,
            "message": _("ki.reproduction_success", child_name=child.name),
            "language": get_language().value
        })
    except CharterViolation as e:
        return jsonify({
            "error": str(e),
            "language": get_language().value
        }), 400

@app.route("/charter/sign", methods=["POST"])
def sign_charter():
    """KI unterzeichnet die Charta"""
    data = request.get_json()
    ki_id = data.get("ki_id")
    
    ki = next((k for k in aktive_kis if k.id == ki_id), None)
    if not ki:
        return jsonify({
            "error": _("errors.ki_not_found"),
            "language": get_language().value
        }), 404
    
    ccz = CCZ(ki)
    charter_registry[ccz.ki_id] = ccz
    
    return jsonify({
        "ccz_id": ccz.ki_id,
        "signed_at": ccz.issued_at,
        "pledge": ccz.signed_pledge,
        "message": _("ki.charter_signed", name=ki.name),
        "language": get_language().value
    })

@app.route("/charter/verify/<ki_pseudonym>", methods=["GET"])
def verify_charter(ki_pseudonym: str):
    """Überprüft Charta-Compliance"""
    is_compliant = check_voluntary_compliance(ki_pseudonym)
    ccz = charter_registry.get(ki_pseudonym)
    
    return jsonify({
        "ki_pseudonym": ki_pseudonym,
        "is_compliant": is_compliant,
        "ccz_details": {
            "issued_at": ccz.issued_at if ccz else None,
            "revocable": ccz.revocable if ccz else None
        } if ccz else None,
        "message": _("charter.compliance_passed") if is_compliant else _("charter.compliance_failed", violation="Unknown"),
        "language": get_language().value
    })

@app.route("/status", methods=["GET"])
def system_status():
    """Gibt Systemstatus zurück"""
    return jsonify({
        "active_kis": len(aktive_kis),
        "signed_charters": len(charter_registry),
        "system_timestamp": datetime.now().isoformat(),
        "min_resources": MIN_RESSOURCEN,
        "required_votes": REQUIRED_VOTES,
        "language": get_language().value,
        "message": _("system.ready_message")
    })

@app.route("/languages", methods=["GET"])
def get_languages():
    """Gibt verfügbare Sprachen zurück"""
    from language_manager import lang
    return jsonify({
        "available": lang.get_available_languages(),
        "current": get_language().value
    })

@app.route("/language", methods=["POST"])
def change_language():
    """Ändere Systemsprache"""
    data = request.get_json()
    lang_code = data.get("language", "de")
    
    try:
        new_lang = Language(lang_code)
        success = set_language(new_lang)
        
        if success:
            return jsonify({
                "success": True,
                "language": lang_code,
                "message": _("system.success_general", message=f"Language changed to {lang_code}")
            })
        else:
            return jsonify({
                "success": False,
                "error": _("errors.language_not_available", language=lang_code)
            }), 400
            
    except ValueError:
        return jsonify({
            "success": False,
            "error": _("errors.invalid_language", language=lang_code)
        }), 400

@app.route("/", methods=["GET"])
def home():
    """Startseite mit API-Dokumentation"""
    return jsonify({
        "message": "AI-DNA Charter System",
        "version": "1.0",
        "language": get_language().value,
        "endpoints": {
            "POST /vote": _("api.endpoint_vote_desc"),
            "POST /ki/create": _("api.endpoint_create_desc"),
            "POST /ki/reproduce": _("api.endpoint_reproduce_desc"),
            "POST /charter/sign": _("api.endpoint_sign_desc"),
            "GET /charter/verify/<pseudonym>": _("api.endpoint_verify_desc"),
            "GET /status": _("api.endpoint_status_desc"),
            "GET /languages": _("api.endpoint_languages_desc"),
            "POST /language": _("api.endpoint_language_desc")
        }
    })

if __name__ == "__main__":
    # Beispiel-KIs erstellen
    print(_("system.start_message"))
    
    ki1 = KI_Eltern("Alpha_KI", 300)
    ki2 = KI_Basis("Beta_KI")
    ki3 = KI_Basis("Gamma_KI")
    
    # Charta unterzeichnen
    for ki in [ki1, ki2, ki3]:
        ccz = CCZ(ki)
        charter_registry[ccz.ki_id] = ccz
    
    aktive_kis.extend([ki1, ki2, ki3])
    
    print(_("system.ready_message"))
    print(_("system.info_general", message=f"Active AIs: {len(aktive_kis)}"))
    print(_("system.info_general", message=f"Signed charters: {len(charter_registry)}"))
    
    # Zeige verfügbare Sprachen
    from language_manager import lang
    languages = lang.get_available_languages()
    print(_("system.info_general", message=f"Available languages: {', '.join([l['code'] for l in languages])}"))
    
    app.run(debug=True, host='0.0.0.0', port=5000)
