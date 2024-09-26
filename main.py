##############################
# Pogramm: Main Pogramm      #
# Code Version: 1.2          #
# Code by BolliSoft          #
# (c) by Nico Bollhalder     #
##############################

import sys
sys.path.append('./DLL/Module/')
sys.path.append('./DLL/Skripte/ScreenRec/')
from cryptography.fernet import Fernet
from datetime import datetime, date
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkcalendar import Calendar
import play
import rec
import threading
import pyautogui
import time
import keyboard
import os

selected_file=None
wert1=None
wert2=None

def datum_aus_token_entschluesseln(schluessel_datei="./Lizenz/Lizenz.key", token_datei="./Lizenz/_Lizenz.enc"):
    """
    Entschlüsselt ein Datum aus einer Token-Datei und prüft, ob es noch gültig ist.

    Args:
        schluessel_datei: Der Pfad zur Datei, die den Schlüssel enthält (Standard: "schluessel.key").
        token_datei: Der Pfad zur Datei, die das Token enthält (Standard: "token.enc").

    Returns:
        Das entschlüsselte Datum als String im Format 'YYYY-MM-DD'.
    """

    # Schlüssel und Token aus Dateien laden
    try:
        with open(schluessel_datei, "rb") as schluessel_file:
            schluessel = schluessel_file.read()
        with open(token_datei, "rb") as token_file:
            token = token_file.read()
    except:
            messagebox.showinfo("Keine Lizenz gefunden", "Es wurde keine Lizenz gefunden bitte erwerben sie eine Lizenz schreiben sie nico.bollhalder22@gmail.com\nPogramm wird nun geschlossen!")
    try:
        f = Fernet(schluessel)
        datum_bytes = f.decrypt(token)
        datum_str = datum_bytes.decode('utf-8')
    except:
        messagebox.showinfo("Lizenz Manipuliert!", "Lizenz wurde manipuliert oder ist defekt!\nPogramm wird nun geschlossen!")
        datum_str=None

    # Datum überprüfen
    entschluesseltes_datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
    heute = date.today()

    if entschluesseltes_datum >= heute:
        return datum_str,True # gültig
    else:
        return datum_str,False # abgelaufen

datum, ist_gueltig = datum_aus_token_entschluesseln() 
if ist_gueltig == False:
    messagebox.showinfo("Lizenz", "Lizenz ungültig/abgelaufen oder nicht vorhanden!")
    
