##################################
# Pogramm: CCsv skript           #
# Code Version: 1.1              #
# Code by BolliSoft              #
# (c) by Nico Bollhalder & Lenny #
##################################

import csv
import tkinter as tk
from tkinter import filedialog, messagebox
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

def remove_bom(header):
    """ Remove BOM from the header if present """
    return [col.lstrip('\ufeff') for col in header]

def compare_and_remove_duplicates():
    # File selection dialogs for both CSV files
    file1_path = filedialog.askopenfilename(title="Wähle die CRM Datei aus",initialdir="~/Downloads", filetypes=[("CSV Dateien", "*.csv")])
    file2_path = filedialog.askopenfilename(title="Wähle die Neuen Leads aus",initialdir="./Exports/CSV/", filetypes=[("CSV Dateien", "*.csv")])
    if os.path.exists("cleanCSV.csv"):
        os.remove("cleanCSV.csv")
        print("Vorhandene 'cleanCSV.csv' gelöscht.")

    if not file1_path or not file2_path:
        messagebox.showwarning(texte["warning_sign"], texte["select_two_files"])
        print("Bitte wähle zwei Dateien aus.")
        return

    try:
        # Read CSV file 1 (the reference file to compare against)
        with open(file1_path, 'r', newline='', encoding='utf-8') as file1:
            reader1 = csv.reader(file1)
            header1 = next(reader1, None)  # Read the header if exists
            header1 = remove_bom(header1)  # Remove BOM from header

            if header1 and "Firmenname" in header1:
                index1 = header1.index("Firmenname")  # Find the index of the "Firmenname" column
            else:
                
                print('Header "Firmenname" nicht gefunden in Datei 1.')
                return

            file1_rows = {tuple(row[index1] for index1 in range(len(header1))) for row in reader1}  # Store rows as a set for fast lookup

        # Read CSV file 2 (the file that will have entries removed if they exist in file 1)
        with open(file2_path, 'r', newline='', encoding='utf-8') as file2:
            reader2 = csv.reader(file2)
            header2 = next(reader2, None)  # Read the header if exists
            header2 = remove_bom(header2)  # Remove BOM from header

            if header2 and "Firmenname" in header2:
                index2 = header2.index("Firmenname")  # Find the index of the "Firmenname" column
            else:
                print('Header "Firmenname" nicht gefunden in Datei 2.')
                return

            file2_rows = [tuple(row) for row in reader2]  # Store rows in a list to maintain order

        # Find and remove rows from file 2 that are found in file 1 based on "Firmenname"
        file2_unique_rows = [row for row in file2_rows if row[index2] not in {r[index1] for r in file1_rows}]
        removed_rows = [row for row in file2_rows if row[index2] in {r[index1] for r in file1_rows}]  # Track removed rows

        # Save the updated CSV file without the entries from file 1
        save_path = "./Exports/CSV/cleanCSV.csv"
        if not save_path:
            messagebox.showwarning(texte["abort"], texte["save_abort"])
            print("Speichern abgebrochen.")
            return
    
        with open(save_path, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            if header2:
                writer.writerow(header2)  # Write the header back if it existed
            writer.writerows(file2_unique_rows)

        # Display removed rows
        if removed_rows:
            # Update the result label with information about removed rows
            messagebox.showinfo(texte["erfolgreich_title"], texte["save_erfolg"].format(len(file2_rows), len(file2_unique_rows), len(removed_rows)))
            print(f"Datei erfolgreich gespeichert!\nVorher: {len(file2_rows)} Zeilen, Nachher: {len(file2_unique_rows)}\n\nEntfernte Zeilen: {len(removed_rows)}")

    except Exception as e:
        messagebox.showwarning(texte["error"], texte["error_01"].format(e))
        print(f"Ein Fehler ist aufgetreten: {e}")
