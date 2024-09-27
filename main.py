##############################
# Pogramm: Main Pogramm      #
# Code Version: 1.3          #
# Code by BolliSoft          #
# (c) by Nico Bollhalder     #
##############################

import sys
sys.path.append('./DLL/Module/')
sys.path.append('./DLL/Skripte/ScreenRec/')
sys.path.append('./DLL/Skripte/DB/')
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
import locale
import csv
import RD
import CCsv


selected_file=None
wert1=None
wert2=None


from cryptography.fernet import Fernet
from datetime import datetime, date

def datum_aus_token_entschluesseln(schluessel_datei="./Lizenz/Lizenz.key", token_datei="./Lizenz/_Lizenz.enc"):
    """
    Entschlüsselt ein oder mehrere Datumswerte (repräsentieren Lizenzen) aus einer Token-Datei 
    und prüft deren Gültigkeit.

    Args:
        schluessel_datei: Der Pfad zur Datei, die den Schlüssel enthält (Standard: "schluessel.key").
        token_datei: Der Pfad zur Datei, die das Token enthält (Standard: "token.enc").

    Returns:
        Ein Tupel bestehend aus:
            - datum_werte: Eine Liste der entschlüsselten Datumswerte als Strings im Format 'YYYY-MM-DD'.
            - gueltigkeiten: Eine Liste, die für jedes Datum angibt, ob es gültig ist (True) oder nicht (False).
    """

    try:
        # Schlüssel und Token aus Dateien laden
        with open(schluessel_datei, "rb") as schluessel_file:
            schluessel = schluessel_file.read()
        with open(token_datei, "rb") as token_file:
            token = token_file.read()

        f = Fernet(schluessel)
        datum_bytes = f.decrypt(token)
        datum_str = datum_bytes.decode('utf-8')

        # Datumswerte trennen und überprüfen
        datum_werte = datum_str.split(":")
        gueltigkeiten = []  # Liste zur Speicherung der Gültigkeiten
        heute = date.today()

        for datum_wert in datum_werte:
            try:
                entschluesseltes_datum = datetime.strptime(datum_wert, "%Y-%m-%d").date()
                if entschluesseltes_datum >= heute:
                    gueltigkeiten.append(True)  # Lizenz gültig
                    print(f"Lizenz mit Ablaufdatum {datum_wert} ist gültig.")
                else:
                    gueltigkeiten.append(False)  # Lizenz abgelaufen
                    print(f"Lizenz mit Ablaufdatum {datum_wert} ist abgelaufen.")
            except ValueError:
                print(f"Fehler: Ungültiges Datumsformat '{datum_wert}' gefunden.")
                gueltigkeiten.append(False)  # Bei Fehler als ungültig markieren

    except FileNotFoundError:
        print(f"Fehler: Datei nicht gefunden. Überprüfe die Pfade '{schluessel_datei}' und '{token_datei}'.")
        return [], []
    except cryptography.fernet.InvalidToken:
        print("Fehler: Entschlüsselung fehlgeschlagen. Überprüfe den Schlüssel.")
        return [], []

    return datum_werte, gueltigkeiten

def lade_sprache():
    """Lädt die Sprachdatei basierend auf der Windows-Spracheinstellung."""

    # Sprache erkennen
    sprache = locale.getdefaultlocale()[0][:2]  # z.B. 'de' oder 'en'
    print(sprache)

    # Sprachdatei laden
    dateiname = f"./Sprache/{sprache}.txt"
    if not os.path.exists(dateiname):
        dateiname = "./Sprache/en.txt"  # Standardmäßig Deutsch laden
    print(dateiname)

    texte = {}
    with open(dateiname, "r", encoding="utf-8") as f:
        for zeile in f:
            text_id, text = zeile.strip().split(" = ")
            # Ersetze '\\n' durch tatsächliche Zeilenumbrüche
            textt = text.replace("\\n", "\n")
            texte[text_id] = textt
            

    return texte

# Sprachdatei laden
texte = lade_sprache()

# Hauptprogramm
datum_werte, gueltigkeiten = datum_aus_token_entschluesseln()
#print(gueltigkeiten[0])
#print(gueltigkeiten[1])

if not any(gueltigkeiten):  # Prüfung, ob mindestens eine Lizenz gültig ist
    messagebox.showinfo(texte["lizenz_button"], texte["alle_lizenzen_ungueltig"])
elif len(datum_werte) >= 3: 
    # Hier könntest du weitere Aktionen mit spezifischen Lizenzen durchführen,
    # falls nötig (z.B. datum_werte[1], datum_werte[2]) unter Berücksichtigung 
    # ihrer Gültigkeit aus der Liste 'gueltigkeiten'
    pass
    
