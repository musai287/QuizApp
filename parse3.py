import json
import os
import re

def parse_quizlet_v2(file_path):
    if not os.path.exists(file_path):
        print(f"❌ Errore: Il file {file_path} non esiste.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Dividiamo il file usando il nuovo separatore chiaro
    blocks = content.split('*NUOVA DOMANDA*')
    dataset = []

    for block in blocks:
        if 'RISPOSTA' not in block:
            continue
        
        # Separiamo la sezione Domanda+Opzioni dalla sezione Risposta
        parts = block.split('RISPOSTA')
        q_section = parts[0].strip()
        a_section = parts[1].strip()

        # Estraiamo le opzioni (es: a., b., c.)
        options = re.findall(r'^[a-g]\.\s*(.+)', q_section, re.MULTILINE)
        
        # Estraiamo il testo della domanda (tutto prima della prima opzione 'a.')
        q_text_match = re.split(r'\n[a-g]\.', q_section)[0]
        q_text = q_text_match.replace('Relativamente a', 'Relativamente a').strip()

        # Identifichiamo gli indici delle risposte corrette
        correct_indices = []
        for idx, opt in enumerate(options):
            # Pulizia minima per il confronto testuale
            if opt.strip().lower() in a_section.lower():
                correct_indices.append(idx)

        if q_text and options:
            dataset.append({
                "domanda": q_text,
                "opzioni": [o.strip() for o in options],
                "corrette": correct_indices
            })

    # Salvataggio nel file JSON per l'app
    os.makedirs('data', exist_ok=True)
    output_path = 'data/sopr_quiz.json'
    with open(output_path, 'w', encoding='utf-8') as out:
        json.dump(dataset, out, indent=4, ensure_ascii=False)
    
    print(f"✅ Conversione completata! Create {len(dataset)} domande in '{output_path}'.")

# Avvio del processo sul nuovo file
parse_quizlet_v2('./data/quizletespv2.txt')
