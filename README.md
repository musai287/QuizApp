SOPR Quiz Master PRO

Applicazione desktop modulare progettata per lo studio e la simulazione di esami per Sistemi Operativi (SOPR). L'applicativo è progettato per gestire database di oltre 160 domande.
Features Principali

    Architettura Modulare (MVC): Codice organizzato in Model, View e Controller.

    Navigazione "Random Access": Sidebar laterale per navigare direttamente verso qualsiasi domanda del database.

    Layout Responsivo: Il testo delle domande e le opzioni si adattano dinamicamente alla larghezza della finestra.

    Isolamento dei Processi (Subprocessing): Risoluzione dei problemi di Context Switching su macOS. L'apertura del file picker avviene in un processo Python isolato per non bloccare l'Event Loop principale di Flet.

    Gestione Dinamica del Punteggio: Il sistema aggiorna il punteggio totale in tempo reale permettendo di modificare la scelta anche dopo la prima verifica.

    Feedback Visivo: Le risposte corrette vengono indicate tramite messaggi testuali e lettere identificative (a, b, c...).

Requisiti di Sistema e Installazione
1. Installazione di Tkinter (Richiesto per macOS)

L'applicazione utilizza Tkinter per il selettore dei file. Su macOS, utilizzando Python installato tramite Homebrew, è necessario installare manualmente il supporto grafico:
Bash

brew install tcl-tk
brew install python-tk

(Su Fedora/Linux: sudo dnf install python3-tkinter)
2. Configurazione dell'Ambiente Virtuale

Crea e attiva un ambiente virtuale dedicato:
Bash

# Entra nella cartella del progetto
cd ~/QuizApp

# Crea l'ambiente chiamato 'quiz'
python3 -m venv quiz

# Attiva l'ambiente
source quiz/bin/activate

3. Installazione delle Dipendenze

Con l'ambiente attivo, installa la libreria Flet:
Bash

pip install flet

Come avviare l'Applicazione

Posizionati nella root del progetto e avvia lo script principale:
Bash

# Attiva l'ambiente (se non è già attivo)
source quiz/bin/activate

# Avvia l'applicazione
python3 src/main.py

Tramite il pulsante "Seleziona File JSON", carica uno dei file presenti nella directory data/ (es. sopr_quiz_completo.json).
Struttura del Progetto

Il codice sorgente è suddiviso nei seguenti moduli:

    src/main.py: Gestisce l'inizializzazione e la navigazione tra le view dell'applicazione.

    src/models.py: Contiene la classe QuizState per la gestione dello stato, dei dati e del calcolo dei punteggi.

    src/views.py: Raccoglie i componenti UI e le funzioni di rendering dell'interfaccia Flet.

    src/utils.py: Gestisce i processi esterni e l'isolamento delle chiamate di sistema (file dialog).

    data/: Directory destinata ai database delle domande.

Formato Dati (JSON)

Il parser dell'applicazione richiede file JSON formattati con la seguente struttura:
JSON

[
  {
    "domanda": "Testo della domanda?",
    "opzioni": ["Opzione A", "Opzione B", "Opzione C"],
    "corrette": [0]
  }
]