import json
import os
import re
import sys
import fitz  # PyMuPDF

def parse_moodle_pdf(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File non trovato: {file_path}")
        return

    print(f"📄 Estrazione Logica a 3-Box da: {file_path}...\n")
    
    try:
        doc = fitz.open(file_path)
        content = ""
        for page in doc:
            content += page.get_text("text") + "\n"
    except Exception as e:
        print(f"❌ Errore nella decodifica del PDF: {e}")
        return

    # Pulizia iniziale delle intestazioni di pagina Moodle
    content = re.sub(r'\\s*', '', content)
    content = re.sub(r'\d{2}/\d{2}/\d{4}, \d{2}:\d{2}\n?', '', content)
    content = re.sub(r'Test Teoria.*e-Learning Unica\n?', '', content)
    content = re.sub(r'https://elearning\.unica\.it/.*\n?', '', content)
    content = re.sub(r'\d+ di \d+\n?', '', content)
    content = re.sub(r'Vai a\.\.\.\n?', '', content)
    content = re.sub(r'< Previous Activity\n?', '', content)
    content = re.sub(r'Next Activity >\n?', '', content)

    # Dividiamo il documento intero in blocchi basati su "Domanda X"
    blocks = re.split(r'(?:^|\n)\s*(Domanda\s+\d+)\b', content, flags=re.IGNORECASE)
    dataset = []

    # blocks conterrà: ['', 'Domanda 1', 'testo della dom 1...', 'Domanda 2', ...]
    for i in range(1, len(blocks), 2):
        q_num_text = blocks[i]
        q_num = int(re.search(r'\d+', q_num_text).group())
        raw_text = blocks[i+1]

        # ==========================================
        # ARCHITETTURA A 3 BOX (Identificazione)
        # ==========================================

        # BOX 1: Header (Fino al punteggio)
        box1_end_match = re.search(r'(?i)(Punteggio ottenuto[^\n]*\n|Non risposto[^\n]*\n)', raw_text)
        start_box2 = box1_end_match.end() if box1_end_match else 0

        # BOX 3: Footer (Inizia con la dichiarazione della risposta corretta)
        box3_start_match = re.search(r'(?i)(La risposta corretta è|Le risposte corrette sono)[\:\.]', raw_text)
        if box3_start_match:
            end_box2 = box3_start_match.start()
            box3_text = raw_text[box3_start_match.end():].strip()
        else:
            end_box2 = len(raw_text)
            box3_text = ""

        # BOX 2: Il Cuore (La stringa ESATTA tra l'Header e il Footer)
        box2_text = raw_text[start_box2:end_box2].strip()

        # Puliamo la "coda" del Box 2 dall'eventuale feedback utente (es. "Risposta parzialmente esatta.")
        box2_text = re.sub(r'(?i)\n\s*Risposta\s+(corretta|errata|parzialmente esatta|parzialmente corretta)\.?\s*(\nHai selezionato.*)?$', '', box2_text, flags=re.DOTALL).strip()


        # ==========================================
        # PARSING DEL BOX 2 (Domanda + Opzioni)
        # ==========================================
        alt_match = re.search(r'(?i)(Scegli una o più alternative[\:\.]|Scegli un\'alternativa[\:\.]|Risposta[\:\.])', box2_text)

        is_open_ended = False

        if alt_match:
            q_text = box2_text[:alt_match.start()].strip()
            opts_text = box2_text[alt_match.end():].strip()
            if "Risposta" in alt_match.group():
                is_open_ended = True
        else:
            # Se non c'è la scritta "Scegli un'alternativa", è un esercizio a calcolo
            q_text = box2_text.strip()
            opts_text = ""
            is_open_ended = True

        # Rimuoviamo doppi a capo dalla domanda
        q_text = re.sub(r'\n+', '\n', q_text).strip()

        options_list = []
        correct_indices = []

        if not is_open_ended and opts_text:
            # Appiattiamo le opzioni in una riga singola per estrarle con precisione
            opts_flat = re.sub(r'\s+', ' ', opts_text).strip()

            # Troviamo i marker (a., b., i., ii.) ignorando i simboli grafici di Moodle
            marker_regex = r'(?:^|\s)(?:[\uf05d\uf05c☑✔☐Lq]\s*)?([a-hA-H]|[ivxIVX]{1,4})[\.\)]\s+'
            matches = list(re.finditer(marker_regex, opts_flat))

            for idx in range(len(matches)):
                start = matches[idx].end()
                end = matches[idx+1].start() if idx + 1 < len(matches) else len(opts_flat)
                
                opt_str = opts_flat[start:end].strip()
                
                # Pulizia finale dell'opzione dai caratteri Unicode e spoiler ("Vero:", "Falso:")
                opt_str = re.sub(r'[\uf05d\uf05c☑✔☐]', '', opt_str).strip()
                opt_str = re.split(r'(?i)\b(?:Vero|Falso)\b|⊗|✔|❌|✅', opt_str)[0].strip()

                if opt_str:
                    options_list.append(opt_str)

            # Assegnazione Punti incrociando col Box 3
            if box3_text:
                super_clean_sol = re.sub(r'\W', '', box3_text.lower())
                for idx, opt in enumerate(options_list):
                    super_clean_opt = re.sub(r'\W', '', opt.lower())
                    if super_clean_opt and super_clean_opt in super_clean_sol:
                        correct_indices.append(idx)
        else:
            # Gestione degli Esercizi a Calcolo
            risultato_pulito = ""
            if box3_text:
                sol_num_match = re.search(r'([\d\,]+)', box3_text)
                if sol_num_match:
                    risultato_pulito = sol_num_match.group(1)

            if risultato_pulito:
                options_list = [f"Risultato: {risultato_pulito}"]
            else:
                options_list = [f"Risultato: NON TROVATO (Compilare a mano)"]

            correct_indices = [0]

        if q_text:
            dataset.append({"domanda": q_text, "opzioni": options_list, "corrette": correct_indices})
            print(f"✅ Domanda {q_num} OK ({len(options_list)} opzioni)")
        else:
            print(f"❌ Domanda {q_num} SALTATA: Testo vuoto.")

    nome_base = os.path.splitext(os.path.basename(file_path))[0]
    output_path = f'data/{nome_base}_parsed.json'
    
    os.makedirs('data', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as out:
        json.dump(dataset, out, indent=4, ensure_ascii=False)
    
    print(f"\n🎉 PARSING A 3-BOX COMPLETATO! Trovate {len(dataset)} domande.")
    print(f"💾 File salvato in: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Utilizzo: python parse_moodle.py <percorso_del_file.pdf>")
    else:
        parse_moodle_pdf(sys.argv[1])
