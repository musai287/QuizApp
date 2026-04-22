import json
import os
import re

def parse_final(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File non trovato: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Dividiamo per la parola chiave che hai inserito
    blocks = content.split('*NUOVA DOMANDA*')
    dataset = []

    for block in blocks:
        if 'RISPOSTA' not in block:
            continue
        
        parts = block.split('RISPOSTA')
        q_section = parts[0].strip()
        a_section = parts[1].strip()

        # 1. Regex evoluta per le opzioni: cattura "a.", "* a.", "- a.", ecc.
        # Supporta sia lettere minuscole che maiuscole
        options_raw = re.findall(r'^\s*[\*\-\•\○\s]*([a-gA-G])\.\s*(.+)', q_section, re.MULTILINE)
        
        # Se non trova lettere, prova a cercare righe che iniziano con pallini (○ o ●)
        if not options_raw:
            bullet_options = re.findall(r'^[○●]\s*(.+)', q_section, re.MULTILINE)
            if bullet_options:
                # Se sono pallini, assegniamo noi le lettere a, b, c...
                options_raw = [(chr(97 + i), opt) for i, opt in enumerate(bullet_options)]

        options_text = [opt[1].strip() for opt in options_raw]
        
        # 2. Estrazione della domanda pulita
        # Prendiamo tutto ciò che non è un'opzione e non è un'intestazione
        q_lines = q_section.split('\n')
        q_text_lines = []
        for line in q_lines:
            clean_line = line.strip()
            # Se la riga non è un'opzione e non è un'intestazione di Quizlet, è la domanda
            if not re.match(r'^[\*\-\•\○\s]*[a-gA-G]\.', clean_line) and \
               not clean_line.startswith('○') and \
               not clean_line.startswith('●'):
                q_text_lines.append(clean_line)
        
        q_full_text = " ".join(q_text_lines)
        # Pulizia finale da etichette inutili
        q_full_text = re.sub(r'(\*\*File \d+:\*\*|\*\*Domanda:\*\*|Domanda \d+:)', '', q_full_text).strip()

        # 3. Mappatura risposte corrette
        correct_indices = []
        for idx, opt in enumerate(options_text):
            # Confronto flessibile (senza spazi extra e case-insensitive)
            if opt.lower() in a_section.lower():
                correct_indices.append(idx)

        if q_full_text and options_text:
            dataset.append({
                "domanda": q_full_text,
                "opzioni": options_text,
                "corrette": correct_indices
            })

    os.makedirs('data', exist_ok=True)
    with open('data/sopr_quiz.json', 'w', encoding='utf-8') as out:
        json.dump(dataset, out, indent=4, ensure_ascii=False)
    
    print(f"🚀 CONVERSIONE COMPLETATA!")
    print(f"✅ Domande totali caricate: {len(dataset)}")

parse_final('./data/quizletespv2.txt')
