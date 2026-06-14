import json
import os
import re
import sys
from bs4 import BeautifulSoup

def parse_moodle_html(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File non trovato: {file_path}")
        return

    print(f"📄 Analisi DOM HTML in corso da: {file_path}...\n")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    dataset = []
    
    # Trova tutti i blocchi delle domande (Moodle usa la classe 'que')
    domande = soup.find_all('div', class_=lambda x: x and 'que' in x.split())

    for d in domande:
        # 1. Estrai il testo della domanda
        qtext_div = d.find('div', class_='qtext')
        if not qtext_div: 
            continue
        
        q_text = qtext_div.get_text(separator='\n', strip=True)
        
        # 2. Estrai le opzioni multiple
        options_list = []
        answer_div = d.find('div', class_='answer')
        
        if answer_div:
            # Moodle usa SEMPRE le classi r0 e r1 per alternare le righe delle opzioni
            rows = answer_div.find_all(lambda tag: tag.has_attr('class') and any(c in ['r0', 'r1'] for c in tag['class']))
            
            # Fallback di emergenza: se non ci sono r0/r1, prendiamo il parent dei radio/checkbox
            if not rows:
                inputs = answer_div.find_all('input', type=['radio', 'checkbox'])
                rows = [inp.parent for inp in inputs]
            
            for row in rows:
                # Rimuoviamo input, lettere (a., b.) e icone (spunte/croci) dal DOM per non estrarne il testo
                for inp in row.find_all('input'):
                    inp.decompose()
                for span in row.find_all('span', class_='answernumber'):
                    span.decompose()
                for icon in row.find_all(['i', 'img']):
                    icon.decompose()
                    
                opt_text = row.get_text(separator=' ', strip=True)
                
                # Togliamo eventuali feedback residui a fine riga ("Vero", "Falso")
                opt_text = re.split(r'(?i)\b(?:Vero|Falso)\b', opt_text)[0].strip()
                if opt_text:
                    options_list.append(opt_text)
        
        # 3. Estrai la soluzione corretta (Ground Truth del prof)
        right_answer_div = d.find('div', class_='rightanswer')
        soluzioni_text = ""
        if right_answer_div:
            soluzioni_text = right_answer_div.get_text(separator=' ', strip=True)
            # FIX: Pulisce "La risposta corretta è:" o "Le risposte corrette sono:"
            soluzioni_text = re.sub(r'(?i)(?:L[ae]\s+)?(?:rispost[ae]\s+corrett[ae]\s+(?:sono|è|e\'))[\s\:\.]*', '', soluzioni_text).strip()

        correct_indices = []
        
        # 4. Assegnazione logica e Fault Tolerance
        if options_list:
            if soluzioni_text:
                super_clean_sol = re.sub(r'\W', '', soluzioni_text.lower())
                for idx, opt in enumerate(options_list):
                    super_clean_opt = re.sub(r'\W', '', opt.lower())
                    if super_clean_opt and super_clean_opt in super_clean_sol:
                        correct_indices.append(idx)
        else:
            # Caso VERO di Domande aperte / Calcoli
            if soluzioni_text:
                options_list = [f"Risultato: {soluzioni_text}"]
                correct_indices = [0]
            else:
                options_list = ["Risultato: NON TROVATO (Compilare a mano)"]
                correct_indices = [0]

        if q_text:
            dataset.append({"domanda": q_text, "opzioni": options_list, "corrette": correct_indices})

    nome_base = os.path.splitext(os.path.basename(file_path))[0]
    output_path = f'data/{nome_base}_html_parsed.json'
    
    os.makedirs('data', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as out:
        json.dump(dataset, out, indent=4, ensure_ascii=False)
    
    print(f"🎉 PARSING HTML COMPLETATO! Trovate {len(dataset)} domande perfettamente strutturate.")
    print(f"💾 File salvato in: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Utilizzo: python parse_html.py <percorso_del_file.html>")
    else:
        parse_moodle_html(sys.argv[1])
