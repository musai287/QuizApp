import flet as ft
import json
import os

def main(page: ft.Page):
    page.title = "App Quiz"
    # Nota: ThemeMode è già maiuscolo
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window_width = 800
    page.window_height = 700

    state = {
        "domande": [],
        "indice": 0,
        "punti": 0,
        "selezionate": set(),
        "mostra_risultato": False
    }

    def carica_test(nome_file):
        # Cerchiamo il file nella cartella data che sta allo stesso livello di src
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(base_path, "data", nome_file)
        
        with open(full_path, "r", encoding="utf-8") as f:
            state["domande"] = json.load(f)
        state["indice"] = 0
        state["punti"] = 0
        mostra_domanda()

    def mostra_domanda():
        page.clean()
        if state["indice"] >= len(state["domande"]):
            page.add(
                ft.Column([
                    ft.Text("🎉 Quiz Completato!", size=40, weight="bold"),
                    ft.Text(f"Punteggio Finale: {state['punti']} / {len(state['domande'])}", size=25),
                    ft.ElevatedButton("Ricomincia", on_click=lambda _: main(page))
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
            return

        q = state["domande"][state["indice"]]
        state["selezionate"] = set()
        state["mostra_risultato"] = False

        quesito = ft.Text(f"Domanda {state['indice'] + 1}/{len(state['domande'])}", size=16, color=ft.Colors.BLUE_200)
        testo_domanda = ft.Text(q["domanda"], size=22, weight="bold")
        
        opzioni_view = ft.Column()
        def on_check(e):
            idx = e.control.data
            if e.control.value: state["selezionate"].add(idx)
            else: state["selezionate"].discard(idx)

        for i, opt in enumerate(q["opzioni"]):
            opzioni_view.controls.append(
                ft.Checkbox(label=opt, data=i, on_change=on_check)
            )

       
        btn_conferma = ft.ElevatedButton("Verifica Risposta", on_click=valida, icon=ft.Icons.CHECK)
        
        page.add(
            ft.Card(
                content=ft.Container(
                    content=ft.Column([quesito, testo_domanda, ft.Divider(), opzioni_view, btn_conferma], spacing=20),
                    padding=30
                )
            )
        )
        page.update()

    def valida(e):
        if state["mostra_risultato"]: return
        
        q = state["domande"][state["indice"]]
        corrette = set(q["corrette"])
        esatto = state["selezionate"] == corrette
        
        if esatto:
            state["punti"] += 1
            # Qui ho corretto ft.colors -> ft.Colors
            colore = ft.Colors.GREEN_400
            testo = "CORRETTO!"
        else:
            colore = ft.Colors.RED_400
            lettere = [chr(97 + i) for i in corrette]
            testo = f"SBAGLIATO. Risposte corrette: {', '.join(lettere)}"

        state["mostra_risultato"] = True
        page.add(ft.Text(testo, color=colore, size=20, weight="bold"))
        # Qui ho corretto ft.icons -> ft.Icons
        page.add(ft.ElevatedButton("Prossima Domanda", on_click=prossimo, icon=ft.Icons.ARROW_FORWARD))
        page.update()

    def prossimo(e):
        state["indice"] += 1
        mostra_domanda()

    # Logica per trovare i file nella cartella data
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_path, "data")
    
    if os.path.exists(data_dir):
        files = [f for f in os.listdir(data_dir) if f.endswith(".json")]
        page.add(ft.Text("Quiz App", size=28, weight="bold"))
        page.add(ft.Text("Seleziona un set di domande:", size=16))
        for f in files:
            page.add(ft.ListTile(
                # Qui ho corretto ft.icons -> ft.Icons
                leading=ft.Icon(ft.Icons.DESCRIPTION),
                title=ft.Text(f),
                on_click=lambda e, nome=f: carica_test(nome)
            ))
    else:
        page.add(ft.Text(f"Errore: Cartella 'data' non trovata in {data_dir}", color=ft.Colors.RED))

ft.app(target=main)
