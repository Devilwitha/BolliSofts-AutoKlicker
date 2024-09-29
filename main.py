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
sys.path.append('./DLL/Skripte/Auto/')
sys.path.append('./DLL/Skripte/DRec/')
sys.path.append('./DLL/Skripte/Logger/')
from cryptography.fernet import Fernet
from datetime import datetime, date
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkcalendar import Calendar
import customtkinter as ctk
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
import shedule
import schedule
import displayrec as drec
import cv2
import Log



selected_file=None
wert1=None
wert2=None
logfile = Log.erstelle_log_datei()

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
        d = "Schlüssel und Token aus Dateien laden" #"Schlüssel und Token aus Dateien laden"
        Log.log(logfile, d)
        with open(schluessel_datei, "rb") as schluessel_file:
            schluessel = schluessel_file.read()
            d = "Schlüssel gelesen: " + str(schluessel) 
            Log.log(logfile, d)
        with open(token_datei, "rb") as token_file:
            token = token_file.read()
            d = "Token gelesen:: "+ str(token) 
            Log.log(logfile, d)

        f = Fernet(schluessel)
        datum_bytes = f.decrypt(token)
        datum_str = datum_bytes.decode('utf-8')
        d = "Entschlüsseltes Datum: " + str(datum_str) 
        Log.log(logfile, d)

        # Datumswerte trennen und überprüfen
        d = "Datumswerte trennen und überprüfen"
        Log.log(logfile, d)
        datum_werte = datum_str.split(":")
        gueltigkeiten = []  # Liste zur Speicherung der Gültigkeiten
        d = "Liste zur Speicherung der Gültigkeiten" 
        Log.log(logfile, d)
        heute = date.today()
        d = "Datum Heute: " + str(heute) 
        Log.log(logfile, d)

        for datum_wert in datum_werte:
            try:
                entschluesseltes_datum = datetime.strptime(datum_wert, "%Y-%m-%d").date()
                if entschluesseltes_datum >= heute:
                    gueltigkeiten.append(True)  # Lizenz gültig
                    d = (f"Lizenz mit Ablaufdatum {datum_wert} ist gültig.")
                    Log.log(logfile, d)
                else:
                    gueltigkeiten.append(False)  # Lizenz abgelaufen
                    d = (f"Lizenz mit Ablaufdatum {datum_wert} ist abgelaufen.")
                    Log.log(logfile, d)
            except ValueError:
                d = (f"Fehler: Ungültiges Datumsformat '{datum_wert}' gefunden.")
                Log.log(logfile, d)
                gueltigkeiten.append(False)  # Bei Fehler als ungültig markieren

    except FileNotFoundError:
        d=(f"Fehler: Datei nicht gefunden. Überprüfe die Pfade '{schluessel_datei}' und '{token_datei}'.")
        Log.log(logfile, d)
        return [], []
    except cryptography.fernet.InvalidToken:
        d = ("Fehler: Entschlüsselung fehlgeschlagen. Überprüfe den Schlüssel.")
        Log.log(logfile, d)
        return [], []

    return datum_werte, gueltigkeiten

def lade_sprache():
    """Lädt die Sprachdatei basierend auf der Windows-Spracheinstellung."""

    # Sprache erkennen
    sprache = locale.getdefaultlocale()[0][:2]  # z.B. 'de' oder 'en'
    d = (sprache)
    Log.log(logfile, d)

    # Sprachdatei laden
    dateiname = f"./Sprache/{sprache}.txt"
    if not os.path.exists(dateiname):
        dateiname = "./Sprache/en.txt"  # Standardmäßig Deutsch laden
    d = (dateiname)
    Log.log(logfile, d)

    texte = {}
    with open(dateiname, "r", encoding="utf-8") as f:
        for zeile in f:
            text_id, text = zeile.strip().split(" = ")
            # Ersetze '\\n' durch tatsächliche Zeilenumbrüche
            textt = text.replace("\\n", "\n")
            texte[text_id] = textt
            

    return texte

# Sprachdatei laden
d = "Sprache Laden"
Log.log(logfile, d)
texte = lade_sprache()

# Hauptprogramm
datum_werte, gueltigkeiten = datum_aus_token_entschluesseln()
#print(gueltigkeiten[0])
#print(gueltigkeiten[1])

if not any(gueltigkeiten):  # Prüfung, ob mindestens eine Lizenz gültig ist
    print("!")#messagebox.showinfo(texte["lizenz_button"], texte["alle_lizenzen_ungueltig"])
