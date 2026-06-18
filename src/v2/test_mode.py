import json
import os
import random
from models import QuizState

def genera_test_casuale(cartella_dati="data", num_domande=12) -> QuizState:
    """Estrae un numero definito di domande casuali da tutti i file JSON disponibili."""
    tutte_le_domande = []
    
    # Costruiamo il percorso assoluto alla cartella data partendo da dove lanci lo script
    base_path = os.path.abspath(cartella_dati)
    
    if not os.path.exists(base_path):
        raise FileNotFoundError(f"Cartella dati non trovata: {base_path}")

    # Leggiamo tutti i JSON
    for filename in os.listdir(base_path):
        if filename.endswith(".json"):
            filepath = os.path.join(base_path, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    domande_file = json.load(f)
                    tutte_le_domande.extend(domande_file)
            except Exception as e:
                print(f"Errore lettura {filename}: {e}")

    # Rimuoviamo eventuali duplicati usando il testo della domanda come chiave
    domande_uniche = []
    testi_visti = set()
    for d in tutte_le_domande:
        testo = d.get("domanda", "").strip()
        if testo and testo not in testi_visti:
            domande_uniche.append(d)
            testi_visti.add(testo)

    # Selezioniamo le domande (o tutte se sono meno di 12)
    if len(domande_uniche) > num_domande:
        domande_scelte = random.sample(domande_uniche, num_domande)
    else:
        domande_scelte = domande_uniche
        random.shuffle(domande_scelte)

    nuovo_stato = QuizState()
    nuovo_stato.domande = domande_scelte
    
     # INIZIALIZZA I CONTENITORI VUOTI PER EVITARE IL KEYERROR
    nuovo_stato.risposte_utente = {i: set() for i in range(len(domande_scelte))}
    nuovo_stato.punti_presi = set()
    nuovo_stato.punti = 0
    nuovo_stato.indice = 0
    
    return nuovo_stato
