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
        #try:
            global selected_file
            play.play_actions("./Konfig/Recorder/"+selected_file)
        #except:
            #messagebox.showwarning("Keine Aufnahmen", "Es wurde keine Konfiguration geladen oder es wurde noch keine erstellt.\nBitte zuerst eine Aufnahme erstellen!")
    def rec_actions_in_thread():
        wert1, wert2 = lade_standardwerte()
        rec.start_recording(wert1,wert2)

    def button_rec():
        threading.Thread(target=rec_actions_in_thread).start()
        messagebox.showinfo("Rec", wert1+" Pause einfügen\n"+wert2+" Aufnahme beenden!")        

    def button_play():
        threading.Thread(target=play_actions_in_thread).start()
        messagebox.showinfo("Aufnahme", "Aufnahme wird abgespielt")

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
    fenster.geometry("500x300")
    fenster.iconbitmap("./Bilder/FIcon.ico")

    #KeyBinder
    # Label und Eingabefeld 1
    label1 = tk.Label(fenster, text="Pause Setzen:")
    label1.grid(row=1, column=0, pady=0, padx=0)
    entry1 = tk.Entry(fenster)
    # entry1.insert(0, "f3")  # Standardwert wird jetzt in lade_standardwerte() gesetzt 
    entry1.grid(row=2, column=0, pady=0, padx=0)

    # Label und Eingabefeld 2
    label2 = tk.Label(fenster, text="Aufnahme stoppen:")
    label2.grid(row=3, column=0, pady=10, padx=10)
    entry2 = tk.Entry(fenster)
    # entry2.insert(0, "f4")  # Standardwert wird jetzt in lade_standardwerte() gesetzt
    entry2.grid(row=4, column=0, pady=10, padx=10)
    # Standardwerte laden
    wert1, wert2 = lade_standardwerte()
    # Bestätigungsbutton
    confirm_button = ttk.Button(fenster, text="Keybindings Speichern", command=on_confirm)
    confirm_button.grid(row=5, column=0, pady=10, padx=10)

    # Label
    label = ttk.Label(fenster, text="Recorder")
    label.grid(row=0, column=0, pady=10, padx=10)
    label = ttk.Label(fenster, text="Info")
    label.grid(row=0, column=5, pady=10, padx=10)
    label = ttk.Label(fenster, text="Automation")
    label.grid(row=0, column=4, pady=10, padx=10)
    label = ttk.Label(fenster, text="Test Automation")
    label.grid(row=0, column=1, pady=10, padx=10)

    # Button
    button = ttk.Button(fenster, text="Rec", command=button_rec)
    button.grid(row=6, column=0, pady=0, padx=10)
    button = ttk.Button(fenster, text="Play", command=button_play)
    button.grid(row=2, column=1, pady=10, padx=10)
    button = ttk.Button(fenster, text="Auto", command=button_lizenz)
    button.grid(row=1, column=4, pady=10, padx=10)
    button = ttk.Button(fenster, text="Lizenz", command=button_lizenz)
    button.grid(row=1, column=5, pady=10, padx=10)
    button = ttk.Button(fenster, text="Help", command=show_help)
    button.grid(row=2, column=5, pady=10, padx=10)

    # Dropdown-Liste erstellen
    combobox = ttk.Combobox(fenster, state="readonly")  # Readonly, damit der Benutzer nur aus der Liste auswählen kann
    combobox.grid(row=1, column=1, pady=0, padx=10)
    # Event-Handler für das Öffnen der Dropdown-Liste
    combobox.bind("<Button-1>", populate_dropdown)  # <Button-1> ist ein Linksklick
    # Event-Handler für die Auswahl
    combobox.bind("<<ComboboxSelected>>", on_select)

    # Fenster anzeigen
    fenster.mainloop()
    #}

