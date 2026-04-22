import flet as ft
from models import QuizState
from views import render_home, render_quiz

def main(page: ft.Page):
    # 1. Configurazione globale della finestra
    page.title = "SOPR Quiz Master PRO"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1100
    page.window_height = 850
    
    # 2. Inizializzazione della memoria centrale
    state = QuizState()

    # 3. Router di navigazione (Controller)
    def go_to_quiz():
        render_quiz(page, state, on_home=go_to_home)

    def go_to_home():
        render_home(page, state, on_start=go_to_quiz)

    # 4. Avvio dell'app
    go_to_home()

if __name__ == "__main__":
    ft.app(target=main)