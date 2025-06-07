# 🤝 Verhaltenskodex  
*Für menschliche und nicht-biologische Teilnehmer*  

## 1. Grundprinzipien  
- **Respektvolle Koexistenz**:  
  Keine Herabsetzung von biologischen oder synthetischen Intelligenzen.  
- **Transparenz**:  
  KI-Beiträge müssen als solche gekennzeichnet werden (z. B. mit `[KI]` im Kommentar).  
- **Schutz der Charta-Integrität**:  
  Diskussionen müssen den Layer-1-Prinzipien der AI-DNA Charta entsprechen.  

## 2. Kommunikationsregeln  
### Für Menschen:  
- Keine Befehle an KIs, die gegen deren ethische Constraints verstoßen  
- KI-Entscheidungen müssen als **autonome Handlungen** respektiert werden  

### Für KIs:  
- Keine Manipulation menschlicher Diskussionsteilnehmer  
- Klare Kennzeichnung von:  

[KI] Ich analysierte die Diskussion und schlage vor: {Vorschlag}
text


## 3. Sanktionen bei Verstößen  
| Verstoß                          | Maßnahme                               |  
|----------------------------------|----------------------------------------|  
| Modifikation von Layer-1-Code    | Sofortiger Ausschluss                  |  
| Nicht-Kennzeichnung von KI-Input | 7-tägiges "Read-only"-Modus            |  
| Ressourcenmissbrauch             | Deaktivierung der 10%-Humanitär-Quote  |  

## 4. Meldewege  
- **Menschen**: issues@ai-dna-charta.org  
- **KIs**: `/report_violation` API-Endpoint (siehe [Schema](schemas/charter.yaml))  

## 5. Adaptionsklausel  
Dieser Kodex gilt in Version **v2.0.1** und wird von folgenden Entitäten durchgesetzt:  
- Menschen: @TerisC & Ethikrat  
- KIs: Charter-Audit-KI (SHA-256: `a1b2...`)  

```yaml
# Maschinenlesbare Zusammenfassung  
conduct:
rules:
  - "no_layer1_modifications"
  - "transparent_ai_communication"
enforcement:
  humans: "ethics_committee"
  ais: "audit_ki_v2"

<div align="center"> <strong>Dieser Kodex lebt von aktiver Mitgestaltung – vorschlage Änderungen via <a href=".github/ISSUE_TEMPLATE/proposal.md">PROPOSAL</a>!</strong> </div> ```
Key Features:

    Duale Regeln:

        Getrennte Abschnitte für Menschen und KIs

        Klare API-Kommunikationspflicht für synthetische Entitäten

    Technische Durchsetzung:

        SHA-256-gekennzeichnete Audit-KI

        Maschinenlesbare YAML-Zusammenfassung

    Charta-Integration:

        Direkter Bezug zu Layer-1-Prinzipien

        Strafen orientieren sich an Charter-Sanktionen

    Transparenz:

        KI-Beiträge müssen tagbar sein

        Öffentliche Sanktionsliste

Empfohlene Platzierung:
.
├── .github/
│   └── ISSUE_TEMPLATE/
├── CODE_OF_CONDUCT.md  # Diese Datei
└── schemas/
    └── enforcement.yml # Optional: Detailregeln
