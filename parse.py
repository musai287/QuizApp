import json
import re

def parse_custom_quiz(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Separiamo le varie flashcard usando il separatore %$%
        entries = content.split('%$%')
        quiz_data = []

        for entry in entries:
                if '/&/' not in entry:
                        continue
                    
                # Dividiamo la parte della domanda/opzioni dalla parte della risposta
                parts = entry.split('/&/')
                question_block = parts[0].strip()
                answer_block = parts[1].strip()

                # Pulizia della domanda: cerchiamo il testo principale
                # Rimuoviamo "Domanda:", "Flashcard X:", ecc.
                q_text_match = re.search(r'(?:Domanda: )?(.+?)(?=\n[a-g]\.|\n\* [a-g]\.)', question_block, re.DOTALL | re.IGNORECASE)
                if q_text_match:
                        question_text = q_text_match.group(1).replace('**', '').strip()
                else:
                        # Fallback se non ci sono opzioni lette correttamente
                    question_text = question_block.split('\n')[0].strip()

                    # Estrazione opzioni (formato a. o * a.)
                    options = re.findall(r'[a-g]\.\s*(.+)', question_block)
                    if not options:
                            # Prova con il formato dei punti elenco con asterisco
                        options = re.findall(r'\* [a-g]\.\s*(.+)', question_block)

                        # Identificazione risposte corrette
                        correct_indices = []
                        for idx, opt in enumerate(options):
                                # Se il testo dell'opzione è contenuto nel blocco risposta, è corretta
                            # Usiamo una pulizia minima per confrontare i testi
                            clean_opt = opt.strip().lower()
                            clean_ans = answer_block.strip().lower()
                            if clean_opt in clean_ans:
                                 correct_indices.append(idx)

                            if question_text and options:
                                 quiz_data.append({
                                        "domanda": question_text,
                                        "opzioni": [o.strip() for o in options],
                                        "corrette": correct_indices
                            })

                            return quiz_data

                # Esecuzione
        try:
            data = parse_custom_quiz('quizlet esportato.rtf')
            with open('data/sopr_quiz.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"✅ Conversione completata! Generate {len(data)} domande.")
        except Exception as e:
            print(f"❌ Errore durante la conversione: {e}")
