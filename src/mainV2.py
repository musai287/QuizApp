import flet as ft
import json
import os
import subprocess
import sys

def main(page: ft.Page):
    page.title = "SOPR Quiz Master"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 850
    page.window_height = 750
    
    state = {"domande": [], "indice": 0, "punti": 0, "selezionate": set()}

    # --- HACK SOPR: ISOLAMENTO DEL PROCESSO PER TKINTER ---
    def seleziona_file_finder(e):
        # Lanciamo un mini-script Python separato solo per il Finder
        # Questo evita il conflitto di thread/context switching su Mac
        script = (
            "import tkinter as tk; "
            "from tkinter import filedialog; "
            "root=tk.Tk(); root.withdraw(); "
            "root.attributes('-topmost', True); "
            "print(filedialog.askopenfilename(filetypes=[('JSON files', '*.json')]))"
        )
        
        try:
            # Esegue lo script e cattura l'output (il percorso del file)
            risultato = subprocess.run(
                [sys.executable, "-c", script], 
                capture_output=True, 
                text=True
            )
            file_path = risultato.stdout.strip()
            
            if file_path and os.path.exists(file_path):
                carica_dati(file_path)
        except Exception as ex:
            print(f"Errore subprocess: {ex}")

    def carica_dati(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                state["domande"] = json.load(f)
            state["indice"] = 0
            state["punti"] = 0
            inizia_quiz()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Errore: {ex}"))
            page.snack_bar.open = True
            page.update()

    def inizia_quiz():
        page.clean()
        mostra_domanda()

    def mostra_domanda():
        page.clean()
        if state["indice"] >= len(state["domande"]):
            perc = (state["punti"] / len(state["domande"])) * 100
            page.add(ft.Column([
                ft.Text("🏁 Quiz Terminato!", size=40, weight="bold"),
                ft.Text(f"Punteggio: {state['punti']} / {len(state['domande'])} ({perc:.1f}%)"),
                ft.ElevatedButton("Ricomincia", on_click=lambda _: main(page))
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
            return

        q = state["domande"][state["indice"]]
        state["selezionate"] = set()

        page.add(ft.Text(f"Domanda {state['indice']+1}/{len(state['domande'])}", color=ft.Colors.BLUE_200))
        page.add(ft.Text(q["domanda"], size=20, weight="bold"))
        
        opzioni_col = ft.Column()
        def on_check(e):
            idx = e.control.data
            if e.control.value: state["selezionate"].add(idx)
            else: state["selezionate"].discard(idx)

        for i, opt in enumerate(q["opzioni"]):
            opzioni_col.controls.append(ft.Checkbox(label=opt, data=i, on_change=on_check))

        def verifica(e):
            corrette = set(q["corrette"])
            esatto = state["selezionate"] == corrette
            if esatto: state["punti"] += 1
            colore = ft.Colors.GREEN_400 if esatto else ft.Colors.RED_400
            msg = "CORRETTO! 🎉" if esatto else f"ERRORE ❌. Risposta corretta: {q['corrette']}"
            page.add(ft.Text(msg, color=colore, weight="bold"))
            page.add(ft.ElevatedButton("Prossima", on_click=lambda _: prossimo()))
            page.update()

        def prossimo():
            state["indice"] += 1
            mostra_domanda()

        page.add(opzioni_col)
        page.add(ft.ElevatedButton("Verifica Risposta", icon=ft.Icons.CHECK, on_click=verifica))
        page.update()

    # SCHERMATA INIZIALE
    page.add(
        ft.Column([
            ft.Icon(ft.Icons.TERMINAL, size=80, color=ft.Colors.BLUE_400),
            ft.Text("SOPR Quiz Master", size=32, weight="bold"),
            ft.Text("Utilizzo di subprocess per isolamento GUI", color=ft.Colors.GREY_500),
            ft.ElevatedButton(
                "Apri Finder (Subprocess)", 
                icon=ft.Icons.FOLDER_OPEN,
                on_click=seleziona_file_finder,
                height=60, width=350
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
    )

ft.app(target=main)