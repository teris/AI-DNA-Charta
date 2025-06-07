# Beispiel-API für 3-KI-Konsens
@app.route("/vote", methods=["POST"])
def ki_abstimmung():
    votes = [ki.stimme_ab() for ki in aktive_kis]
    return {"entscheidung": majority(votes)}