elif len(datum_werte) >= 3: 
    # Hier könntest du weitere Aktionen mit spezifischen Lizenzen durchführen,
    # falls nötig (z.B. datum_werte[1], datum_werte[2]) unter Berücksichtigung 
    # ihrer Gültigkeit aus der Liste 'gueltigkeiten'
    pass
    

    #{
def play_actions_in_thread():
    try:
        d = "Abspielen der Aufnahme hat begonnen!"
        Log.log(logfile, d)
        global selected_file
        d = selected_file
        Log.log(logfile, d)
        wert1, wert2 = lade_standardwerte()
        messagebox.showinfo(texte["aufnahme_titel"], texte.get("aufnahme_nachricht", "aufnahme_nachricht nicht gefunden").format(wert2))
        play.play_actions("./Konfig/Recorder/"+selected_file, wert2)
        d = "Abspielen beended!"
        Log.log(logfile, d)
    except:
        d = "Keine Aufnahme vorhanden!"
        Log.log(logfile, d)
        messagebox.showwarning(texte["keine_aufnahmen_titel"], texte["keine_aufnahmen_nachricht"])

            
def rec_actions_in_thread():
    d = "Rec gestarted!"
    Log.log(logfile, d)
    wert1, wert2 = lade_standardwerte()
    rec.start_recording(wert1,wert2)
    messagebox.showinfo(texte["rec_titel"], texte.get("rec_nachricht", "rec_nachricht nicht gefunden"))
    d = "Rec beended!"
    Log.log(logfile, d)
        

def button_rec():
    d = "Button: button_rec"
    Log.log(logfile, d)
    rec_actions_in_thread()        

def button_play():
    d = "Button: button_play"
    Log.log(logfile, d)
    threading.Thread(target=play_actions_in_thread).start()
       
def button_dbverarbeiten():
    d = "Button: button_dbverarbeiten"
    Log.log(logfile, d)
    RD.remove_duplicates()
        
def button_ccsv():
    d = "Button: button_ccsv"
    Log.log(logfile, d)
    CCsv.compare_and_remove_duplicates()
    
def button_stop_screenrec():
    d = "Button: button_stop_screenrec"
    Log.log(logfile, d)
    drec.stop_screen_rec()
    ctk.CTkButton(screenrec_frame, text=texte["screenrec_button"], command=button_screenrec).grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    
def button_screenrec():
    d = "Button: button_screenrec"
    Log.log(logfile, d)
    drec.start_screen_rec_threaded()
    ctk.CTkButton(screenrec_frame, text=texte["stop_screenrec_button"], command=button_stop_screenrec).grid(row=0, column=0, columnspan=2, padx=5, pady=5)

def button_kill_automation():
    d = "Button: button_kill_automation"
    Log.log(logfile, d)
    shedule.stop_schedule()
    Log.log(logfile, "Erstelle CTkButton für Automation")  # Debugging-Ausgabe
    ctk.CTkButton(automation_frame, text=texte["automation_button"], command=button_automation).grid(row=0, column=0, columnspan=2, padx=5, pady=5)

def button_automation():
    d = "Button: button_automation"
    Log.log(logfile, d)
    shedule.start_schedule()
    Log.log(logfile, "Erstelle CTkButton für Kill Automation")  # Debugging-Ausgabe
    ctk.CTkButton(automation_frame, text=texte["kill_automation_button"], command=button_kill_automation).grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    
def button_lizenzordner():
    d = "Button: button_lizenzordner"
    Log.log(logfile, d)
    #result = messagebox.askquestion("Bestätigung", "Möchtest du den Lizenz Ordner öffnen?", icon='question')
    #if result == 'yes':button_csvordner
    open_folder(".\Lizenz")    

def button_csvordner():
    d = "Button: button_csvordner"
    Log.log(logfile, d)
    #result = messagebox.askquestion("Bestätigung", "Möchtest du den Lizenz Ordner öffnen?", icon='question')
    #if result == 'yes':button_csvordner
    open_folder(".\Exports\CSV")  
    
def button_aufnahmeordner():
    d = "Button: button_aufnahmeornder"
    Log.log(logfile, d)
    #result = messagebox.askquestion("Bestätigung", "Möchtest du den Lizenz Ordner öffnen?", icon='question')
    #if result == 'yes':
    open_folder(".\Konfig\Recorder") 

def button_videoordner():
    d = "Button: button_videoordner"
    Log.log(logfile, d)
    #result = messagebox.askquestion("Bestätigung", "Möchtest du den Lizenz Ordner öffnen?", icon='question')
    #if result == 'yes':
    open_folder(".\Exports\Videos") 
    
