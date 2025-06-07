class VoDiCoPrins:
    @staticmethod
    def generate_badge(ki):
        if ki.voluntary_compliance:
            return f"VoDiCoPrins-Certified-{ki.pseudonym}"
        return "Independent-Agent"
