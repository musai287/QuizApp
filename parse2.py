import json
import os
import re

def parse_quizlet(file_path):
    if not os.path.exists(file_path):
        print(f"❌ Errore: Il file {file_path} non esiste.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Dividiamo il file usando il separatore di riga %$%
    blocks = content.split('%$%')
    dataset = []

    for block in blocks:
        if '/&/' not in block:
            continue
        
        # Separiamo Domanda+Opzioni dalla Risposta Corretta
        parts = block.split('/&/')
        q_section = parts[0].strip()
        a_section = parts[1].strip()

        # Estraiamo le opzioni (cerca righe che iniziano con una lettera e un punto, es: "a.")
        options = re.findall(r'^[a-g]\.\s*(.+)', q_section, re.MULTILINE)
        
        # Estraiamo il testo della domanda (tutto ciò che precede la prima opzione "a.")
        q_text_match = re.split(r'\n[a-g]\.', q_section)[0]
        q_text = q_text_match.replace('Domanda:', '').replace('Flashcard', '').strip()

        # Troviamo gli indici delle risposte corrette
        # Confrontiamo ogni opzione con il testo della risposta corretta
        correct_indices = []
        for idx, opt in enumerate(options):
            # Se l'opzione è presente nel blocco della risposta corretta, la aggiungiamo
            if opt.strip().lower() in a_section.lower():
                correct_indices.append(idx)

        if q_text and options:
            dataset.append({
                "domanda": q_text,
                "opzioni": options,
                "corrette": correct_indices
            })

    # Salvataggio
    os.makedirs('data', exist_ok=True)
    with open('data/sopr_quiz.json', 'w', encoding='utf-8') as out:
        json.dump(dataset, out, indent=4, ensure_ascii=False)
    
    print(f"✅ Conversione riuscita! Create {len(dataset)} domande in 'data/sopr_quiz.json'")

# Avvio
parse_quizlet('./data/quizletesp.txt')
