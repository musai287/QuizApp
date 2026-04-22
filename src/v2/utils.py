import subprocess
import sys

def seleziona_file_finder():
    """Apre il Finder in un processo isolato per prevenire il context switching deadlock su macOS."""
    script = (
        "import tkinter as tk; from tkinter import filedialog; "
        "root=tk.Tk(); root.withdraw(); root.attributes('-topmost', True); "
        "print(filedialog.askopenfilename(filetypes=[('JSON files', '*.json')]))"
    )
    risultato = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    return risultato.stdout.strip()