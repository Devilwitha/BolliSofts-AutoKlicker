##########################
# Pogramm: MausReplayer  #
# Code Version: 1.2      #
# Code by BolliSoft      #
# (c) by Nico Bollhalder #
##########################

import pyautogui
import time
import keyboard

def play_actions(pathToFile, wert2):
    with open(pathToFile, "r") as f:
        aktionen = f.readlines()  # Lies alle Zeilen auf einmal in eine Liste

    for aktion in aktionen:
        aktion = aktion.strip()
        if aktion.startswith("Position"):
            x, y = map(int, aktion.split(":")[1].split(","))
            pyautogui.moveTo(x, y)
        elif aktion == "Click":
            pyautogui.click()
        elif aktion.startswith("Delay"):
            delay = float(aktion.split(":")[1])
            time.sleep(delay)
        elif aktion.startswith("Key"):
            try:
                taste = aktion.split(": ")[1]
                keyboard.press(taste)
            except:
                print(str(taste)+" Unbekannt!")
        elif aktion.startswith("End"):
            exit
        time.sleep(0.01)  
        print(aktion)  # Ausgabe der Aktion
        if keyboard.is_pressed(wert2):
            break
    

#play_actions()
