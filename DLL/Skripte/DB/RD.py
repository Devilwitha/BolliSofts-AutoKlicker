import csv
import tkinter as tk
from tkinter import filedialog

def remove_duplicates():
    # Open file dialog to choose the CSV file to clean
    input_csv = filedialog.askopenfilename(title="Wähle die Eingabe-CSV-Datei aus")

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
        output_csv = filedialog.asksaveasfilename(defaultextension=".csv", title="Speichere die bereinigte CSV-Datei", filetypes=[("CSV-Dateien", "*.csv")])
        if not output_csv:
            print("Speichern abgebrochen.")
            return

        # Write the cleaned data to the output CSV
        with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(unique_rows)

        # Display result message
        print(f"Datei erfolgreich bereinigt und gespeichert! Vorher: {len(rows)} Zeilen, Nachher: {len(unique_rows)} Zeilen")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

