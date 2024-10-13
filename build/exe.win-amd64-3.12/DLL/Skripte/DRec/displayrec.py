import cv2
import numpy as np
import pyautogui
from keyboard import is_pressed
import tkinter as tk
from tkinter import filedialog
import os
import threading

# Globale Variable für den Thread und den Aufnahmestatus
recording_thread = None
is_recording = False

def screen_rec():
    global is_recording
    # Bildschirmgröße ermitteln
    screen_size = (pyautogui.size().width, pyautogui.size().height)

    # Video-Codec definieren
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Standard-Speicherpfad 
    default_path = os.path.expanduser("./Exports/Videos/") 

    # Datei-Dialog öffnen, um den Speicherort und Dateinamen zu wählen 
    root = tk.Tk()
    root.withdraw() 
    file_path = filedialog.asksaveasfilename(
        initialdir=default_path, 
        defaultextension=".mp4",
        filetypes=[("MP4-Dateien", "*.mp4")],
    )

    if not file_path:  
        print("Aufnahme abgebrochen.")
        return

    # VideoWriter-Objekt erstellen 
    out = cv2.VideoWriter(file_path, fourcc, 20.0, screen_size)

    print("Aufnahme gestartet. Schließen Sie das Fenster, um die Aufnahme zu beenden.")

    # Fenster für die Anzeige erstellen
    cv2.namedWindow("Screen Recording", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Screen Recording", 800, 600)  # Optional: Größe anpassen

    is_recording = True

    while is_recording and cv2.getWindowProperty("Screen Recording", cv2.WND_PROP_VISIBLE) >= 1:
        # Bildschirm erfassen
        img = pyautogui.screenshot()
        frame = np.array(img)

        # Farbe von BGR zu RGB konvertieren 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Frame zum Video hinzufügen
        out.write(frame)

        # Frame im Fenster anzeigen
        cv2.imshow("Screen Recording", frame)
        cv2.waitKey(1)  # Notwendig, um das Fenster zu aktualisieren

    # Aufnahme beenden und Ressourcen freigeben
    out.release()
    cv2.destroyAllWindows()
    is_recording = False
    print(f"Aufnahme beendet und gespeichert als '{file_path}'")


def start_screen_rec_threaded():
    global recording_thread, is_recording
    if not is_recording: 
        recording_thread = threading.Thread(target=screen_rec)
        recording_thread.start()
    else:
        print("Aufnahme läuft bereits.")

def stop_screen_rec():
    global recording_thread, is_recording
    if is_recording:
        is_recording = False 
        if recording_thread and recording_thread.is_alive():
            recording_thread.join() 
            recording_thread = None
        print("Aufnahme gestoppt.")
    else:
        print("Keine Aufnahme läuft.")