import time
import schedule
import threading
from tkinter import filedialog
import sys
sys.path.append('../ScreenRec')
sys.path.append('../exeRunningChecker')
import play
import erc

stop_flag = threading.Event()  # Definiere stop_flag global


def lade_standardwerte():
    global wert1, wert2
    try:
        with open("../../..//Konfig/Keybindings/Keybindings.txt", "r") as f:
            zeilen = f.readlines()
            if len(zeilen) >= 2:
                wert1 = zeilen[0].split(":")[1].strip()
                wert2 = zeilen[1].split(":")[1].strip()
                return wert2  # Gibt immer ein Tupel zurück
            else:
                raise ValueError("Datei enthält nicht genügend Werte")
    except FileNotFoundError:
        #print("Datei 'Keybindings.txt' nicht gefunden. Standardwerte werden verwendet.")
        return "f4"  # Gibt Standardwerte zurück
        
    except ValueError as e:
        #print(f"Fehler beim Lesen der Werte: {e}. Standardwerte werden verwendet.")
        return "f4"  # Gibt Standardwerte zurück
    
def meine_methode(input_txt, wert2):
    if input_txt is not None and wert2 is not None:
        t = threading.Thread(target=play.play_actions, args=(input_txt, wert2)) # Übergebe 'zeit' als Argument
        t.start()
    else:
        print("Fehler: input_txt oder wert2 ist None. play_actions kann nicht ausgeführt werden.")

def schedule_task(zeit1, input_txt):
    stunde = str(zeit1)
    zeit_formatiert = stunde
    wert2 = lade_standardwerte()
    schedule.every().day.at(stunde).do(meine_methode, input_txt, wert2)
    print("Sheduele gesetzt auf: " + stunde)

    while not stop_flag.is_set():  # Führe die Schleife aus, bis stop_flag gesetzt wird
        schedule.run_pending()
        if erc.isrunning_prozess("main.exe"):
            print("Automation is Running!")
            time.sleep(1)  # Überprüfe jede Sekunde auf anstehende Aufgaben
        else:
            erc.beende_prozess("main.exe")

# Starte den Scheduler in einem separaten Thread
def start_schedule(zeit1):
    global input_txt, stop_flag
    stop_flag = threading.Event()
    print(zeit1)
    input_txt = filedialog.askopenfilename(title="Txt wählen",initialdir="../../..Konfig/Recorder/", filetypes=[("Text Dateien", "*.txt")])
    global t  # Damit wir den Thread global zugreifen können
    t = threading.Thread(target=schedule_task, args=(zeit1, input_txt)) # Übergebe 'zeit' als Argument
    t.start()
    print("Automation wurde gestartet")

# Beende den Thread
def stop_schedule():
    global t, stop_flag  # Greife auf die globalen Variablen zu
    stop_flag.set()
    t.join()
    print("Automation wurde gestopt")