if gueltigkeiten[0] == True or False:
    #{
    def play_actions_in_thread():
        try:
            global selected_file
            wert1, wert2 = lade_standardwerte()
            messagebox.showinfo(texte["aufnahme_titel"], texte.get("aufnahme_nachricht", "aufnahme_nachricht nicht gefunden").format(wert2))
            play.play_actions("./Konfig/Recorder/"+selected_file, wert2)
        except:
            messagebox.showwarning(texte["keine_aufnahmen_titel"], texte["keine_aufnahmen_nachricht"])
            
    def rec_actions_in_thread():
        wert1, wert2 = lade_standardwerte()
        messagebox.showinfo(texte["rec_titel"], texte.get("rec_nachricht", "rec_nachricht nicht gefunden").format(wert1, wert2))
        rec.start_recording(wert1,wert2)
        

    def button_rec():
        rec_actions_in_thread()        

    def button_play():
        threading.Thread(target=play_actions_in_thread).start()
       
    def button_dbverarbeiten():
        RD.remove_duplicates()
        
    def button_ccsv():
        CCsv.compare_and_remove_duplicates()
        
        
    def button_lizenz():
        try:
            if len(datum_werte) > 1:
                messagebox.showinfo(texte["lizenz_titel"], texte["lizenz_nachricht_mehrere"].format(datum_werte[0], datum_werte[1]))
            else:
                messagebox.showinfo(texte["lizenz_titel"], texte["lizenz_nachricht"].format(datum_werte[0]))
        except:
            messagebox.showinfo(texte["lizenz_titel"], texte["lizenz_nachricht"].format(datum_werte[0]))

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
        help_window = tk.Toplevel()
        help_window.title(texte["hilfe_titel"])
        help_window.iconbitmap("./Bilder/FIcon.ico")

    # Hole den Hilfetext und ersetze Platzhalter
        hilfe_text_mit_werten = texte.get("hilfe_text", "Hilfetext nicht gefunden").format(wert1, wert2)

    # Ersetze '\\n' durch tatsächliche Zeilenumbrüche
        hilfe_text_mit_zeilenumbruechen = hilfe_text_mit_werten.replace("\\n", "\n")

    # Label erstellen und als "rich text" behandeln
        help_label = tk.Label(help_window, text=hilfe_text_mit_zeilenumbruechen, wraplength=350, justify='left')
        help_label.pack(padx=20, pady=20)

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
    text=texte["fenster_titel"]
    fenster.title(text)
    fenster.geometry("400x400") 
    fenster.iconbitmap("./Bilder/FIcon.ico")

    # Frames erstellen
    recorder_frame = ttk.LabelFrame(fenster, text=texte["aufnahme_titel"])
    recorder_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    keybindings_frame = ttk.LabelFrame(fenster, text=texte["keybindings_label"])
    keybindings_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

    info_frame = ttk.LabelFrame(fenster, text=texte["info_label"])
    info_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    automation_frame = ttk.LabelFrame(fenster, text=texte["automation_label"])
    automation_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
    if gueltigkeiten[0] == True:
     # Recorder-Elemente
       ttk.Label(recorder_frame, text=texte["recorder_label"]).grid(row=0, column=0, padx=5, pady=5)
       combobox = ttk.Combobox(recorder_frame, state="readonly")
       combobox.grid(row=1, column=0, padx=5, pady=5)
       combobox.bind("<Button-1>", populate_dropdown) 
       combobox.bind("<<ComboboxSelected>>", on_select)

       ttk.Button(recorder_frame, text=texte["rec_titel"], command=button_rec).grid(row=2, column=0, padx=5, pady=5)
       ttk.Button(recorder_frame, text=texte["play_title"], command=button_play).grid(row=3, column=0, padx=5, pady=5)

       # Keybindings-Elemente
       keybindings_frame = ttk.LabelFrame(fenster, text=texte["keybindings_label"])
       keybindings_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
       ttk.Label(keybindings_frame, text=texte["pause_label"]).grid(row=0, column=0, padx=5, pady=5)
        # ... (Rest der Keybindings-Elemente bleiben unverändert)
       entry1 = ttk.Entry(keybindings_frame)
       entry1.grid(row=0, column=1, padx=5, pady=5)

       ttk.Label(keybindings_frame, text=texte["stop_label"]).grid(row=1, column=0, padx=5, pady=5)
       entry2 = ttk.Entry(keybindings_frame)
       entry2.grid(row=1, column=1, padx=5, pady=5)

       ttk.Button(keybindings_frame, text=texte["keybindings_speichern_button"], command=on_confirm).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

       # Info-Elemente
       ttk.Button(info_frame, text=texte["lizenz_button"], command=button_lizenz).grid(row=0, column=0, padx=5, pady=5)
       ttk.Button(info_frame, text=texte["hilfe_button"], command=show_help).grid(row=1, column=0, padx=5, pady=5)

    if gueltigkeiten[0] == True:
       # Automation-Elemente (vorerst leer)
       # ...
       ttk.Button(automation_frame, text=texte["db_remove_dublicates"], command=button_dbverarbeiten).grid(row=0, column=0, padx=5, pady=5)
       ttk.Button(automation_frame, text=texte["compare_csv"], command=button_ccsv).grid(row=1, column=0, padx=5, pady=5)
       print("DB Lizenz Gültig!")
       # Standardwerte laden und in die Eingabefelder setzen
    wert1, wert2 = lade_standardwerte()

    # Fenster anzeigen
    fenster.mainloop()
    #}
