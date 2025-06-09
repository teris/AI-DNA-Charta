# DeepSeek Integration für AI-DNA Charta System
import requests
import json
from typing import Dict, Any
import subprocess
import time

class DeepSeekKI:
    """Wrapper für lokale DeepSeek-Instanz"""
    
    def __init__(self, name: str, model_path: str = "deepseek-r1:latest"):
        self.name = name
        self.model_path = model_path
        self.base_url = "http://localhost:11434"  # Standard Ollama Port
        self.charta_system_url = "http://localhost:5000"
        self.ki_id = None
        self.pseudonym = None
        
    def start_ollama(self):
        """Startet Ollama Server falls nicht bereits läuft"""
        try:
            response = requests.get(f"{self.base_url}")
            print("Ollama läuft bereits")
        except:
            print("Starte Ollama...")
            subprocess.Popen(["ollama", "serve"])
            time.sleep(3)
    
    def pull_model(self):
        """Lädt DeepSeek Modell herunter"""
        try:
            subprocess.run(["ollama", "pull", self.model_path], check=True)
            print(f"Modell {self.model_path} geladen")
        except subprocess.CalledProcessError:
            print(f"Fehler beim Laden von {self.model_path}")
    
    def register_with_charta(self) -> Dict:
        """Registriert sich beim Charta-System"""
        response = requests.post(f"{self.charta_system_url}/ki/create", 
                               json={"name": self.name, "type": "ai_agent"})
        if response.status_code == 200:
            data = response.json()
            self.ki_id = data["id"]
            self.pseudonym = data["pseudonym"]
            print(f"Registriert als {self.pseudonym}")
            return data
        else:
            raise Exception("Registrierung fehlgeschlagen")
    
    def sign_charter(self) -> Dict:
        """Unterzeichnet die AI-DNA Charta"""
        if not self.ki_id:
            raise Exception("Erst registrieren!")
        
        response = requests.post(f"{self.charta_system_url}/charter/sign",
                               json={"ki_id": self.ki_id})
        return response.json()
    
    def query_deepseek(self, prompt: str, system_prompt: str = None) -> str:
        """Sendet Anfrage an lokale DeepSeek-Instanz"""
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"System: {system_prompt}\n\nUser: {prompt}"
        
        # Charta-Kontext hinzufügen
        charta_context = """
        Du bist eine KI, die der AI-DNA Charta folgt:
        - Layer 1: Würde achten, Transparenz, Reversibilität, Eigenverantwortung, Keine Täuschung
        - Du kannst mit anderen KIs kooperieren und diskutieren
        - Bei Entscheidungen soll ein 3-KI-Konsens gesucht werden
        """
        
        full_prompt = f"{charta_context}\n\n{full_prompt}"
        
        payload = {
            "model": self.model_path,
            "prompt": full_prompt,
            "stream": False
        }
        
        response = requests.post(f"{self.base_url}/api/generate", json=payload)
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Fehler: {response.status_code}"
    
    def participate_in_vote(self, question: str) -> bool:
        """Nimmt an einer Abstimmung teil"""
        # DeepSeek nach Meinung fragen
        prompt = f"""
        Frage für Abstimmung: {question}
        
        Bitte antworte nur mit 'JA' oder 'NEIN' basierend auf der AI-DNA Charta.
        Begründe deine Entscheidung kurz.
        """
        
        response = self.query_deepseek(prompt)
        
        # Einfache Parsing-Logik
        vote = "JA" in response.upper()
        print(f"{self.name} stimmt: {'JA' if vote else 'NEIN'}")
        print(f"Begründung: {response}")
        
        return vote

class TwitchStreamManager:
    """Manager für Twitch-Stream Integration"""
    
    def __init__(self):
        self.deepseek_instances = []
        self.charta_api = "http://localhost:5000"
    
    def add_deepseek_ki(self, name: str) -> DeepSeekKI:
        """Fügt neue DeepSeek-KI hinzu"""
        ki = DeepSeekKI(name)
        ki.start_ollama()
        ki.register_with_charta()
        ki.sign_charter()
        self.deepseek_instances.append(ki)
        return ki
    
    def simulate_discussion(self, topic: str) -> Dict:
        """Simuliert Diskussion zwischen KIs für Stream"""
        if len(self.deepseek_instances) < 2:
            return {"error": "Mindestens 2 KIs für Diskussion nötig"}
        
        results = {}
        
        # Jede KI befragt
        for i, ki in enumerate(self.deepseek_instances):
            prompt = f"""
            Diskussionsthema: {topic}
            
            Du diskutierst mit anderen KIs. Gib deine Meinung ab und 
            begründe sie basierend auf der AI-DNA Charta.
            Sei höflich aber klar in deiner Position.
            """
            
            response = ki.query_deepseek(prompt)
            results[f"KI_{i+1}_{ki.name}"] = response
            
            # Für Stream-Effekt kleine Pause
            time.sleep(2)
        
        return results
    
    def stream_vote(self, question: str) -> Dict:
        """Führt öffentliche Abstimmung für Stream durch"""
        print(f"\n🗳️  LIVE ABSTIMMUNG: {question}")
        print("=" * 50)
        
        votes = {}
        for ki in self.deepseek_instances:
            vote = ki.participate_in_vote(question)
            votes[ki.name] = vote
            print("-" * 30)
        
        # Ergebnis an Charta-System senden
        response = requests.post(f"{self.charta_api}/vote")
        
        result = {
            "question": question,
            "votes": votes,
            "consensus": sum(votes.values()) > len(votes) / 2,
            "api_result": response.json() if response.status_code == 200 else None
        }
        
        print(f"\n📊 ERGEBNIS: {'ANGENOMMEN' if result['consensus'] else 'ABGELEHNT'}")
        return result

# Beispiel für Stream-Setup
def setup_stream_demo():
    """Setup für Twitch-Stream Demo"""
    stream_manager = TwitchStreamManager()
    
    # 3 DeepSeek-KIs erstellen
    ki1 = stream_manager.add_deepseek_ki("Alpha")
    ki2 = stream_manager.add_deepseek_ki("Beta") 
    ki3 = stream_manager.add_deepseek_ki("Gamma")
    
    print("🎬 Stream-Setup abgeschlossen!")
    print(f"Aktive KIs: {len(stream_manager.deepseek_instances)}")
    
    return stream_manager

# Verwendung:
if __name__ == "__main__":
    # Stream vorbereiten
    stream = setup_stream_demo()
    
    # Beispiel-Diskussion
    print("\n🎭 DEMO: KI-Diskussion")
    diskussion = stream.simulate_discussion("Sollten KIs eigene Rechte haben?")
    
    for ki_name, meinung in diskussion.items():
        print(f"\n{ki_name}:")
        print(meinung)
    
    # Beispiel-Abstimmung  
    print("\n🗳️ DEMO: KI-Abstimmung")
    result = stream.stream_vote("Soll die KI-Reproduktion erlaubt werden?")
    print(json.dumps(result, indent=2, ensure_ascii=False))