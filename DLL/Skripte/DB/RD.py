##################################
# Pogramm: RD Pogramm            #
# Code Version: 1.1              #
# Code by BolliSoft              #
# (c) by Nico Bollhalder & Lenny #
##################################

import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import locale
import os

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

def remove_duplicates():
    # Open file dialog to choose the CSV file to clean
    input_csv = filedialog.askopenfilename(title="CSV wählen",initialdir="~/Downloads", filetypes=[("CSV Dateien", "*.csv")])
    
    if os.path.exists("mergeReady.csv"):
        os.remove("mergeReady.csv")
        print("Vorhandene 'mergeReady.csv' gelöscht.")

    if not input_csv:
        print("Bitte wähle eine CSV-Datei aus.")
        return

    try:
        # Column to check for duplicates
        duplicate_column = 'Firmenname'

        # Read the input CSV and remove duplicates
        with open(input_csv, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            rows = list(reader)

            # Keep track of seen values to remove duplicates
            seen = set()
            unique_rows = []

            for row in rows:
                if row[duplicate_column] not in seen:
                    unique_rows.append(row)
                    seen.add(row[duplicate_column])

        # Open file dialog to save the cleaned CSV
        output_csv = "./Exports/CSV/mergeReady.csv"
        if not output_csv:
            messagebox.showwarning(texte["abort"], texte["save_abort"])
            print("Speichern abgebrochen.")
            return

        # Write the cleaned data to the output CSV
        with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(unique_rows)

        # Display result message
        messagebox.showinfo(texte["erfolgreich_title"], f"Datei erfolgreich bereinigt und gespeichert! Vorher: {len(rows)} Zeilen, Nachher: {len(unique_rows)} Zeilen")
        #print()

    except Exception as e:
        messagebox.showwarning(texte["error"], texte["error_01"].format(e))
        print(f"Ein Fehler ist aufgetreten: {e}")


