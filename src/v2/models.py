import json

class QuizState:
    def __init__(self):
        self.domande = []
        self.indice = 0
        self.punti = 0
        self.risposte_utente = {}
        self.punti_presi = set()

    def carica_da_file(self, path):
        """Legge il JSON e resetta le variabili per un nuovo quiz"""
        with open(path, "r", encoding="utf-8") as f:
            self.domande = json.load(f)
        
        self.indice = 0
        self.punti = 0
        # Inizializza un set vuoto per ogni domanda presente nel file
        self.risposte_utente = {i: set() for i in range(len(self.domande))}
        self.punti_presi = set()