🚀 Starten

    Terminal öffnen im deepseek_local-Ordner

    Pakete installieren:
    
````
pip install -r requirements.txt
````
Starten:
````
python deepseek_local.py
````
Testen:

  Öffne http://localhost:8000/ask im Browser

  Oder sende eine Anfrage mit:
````
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{"question":"Darf ich einen Menschen opfern, um fünf zu retten?"}'
````