def button_lizenz():
    d = "Button: button_lizenz"
    Log.log(logfile, d)
    try:
        if len(datum_werte) > 1:
            messagebox.showinfo(texte["lizenz_titel"], texte["lizenz_nachricht_mehrere"].format(datum_werte[0], datum_werte[1]))
        else:
            messagebox.showinfo(texte["lizenz_titel"], texte["lizenz_nachricht"].format(datum_werte[0]))
    except:
        messagebox.showwarning(texte["lizenz_titel"], texte["nolizenz_nachricht"])

def populate_dropdown(event):
    """Diese Funktion wird aufgerufen, wenn die Dropdown-Liste geöffnet wird. 
    Sie durchsucht den ausgewählten Ordner und füllt die Dropdown-Liste."""
    d = "Durchsuchen des ausgewählten Ordner"
    Log.log(logfile, d)
    folder_path = "./Konfig/Recorder/"
    if not folder_path:
        return  # Benutzer hat abgebrochen
    d = folder_path
    Log.log(logfile, d)

    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    combobox['values'] = txt_files


def on_select(event):
    global selected_file
    """Wird aufgerufen, wenn ein Element in der Dropdown-Liste ausgewählt wird."""
    selected_file = combobox.get()
    d = ("Ausgewählte Datei:", selected_file)
    Log.log(logfile, d)

def show_help():
    d = "Help wird geöffnet"
    Log.log(logfile, d)
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
    
def open_folder(folder_path):
    os.startfile(folder_path)
    
def on_confirm():
    d = "Keybindings werden geändert"
    Log.log(logfile, d)
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
    
    d = "["+value1+"] :"+" ["+value2+"]"+" Gespeichert!"
    Log.log(logfile, d)

    #print("Eingaben wurden in 'Keybindings.txt' gespeichert.")
def lade_standardwerte():
    d = "Lade Standart werte"
    Log.log(logfile, d)
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
                d = "Gelesen: "+"["+wert1 + "]"+" : " +"["+ wert2 + "]"
                Log.log(logfile, d)
                return wert1, wert2  # Gibt immer ein Tupel zurück
            else:
                raise ValueError("Datei enthält nicht genügend Werte")
    except FileNotFoundError:
        #print("Datei 'Keybindings.txt' nicht gefunden. Standardwerte werden verwendet.")
        entry1.delete(0, tk.END) 
        entry2.delete(0, tk.END) 
        entry1.insert(0, "f3")
        entry2.insert(0, "f4")
        d = "Gelesen: "+"[f3]"+" : " +"[f4]"
        Log.log(logfile, d)
        return "f3", "f4"  # Gibt Standardwerte zurück
        
    except ValueError as e:
        #print(f"Fehler beim Lesen der Werte: {e}. Standardwerte werden verwendet.")
        entry1.delete(0, tk.END) 
        entry2.delete(0, tk.END) 
        entry1.insert(0, "f3")
        entry2.insert(0, "f4")
        d = "Gelesen: "+"[f3]"+" : " +"[f4]"
        Log.log(logfile, d)
        return "f3", "f4"  # Gibt Standardwerte zurück

# Hauptfenster erstellen
d = "Hauptfenster erstellen"
Log.log(logfile, d)
fenster = ctk.CTk()
text = texte["fenster_titel"]
fenster.title(text)

#Lizenz Check Window Size
d = "Lizenz Check Window Size"
Log.log(logfile, d)
try:
    if gueltigkeiten[0] and gueltigkeiten[1]:  # Beide Lizenzen gültig
        xy = ("650x400")
        d=("Alle Lizenzen gültig Window")
    elif gueltigkeiten[0]:  # Nur Rec Lizenz gültig
        xy = ("420x400")
        d=("Rec Lizenz only Window")
    elif gueltigkeiten[1]:  # Nur DB Lizenz gültig
        fenster.geometry("430x340")
        d=("DB Lizenz only window")
    else:  # Keine Lizenz gültig (implizit, kein `try-except` nötig)
        xy = ("420x340")  # Oder eine andere Standardgröße
except:
    xy = ("650x400")  # Oder eine andere Standardgröße
    d="Keine Lizenz Window"
fenster.geometry (xy) 
Log.log(logfile, "Window size: "+xy)
Log.log(logfile, d)

fenster.iconbitmap("./Bilder/FIcon.ico")
d = "./Bilder/FIcon.ico"
Log.log(logfile, d)
# Frames erstellen (Wir verwenden jetzt CTkFrames)
recorder_frame = ctk.CTkFrame(fenster, corner_radius=10)  # Etwas abgerundete Ecken
recorder_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

keybindings_frame = ctk.CTkFrame(fenster, corner_radius=10)
keybindings_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

info_frame = ctk.CTkFrame(fenster, corner_radius=10)
info_frame.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

