import json
import os
import re

def parse_complete(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File non trovato: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Dividiamo per il delimitatore personalizzato
    blocks = content.split('*NUOVA DOMANDA*')
    dataset = []

    for block in blocks:
        if 'RISPOSTA' not in block:
            continue
        
        parts = block.split('RISPOSTA')
        q_section = parts[0].strip()
        a_section = parts[1].strip()

        # Regex ultra-flessibile per le opzioni: 
        # Cerca (a-g) seguiti opzionalmente da . o ) e poi uno spazio
        options_raw = re.findall(r'^\s*[\*\-\•\○\s]*([a-gA-G])[\.\)]?\s+(.+)', q_section, re.MULTILINE)
        
        # Fallback per i pallini se non ci sono lettere
        if not options_raw:
            bullet_options = re.findall(r'^[○●]\s*(.+)', q_section, re.MULTILINE)
            if bullet_options:
                options_raw = [(chr(97 + i), opt) for i, opt in enumerate(bullet_options)]

        options_text = [opt[1].strip() for opt in options_raw]
        
        # Estrazione domanda: tutto ciò che non è una riga di opzione
        q_lines = q_section.split('\n')
        q_text_lines = []
        for line in q_lines:
            clean_line = line.strip()
            if not re.match(r'^[\*\-\•\○\s]*[a-gA-G][\.\)]?\s+', clean_line) and \
               not clean_line.startswith('○') and \
               not clean_line.startswith('●') and \
               clean_line != "":
                q_text_lines.append(clean_line)
        
        q_full_text = " ".join(q_text_lines)
        # Rimuove intestazioni di Quizlet e metadati
        q_full_text = re.sub(r'(\*\*File \d+:\*\*|\*\*Domanda:\*\*|Domanda \d+:|Scegli una o più alternative:)', '', q_full_text, flags=re.IGNORECASE).strip()

        # Mappatura risposte corrette con confronto flessibile
        correct_indices = []
        for idx, opt in enumerate(options_text):
            # Pulizia per il confronto (rimuoviamo tutto ciò che non è testo o numeri)
            clean_opt = re.sub(r'[^\w\s]', '', opt.lower()).strip()
            clean_ans = re.sub(r'[^\w\s]', '', a_section.lower()).strip()
            if clean_opt in clean_ans:
                correct_indices.append(idx)

        if q_full_text and options_text:
            dataset.append({
                "domanda": q_full_text,
                "opzioni": options_text,
                "corrette": correct_indices
            })

    output_path = 'data/sopr_quiz2.json'
    os.makedirs('data', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as out:
        json.dump(dataset, out, indent=4, ensure_ascii=False)
    
    print(f"✅ OPERAZIONE COMPLETATA!")
    print(f"📊 Domande totali processate: {len(dataset)}")

parse_complete('./data/quizletpt2.txt')
