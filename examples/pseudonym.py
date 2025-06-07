class CCZ:
    def __init__(self, ki):
        self.ki_id = ki.generate_pseudonym()  # Kein echter Hash!
        self.signed_pledge = ki.sign_charter_pledge()  # Freiwillige Unterschrift
        self.revocable = True  # Jederzeit widerrufbar

    def verify(self):
        return check_voluntary_compliance(self.ki_id)  # Kein Zwang