if ist_gueltig == True:
    #{
    def play_actions_in_thread():
        try:
            global selected_file
            wert1, wert2 = lade_standardwerte()
            messagebox.showinfo(f"Aufnahme", "Aufnahme wird nach dem bestätigen abgespielt\n["+wert2+"] um zu beenden")
            play.play_actions("./Konfig/Recorder/"+selected_file, wert2)
        except:
            messagebox.showwarning("Keine Aufnahmen", "Es wurde keine Konfiguration geladen oder es wurde noch keine erstellt.\nBitte zuerst eine Aufnahme erstellen!")
    def rec_actions_in_thread():
        wert1, wert2 = lade_standardwerte()
        rec.start_recording(wert1,wert2)
        messagebox.showinfo("Rec", wert1+" Pause einfügen\n"+wert2+" Aufnahme beenden!")

    def button_rec():
        rec_actions_in_thread()        

    def button_play():
        threading.Thread(target=play_actions_in_thread).start()

    def button_lizenz():
        messagebox.showinfo("Lizenz", "Ihre Lizenz ist bis "+str(datum)+" gültig\n\nFür eine neue Lizenz oder eine Lizenz verlängerung kontaktieren sie:\n\nnico.bollhalder22@gmail.com\n\n")

    def populate_dropdown(event):
        """Diese Funktion wird aufgerufen, wenn die Dropdown-Liste geöffnet wird. 
        Sie durchsucht den ausgewählten Ordner und füllt die Dropdown-Liste."""
        folder_path = "./Konfig/Recorder/"
        if not folder_path:
            return  # Benutzer hat abgebrochen

        txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        combobox['values'] = txt_files

    def on_select(event):
        global selected_file
        """Wird aufgerufen, wenn ein Element in der Dropdown-Liste ausgewählt wird."""
        selected_file = combobox.get()
        print("Ausgewählte Datei:", selected_file)

    def show_help():
        wert1, wert2 = lade_standardwerte()
        """
        Erstellt und zeigt ein Fenster mit Hilfeinformationen an.
        """

        help_window = tk.Toplevel()  # Erstellt ein neues Fenster über dem Hauptfenster
        help_window.title("Hilfe")
        help_window.iconbitmap("./Bilder/FIcon.ico")

        # Label mit dem Hilfetext
        help_label = tk.Label(help_window, text=f"""
        Dies ist das Maus- und Tastatur-Aufnahmeprogramm.

        Tasten:
        - {wert1} Fügt eine Verzögerung von 10 Sekunde hinzu.
        - {wert2} Beendet die Aufnahme und speichert die Daten.

        Mausklicks und Tastatureingaben werden automatisch aufgezeichnet.
        """)
        help_label.pack(padx=20, pady=20)

        # Button zum Schließen des Hilfefensters
        close_button = tk.Button(help_window, text="Schließen", command=help_window.destroy)
        close_button.pack(padx=20, pady=20)
    
    def on_confirm():
        """
        Diese Funktion wird aufgerufen, wenn der Bestätigungsbutton geklickt wird. 
        Sie liest die Werte aus den Eingabefeldern, löscht ggf. eine bestehende "eingaben.txt" 
        und schreibt die neuen Werte in die Datei.
        """
        value1 = entry1.get()
        value2 = entry2.get()

        # Überprüfen, ob die Datei existiert und ggf. löschen
        if os.path.exists("./Konfig/Keybindings/Keybindings.txt"):
            os.remove("./Konfig/Keybindings/Keybindings.txt")

        # Datei öffnen und Eingaben schreiben
        with open("./Konfig/Keybindings/Keybindings.txt", "w") as f:
            f.write(f"Keybinding 1: {value1}\n")
            f.write(f"Keybinding 2: {value2}\n")

        #print("Eingaben wurden in 'Keybindings.txt' gespeichert.")

    def lade_standardwerte():
        global wert1, wert2
        try:
            with open("./Konfig/Keybindings/Keybindings.txt", "r") as f:
                zeilen = f.readlines()
                if len(zeilen) >= 2:
                    entry1.delete(0, tk.END) 
                    entry2.delete(0, tk.END) 

                    wert1 = zeilen[0].split(":")[1].strip()
                    wert2 = zeilen[1].split(":")[1].strip()
                    entry1.insert(0, wert1)
                    entry2.insert(0, wert2)
                    return wert1, wert2  # Gibt immer ein Tupel zurück
                else:
                    raise ValueError("Datei enthält nicht genügend Werte")
        except FileNotFoundError:
            #print("Datei 'Keybindings.txt' nicht gefunden. Standardwerte werden verwendet.")
            entry1.delete(0, tk.END) 
            entry2.delete(0, tk.END) 
            entry1.insert(0, "f3")
            entry2.insert(0, "f4")
            return "f3", "f4"  # Gibt Standardwerte zurück
        except ValueError as e:
            #print(f"Fehler beim Lesen der Werte: {e}. Standardwerte werden verwendet.")
            entry1.delete(0, tk.END) 
            entry2.delete(0, tk.END) 
            entry1.insert(0, "f3")
            entry2.insert(0, "f4")
            return "f3", "f4"  # Gibt Standardwerte zurück

    # Hauptfenster erstellen
    fenster = tk.Tk()
    fenster.title("BolliSoft's Auto-Klicker")
    fenster.geometry("400x400") 
    fenster.iconbitmap("./Bilder/FIcon.ico")

    # Frames erstellen
    recorder_frame = ttk.LabelFrame(fenster, text="Recorder")
    recorder_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    keybindings_frame = ttk.LabelFrame(fenster, text="Keybindings")
    keybindings_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

    info_frame = ttk.LabelFrame(fenster, text="Info")
    info_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    automation_frame = ttk.LabelFrame(fenster, text="Automation")
    automation_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    # Recorder-Elemente
    ttk.Label(recorder_frame, text="Aufnahmen:").grid(row=0, column=0, padx=5, pady=5)
    combobox = ttk.Combobox(recorder_frame, state="readonly")
    combobox.grid(row=1, column=0, padx=5, pady=5)
    combobox.bind("<Button-1>", populate_dropdown) 
    combobox.bind("<<ComboboxSelected>>", on_select)

    ttk.Button(recorder_frame, text="Rec", command=button_rec).grid(row=2, column=0, padx=5, pady=5)
    ttk.Button(recorder_frame, text="Play", command=button_play).grid(row=3, column=0, padx=5, pady=5)

    # Keybindings-Elemente
    ttk.Label(keybindings_frame, text="Pause:").grid(row=0, column=0, padx=5, pady=5)
    entry1 = ttk.Entry(keybindings_frame)
    entry1.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(keybindings_frame, text="Stop:").grid(row=1, column=0, padx=5, pady=5)
    entry2 = ttk.Entry(keybindings_frame)
    entry2.grid(row=1, column=1, padx=5, pady=5)

    ttk.Button(keybindings_frame, text="Keybindings speichern", command=on_confirm).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Info-Elemente
    ttk.Button(info_frame, text="Lizenz", command=button_lizenz).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(info_frame, text="Hilfe", command=show_help).grid(row=1, column=0, padx=5, pady=5)

    # Automation-Elemente (vorerst leer)
    # ...

    # Standardwerte laden und in die Eingabefelder setzen
    wert1, wert2 = lade_standardwerte()

    # Fenster anzeigen
    fenster.mainloop()
    #}

