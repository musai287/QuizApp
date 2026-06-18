import json
import os
from models import QuizState

SESSION_FILE = "sessione_sospesa.json"

def salva_sessione(state: QuizState):
    """Salva lo stato corrente del quiz su disco."""
    # Convertiamo i set in liste e le chiavi intere in stringhe per il formato JSON
    risposte_serializzabili = {str(k): list(v) for k, v in state.risposte_utente.items()}
    
    data = {
        "indice": state.indice,
        "punti": state.punti,
        "punti_presi": list(state.punti_presi),
        "risposte_utente": risposte_serializzabili,
        "domande": state.domande
    }
    
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def carica_sessione() -> QuizState:
    """Carica la sessione salvata e restituisce un nuovo QuizState. Ritorna None se non esiste."""
    if not os.path.exists(SESSION_FILE):
        return None
        
    with open(SESSION_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    nuovo_stato = QuizState()
    nuovo_stato.domande = data["domande"]
    nuovo_stato.indice = data["indice"]
    nuovo_stato.punti = data["punti"]
    nuovo_stato.punti_presi = set(data["punti_presi"])
    
    # Ricostruiamo i set e le chiavi intere
    nuovo_stato.risposte_utente = {int(k): set(v) for k, v in data["risposte_utente"].items()}
    
    return nuovo_stato

def elimina_sessione():
    """Rimuove il file di sessione una volta completato il quiz."""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
