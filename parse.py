import json
import os
import re

def parse_ultimate(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File non trovato: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = content.split('*NUOVA DOMANDA*')
    dataset = []

    for block in blocks:
        if 'RISPOSTA' not in block:
            continue
        
        parts = block.split('RISPOSTA')
        q_section = parts[0].strip()
        a_section = parts[1].strip()

        # 1. Cerchiamo le opzioni classiche (a. b. c. o a) b) c))
        options_raw = re.findall(r'^\s*[\*\-\•\○\s]*([a-gA-G])[\.\)]?\s+(.+)', q_section, re.MULTILINE)
        options_text = [opt[1].strip() for opt in options_raw]
        
        # 2. Se non ci sono opzioni (è un esercizio di calcolo), creiamo una dummy
        if not options_text:
            # Estraiamo il valore numerico della risposta se esiste (es. "760,00")
            risultato = re.search(r'corretta è\s*:\s*(.+)', a_section, re.IGNORECASE)
            valore = risultato.group(1).strip() if risultato else "Vedi spiegazione"
            options_text = [f"Risultato: {valore}"]
            correct_indices = [0]
        else:
            # Mappatura normale per risposte multiple
            correct_indices = []
            for idx, opt in enumerate(options_text):
                clean_opt = re.sub(r'[^\w\s]', '', opt.lower()).strip()
                clean_ans = re.sub(r'[^\w\s]', '', a_section.lower()).strip()
                if clean_opt in clean_ans:
                    correct_indices.append(idx)

        # 3. Pulizia della domanda
        q_lines = q_section.split('\n')
        q_text = " ".join([l.strip() for l in q_lines if not re.match(r'^[\*\-\•\○\s]*[a-gA-G][\.\)]?\s+', l.strip()) and l.strip() != ""])
        q_text = re.sub(r'(\*\*File \d+:\*\*|\*\*Domanda:\*\*|Domanda \d+:|Scegli una o più alternative:)', '', q_text, flags=re.IGNORECASE).strip()

        if q_text:
            dataset.append({
                "domanda": q_text,
                "opzioni": options_text,
                "corrette": correct_indices
            })

    output_path = 'data/sopr_quiz2.json'
    os.makedirs('data', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as out:
        json.dump(dataset, out, indent=4, ensure_ascii=False)
    
    print(f"✅ CONVERSIONE TOTALE!")
    print(f"📊 Domande processate: {len(dataset)} (Incluse domande di calcolo)")

parse_ultimate('./data/quizletpt2.txt')
