import flet as ft
import json
import os
import subprocess
import sys

def main(page: ft.Page):
    page.title = "SOPR Quiz Master PRO"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1100
    page.window_height = 850
    
    # Stato dell'app
    state = {
        "domande": [], 
        "indice": 0, 
        "punti": 0, 
        "risposte_utente": {}, 
        "punti_presi": set() # Tiene traccia delle domande in cui hai preso il punto
    }

    def carica_dati(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                state["domande"] = json.load(f)
            state["indice"] = 0
            state["punti"] = 0
            state["risposte_utente"] = {i: set() for i in range(len(state["domande"]))}
            state["punti_presi"] = set()
            costruisci_interfaccia_quiz()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Errore: {ex}"))
            page.snack_bar.open = True
            page.update()

    def seleziona_file_finder(e):
        script = (
            "import tkinter as tk; from tkinter import filedialog; "
            "root=tk.Tk(); root.withdraw(); root.attributes('-topmost', True); "
            "print(filedialog.askopenfilename(filetypes=[('JSON files', '*.json')]))"
        )
        risultato = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
        file_path = risultato.stdout.strip()
        if file_path: carica_dati(file_path)

    sidebar_content = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
    main_content = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS, spacing=20)

    def aggiorna_sidebar():
        sidebar_content.controls.clear()
        for i in range(len(state["domande"])):
            is_current = i == state["indice"]
            sidebar_content.controls.append(
                ft.Container(
                    content=ft.Text(f"Domanda {i+1}", color="white" if is_current else "grey400"),
                    padding=10,
                    bgcolor="blue900" if is_current else None,
                    border_radius=5,
                    on_click=lambda _, idx=i: vai_a_domanda(idx),
                    ink=True
                )
            )
        page.update()

    def vai_a_domanda(idx):
        if 0 <= idx < len(state["domande"]):
            state["indice"] = idx
            mostra_domanda()

    def mostra_domanda():
        main_content.controls.clear()
        aggiorna_sidebar()
        
        if state["indice"] >= len(state["domande"]):
            perc = (state["punti"] / len(state["domande"])) * 100
            main_content.controls.append(
                ft.Column([
                    ft.Text("🏁 Quiz Terminato!", size=40, weight="bold"),
                    ft.Text(f"Punteggio Finale: {state['punti']} / {len(state['domande'])} ({perc:.1f}%)", size=20),
                    ft.ElevatedButton("Ricomincia", on_click=lambda _: mostra_home())
                ], horizontal_alignment="center")
            )
            page.update()
            return

        q = state["domande"][state["indice"]]
        
        main_content.controls.append(
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: vai_a_domanda(state["indice"]-1), disabled=state["indice"]==0),
                ft.Text(f"Domanda {state['indice']+1}/{len(state['domande'])}", size=20, weight="bold", color="blue200"),
                ft.IconButton(ft.Icons.ARROW_FORWARD, on_click=lambda _: vai_a_domanda(state["indice"]+1), disabled=state["indice"]==len(state['domande'])-1),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

        main_content.controls.append(ft.Text(q["domanda"], size=22, weight="bold", selectable=True))        
        opzioni_col = ft.Column()
        opzioni_col = ft.Column()
        def on_check(e):
            idx = e.control.data
            if e.control.value: state["risposte_utente"][state["indice"]].add(idx)
            else: state["risposte_utente"][state["indice"]].discard(idx)

        # --- MODIFICA QUI ---
        for i, opt in enumerate(q["opzioni"]):
            is_checked = i in state["risposte_utente"][state["indice"]]
            lettera = chr(97 + i)
            testo_con_lettera = f"{lettera}) {opt}"
            
            # 1. Creiamo la sola spunta senza testo
            box = ft.Checkbox(data=i, value=is_checked, on_change=on_check)
            
            # 2. Creiamo il testo separato e gli diamo "expand=True" per forzare l'a capo
            testo_opzione = ft.Text(testo_con_lettera, size=16, expand=True)
            
            # 3. Li uniamo in una riga allineati in alto (così se il testo fa 3 righe, la spunta resta su)
            opzioni_col.controls.append(
                ft.Row(
                    controls=[box, testo_opzione], 
                    vertical_alignment="start"
                )
            )# Contenitore dedicato per il risultato (così non spamma messaggi multipli)
        risultato_col = ft.Column()

        def verifica(e):
            risultato_col.controls.clear()
            corrette = set(q["corrette"])
            esatto = state["risposte_utente"][state["indice"]] == corrette
            
            # Gestione dinamica dei punti (se cambi idea, si aggiorna)
            if esatto and state["indice"] not in state["punti_presi"]:
                state["punti"] += 1
                state["punti_presi"].add(state["indice"])
            elif not esatto and state["indice"] in state["punti_presi"]:
                state["punti"] -= 1
                state["punti_presi"].remove(state["indice"])
            
            colore = "green400" if esatto else "red400"
            lettere = [chr(97 + i) for i in corrette]
            msg = "CORRETTO! 🎉" if esatto else f"ERRORE ❌. Risposte: {', '.join(lettere)}"
            
            risultato_col.controls.append(ft.Text(msg, color=colore, weight="bold", size=18))
            risultato_col.controls.append(ft.ElevatedButton("Prossima Domanda", icon=ft.Icons.NAVIGATE_NEXT, on_click=lambda _: prossimo()))
            page.update()

        def prossimo():
            state["indice"] += 1
            mostra_domanda()

        main_content.controls.append(opzioni_col)
        main_content.controls.append(ft.ElevatedButton("Verifica Risposta", icon=ft.Icons.CHECK, on_click=verifica))
        main_content.controls.append(risultato_col)
        page.update()

    def costruisci_interfaccia_quiz():
        page.clean()
        page.add(
            ft.Row([
                ft.Container(content=sidebar_content, width=220, bgcolor="black26", padding=10),
                ft.Container(content=main_content, expand=True, padding=30)
            ], expand=True)
        )
        mostra_domanda()

    def mostra_home():
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.QUIZ, size=100, color="blue400"),
                    ft.Text("SOPR Quiz Master PRO", size=32, weight="bold"),
                    ft.ElevatedButton("Seleziona File JSON", icon=ft.Icons.FOLDER_OPEN, on_click=seleziona_file_finder, width=300, height=50)
                ], horizontal_alignment="center", spacing=30),
                alignment=ft.alignment.Alignment(0, 0),
                expand=True
            )
        )

    mostra_home()

ft.app(target=main)