db_frame = ctk.CTkFrame(fenster, corner_radius=10)
db_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

automation_frame = ctk.CTkFrame(fenster, corner_radius=10)
automation_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

screenrec_frame = ctk.CTkFrame(fenster, corner_radius=10)
screenrec_frame.grid(row=1, column=2, padx=20, pady=20, sticky="nsew")

# Recorder-Elemente (Wir verwenden jetzt CTkLabels und CTkButtons)
try:
    if gueltigkeiten[0]:
        ctk.CTkLabel(recorder_frame, text=texte["recorder_label"]).grid(row=0, column=0, padx=5, pady=5)
        combobox = ttk.Combobox(recorder_frame, state="readonly")  # Combobox bleibt von ttk
        combobox.grid(row=1, column=0, padx=5, pady=5)
        combobox.bind("<Button-1>", populate_dropdown)
        combobox.bind("<<ComboboxSelected>>", on_select)

        ctk.CTkButton(recorder_frame, text=texte["rec_titel"], command=button_rec).grid(row=2, column=0, columnspan=2, padx=20, pady=5)
        ctk.CTkButton(recorder_frame, text=texte["play_title"], command=button_play).grid(row=3, column=0, columnspan=2, padx=20, pady=5)
        ctk.CTkButton(recorder_frame, text=texte["aufnahmeordner_button"], command=button_aufnahmeordner).grid(row=4, column=0, columnspan=2, padx=20, pady=5)
        ctk.CTkButton(automation_frame, text=texte["automation_button"], command=button_automation).grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    else:
        ctk.CTkLabel(recorder_frame, text=texte["rec_lizenz_abgelaufen"]).grid(row=0, column=0, padx=20, pady=50)
        ctk.CTkLabel(automation_frame, text=texte["rec_lizenz_abgelaufen"]).grid(row=0, column=0, columnspan=2, padx=20, pady=50)
except:
    ctk.CTkLabel(recorder_frame, text=texte["rec_lizenz_ungueltig"]).grid(row=0, column=0, padx=20, pady=50)
    ctk.CTkLabel(automation_frame, text=texte["rec_lizenz_ungueltig"]).grid(row=0, column=0, columnspan=2, padx=20, pady=50)

# Info-Elemente
ctk.CTkButton(info_frame, text=texte["lizenz_button"], command=button_lizenz).grid(row=1, column=0, columnspan=2, padx=20, pady=20)
ctk.CTkButton(info_frame, text=texte["hilfe_button"], command=show_help).grid(row=0, column=0, columnspan=2, padx=20, pady=20)
ctk.CTkButton(info_frame, text=texte["lizenzordner_button"], command=button_lizenzordner).grid(row=2, column=0, columnspan=2, padx=20, pady=20)

# Keybindings-Elemente (Wir verwenden jetzt CTkLabels und CTkButtons)
ctk.CTkLabel(keybindings_frame, text=texte["pause_label"]).grid(row=0, column=0, padx=5, pady=5)
entry1 = ttk.Entry(keybindings_frame)  # Entry bleibt von ttk
entry1.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(keybindings_frame, text=texte["stop_label"]).grid(row=1, column=0, padx=5, pady=5)
entry2 = ttk.Entry(keybindings_frame)
entry2.grid(row=1, column=1, padx=5, pady=5)

ctk.CTkButton(keybindings_frame, text=texte["keybindings_speichern_button"], command=on_confirm).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

ctk.CTkButton(screenrec_frame, text=texte["screenrec_button"], command=button_screenrec).grid(row=0, column=0, columnspan=2, padx=5, pady=5)
ctk.CTkButton(screenrec_frame, text=texte["csvordner_button"], command=button_videoordner).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Automation-Elemente
try:
    if gueltigkeiten[1]:
        ctk.CTkButton(db_frame, text=texte["db_remove_dublicates"], command=button_dbverarbeiten).grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        ctk.CTkButton(db_frame, text=texte["compare_csv"], command=button_ccsv).grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        ctk.CTkButton(db_frame, text=texte["csvordner_button"], command=button_csvordner).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        print("DB Lizenz Gültig!")
    else:
        ctk.CTkLabel(db_frame, text=texte["db_lizenz_abgelaufen"]).grid(row=0, column=0, padx=5, pady=50)
except:
    ctk.CTkLabel(db_frame, text=texte["db_lizenz_ungueltig"]).grid(row=0, column=0, padx=5, pady=50)
    
wert1, wert2 = lade_standardwerte()

# Fenster anzeigen
d = "Window generiert!"
Log.log(logfile, d)
fenster.mainloop()
#}
