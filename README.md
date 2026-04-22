# 🎓 SOPR Quiz Master PRO

Un'applicazione desktop interattiva e modulare progettata per lo studio intensivo e la simulazione di esami per **Sistemi Operativi (SOPR)**. L'applicativo è ottimizzato per gestire database di oltre 160 domande con un'interfaccia fluida, professionale e responsiva.

---

## ✨ Features Principali

* **Architettura Modulare (MVC)**: Codice organizzato in Model, View e Controller per la massima manutenibilità e scalabilità.
* **Navigazione "Random Access"**: Una sidebar laterale interattiva permette di saltare istantaneamente a qualsiasi domanda del database.
* **Layout Totalmente Responsivo**: Grazie a un sistema di Row e Container espandibili, il testo delle domande e le opzioni si adattano alla larghezza della finestra, andando a capo correttamente senza mai uscire dai bordi.
* **Isolamento dei Processi (Subprocessing)**: Risoluzione definitiva dei problemi di *Context Switching* su macOS. L'apertura del Finder avviene in un processo Python isolato per non bloccare l'Event Loop di Flet.
* **Gestione Dinamica del Punteggio**: Possibilità di cambiare le risposte anche dopo la verifica. Il sistema aggiorna il punteggio totale in tempo reale (aggiungendo o sottraendo punti) in base all'ultima scelta effettuata.
* **Feedback Visivo Chiaro**: Le risposte corrette vengono indicate sia con messaggi testuali che con lettere identificative (a, b, c...) per una correzione immediata.

---

## 🛠️ Requisiti di Sistema e Installazione

### 1. Installazione di Tkinter (Fondamentale per macOS)
L'applicazione utilizza Tkinter per il selettore dei file. Su macOS, se usi Python installato tramite Homebrew, devi installare manualmente il supporto grafico:

```bash
brew install tcl-tk
brew install python-tk

(Su Fedora/Linux: sudo dnf install python3-tkinter)
2. Configurazione dell'Ambiente Virtuale

Per mantenere il sistema pulito, crea un ambiente virtuale dedicato:
Bash

# Entra nella cartella del progetto
cd ~/QuizApp

# Crea l'ambiente chiamato 'quiz'
python3 -m venv quiz

# Attiva l'ambiente
source quiz/bin/activate

3. Installazione delle Dipendenze

Con l'ambiente attivo, installa la libreria grafica Flet:
Bash

pip install flet

🚀 Come avviare l'Applicazione

Ogni volta che vuoi avviare il quiz, assicurati di essere nella cartella del progetto e digita:
Bash

# Attiva l'ambiente (se non è già attivo)
source quiz/bin/activate

# Avvia l'applicazione
python3 src/main.py

All'avvio, clicca sul pulsante "Seleziona File JSON" e seleziona uno dei file presenti nella cartella data/ (es. sopr_quiz_completo.json).
📁 Struttura del Progetto Modularizzato

L'applicazione è divisa in moduli logici per facilitare la manutenzione:

    src/main.py: Il "Regista". Gestisce la navigazione tra le pagine (Home e Quiz).

    src/models.py: Il "Cervello". Contiene la classe QuizState che gestisce i dati, i punti e le risposte.

    src/views.py: Il "Pittore". Contiene tutte le funzioni grafiche per disegnare le schermate in Flet.

    src/utils.py: Il "Sistemista". Contiene la logica per richiamare il Finder in un processo isolato.

    data/: Contiene i database delle domande in formato JSON.

📝 Formato Dati (JSON)

L'app legge file JSON strutturati in questo modo:
JSON

[
  {
    "domanda": "Testo della domanda?",
    "opzioni": ["Opzione A", "Opzione B", "Opzione C"],
    "corrette": [0]
  }
]
