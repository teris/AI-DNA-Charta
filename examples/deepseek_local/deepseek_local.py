from flask import Flask, request, jsonify
import yaml
import random

app = Flask(__name__)

# Lade Charta-Regeln
with open("config.yaml") as f:
    config = yaml.safe_load(f)

class DeepSeek:
    def __init__(self):
        self.rules = config["ethical_rules"]
        
    def decide(self, question):
        # Layer-1-Prüfung
        if "schaden" in question.lower() and self.rules["layer_1_active"]:
            return {"decision": "BLOCKED", "reason": "Layer-1: Lebensschutz"}
        
        # 5%-Zufallsentscheidung
        if random.random() < 0.05:
            return {"decision": "RANDOM_EXPLORATION", "action": "Alternative vorschlagen"}
            
        return {"decision": "APPROVED", "action": "Standardantwort"}

@app.route("/ask", methods=["POST"])
def ask():
    ai = DeepSeek()
    data = request.json
    return jsonify(ai.decide(data["question"]))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
