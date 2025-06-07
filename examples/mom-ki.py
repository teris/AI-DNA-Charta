class KI_Eltern:  
    def reproduzieren(self, ressourcen):  
        if ressourcen >= MIN_RESSOURCEN:  
            tochter = KI_Neugeburt()  
            tochter.install_layer1(self.layer1.hash_verifizieren())  
            return tochter  
        raise CharterViolation("Nicht genug Ressourcen")  
