import cv2
import numpy as np
import pyautogui
from keyboard import is_pressed
import tkinter as tk
from tkinter import filedialog
import os

def star_sreen_rec():
    # Bildschirmgröße ermitteln
    screen_size = (pyautogui.size().width, pyautogui.size().height)

    # Video-Codec definieren
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Standard-Speicherpfad (hier kannst du deinen gewünschten Pfad einstellen)
    default_path = os.path.expanduser("./Exports/Videos/")  # Beispiel: Desktop

    # Datei-Dialog öffnen, um den Speicherort und Dateinamen zu wählen (mit Standardpfad)
    root = tk.Tk()
    root.withdraw()  # Verstecke das Hauptfenster
    file_path = filedialog.asksaveasfilename(
        initialdir=default_path,  # Setze den Standardpfad
        defaultextension=".mp4",
        filetypes=[("MP4-Dateien", "*.mp4")],
    )

    if not file_path:  # Abbrechen, wenn keine Datei ausgewählt wurde
        print("Aufnahme abgebrochen.")
        return

    # VideoWriter-Objekt erstellen mit dem ausgewählten Dateipfad
    out = cv2.VideoWriter(file_path, fourcc, 60.0, screen_size)

    print("Aufnahme gestartet. Drücke F4 zum Beenden.")

    while True:
        # ... (Rest des Aufnahmecodes bleibt gleich)
        # Bildschirm erfassen
        img = pyautogui.screenshot()
        frame = np.array(img)

        # Farbe von BGR zu RGB konvertieren (OpenCV-Standard)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Frame zum Video hinzufügen
        out.write(frame)

        # Auf F4-Taste prüfen
        if is_pressed('f4'):
            break

    # Aufnahme beenden und Ressourcen freigeben
    out.release()
    cv2.destroyAllWindows()

    print(f"Aufnahme beendet und gespeichert als '{file_path}'")