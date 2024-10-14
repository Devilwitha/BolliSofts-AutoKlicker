import pandas as pd
from tkinter import filedialog, Tk
import re
import requests
from bs4 import BeautifulSoup
import threading

def csvExtractor():
    """
    Öffnet einen Dateidialog zur Auswahl einer CSV-Datei und liest diese in einen Pandas DataFrame ein.

    Returns:
        pandas.DataFrame: Der DataFrame mit den Daten aus der CSV-Datei oder None, wenn keine Datei ausgewählt wurde.
    """
    # Create a hidden root window for non-blocking file dialog
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    file_path = filedialog.askopenfilename(
        defaultextension=".csv",
        filetypes=[("CSV Dateien", "*.csv"), ("Alle Dateien", "*.*")]
    )
    root.destroy()  # Destroy the root after file selection
    if file_path:
        try:
            df = pd.read_csv(file_path)
            print("Ausgewählte Datei:", file_path)
            return df
        except Exception as e:
            print(f"Fehler beim Laden der CSV-Datei: {e}")
            return None
    else:
        print("Keine Datei ausgewählt.")
        return None

def extrahiere_informationen(text):
    """
    Extrahiert relevante Informationen aus einem Text (z.B. einer Stellenbeschreibung).

    Args:
        text (str): Der Text, aus dem die Informationen extrahiert werden sollen.

    Returns:
        dict: Ein Dictionary mit den extrahierten Informationen.
    """
    informationen = {}

    # Extrahiere Ansprechpartner (Beispiel)
    ansprechpartner = re.findall(r"(?:Herr|Frau)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", text)
    informationen["Ansprechpartner"] = ansprechpartner[0] if ansprechpartner else None

    # Extrahiere Firmengröße (Beispiel)
    firmengroesse = re.findall(r"(\d+)\s+(Mitarbeiter|Angestellte)", text)
    informationen["Firmengröße"] = firmengroesse[0][0] if firmengroesse else None

    # Extrahiere Anzahl der Standorte (Beispiel)
    standorte = re.findall(r"(\d+)\s+Standorten", text)
    informationen["Standorte"] = standorte[0] if standorte else None

    # Extrahiere Telefonnummern (Beispiel)
    telefonnummern = re.findall(r"(\+\d{2}\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2})", text)
    informationen["Telefonnummern"] = telefonnummern

    # Extrahiere E-Mail-Adressen (Beispiel)
    email_adressen = re.findall(r"([\w\.-]+@[\w\.-]+\.\w+)", text)
    informationen["E-Mail-Adressen"] = email_adressen

    return informationen

def suche_unternehmen_online(firmenname):
    """
    Sucht nach zusätzlichen Informationen über ein Unternehmen im Internet.

    Args:
        firmenname (str): Der Name des Unternehmens.

    Returns:
        dict: Ein Dictionary mit den gefundenen Informationen.
    """
    informationen = {}

    try:
        # Hier könnte eine API oder Webscraping-Tool verwendet werden, um firmenname zu suchen
        # Dies ist ein Platzhalter für API-Nutzung, da Scraping Google möglicherweise gegen Nutzungsrichtlinien verstößt.
        url = f"https://www.google.com/search?q={firmenname}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Hier wird nur das erste Ergebnis als Platzhalter betrachtet
        erste_ergebnis = soup.find("a", href=True)
        if erste_ergebnis:
            response = requests.get(erste_ergebnis["href"])
            soup = BeautifulSoup(response.content, "html.parser")
            # Weitere Informationen extrahieren
            informationen["Webseite"] = erste_ergebnis["href"]
        else:
            print(f"Keine Webseite für {firmenname} gefunden.")

    except requests.RequestException as e:
        print(f"Fehler bei der Online-Suche für {firmenname}: {e}")

    return informationen

def process_data(df):
    """
    Führt die Extraktion von Informationen aus den CSV-Daten durch.
    
    Args:
        df (pandas.DataFrame): Der DataFrame mit den Stellenbeschreibungen und Firmennamen.

    Returns:
        pandas.DataFrame: Der DataFrame mit den extrahierten Informationen.
    """
    stellenbeschreibungen_spalte = "Stelle"  # Anpassen, falls die Spalte anders heißt
    firmenname_spalte = "Firmenname"  # Anpassen, falls die Spalte anders heißt

    df["Informationen"] = df[stellenbeschreibungen_spalte].apply(extrahiere_informationen)
    df["Online-Informationen"] = df[firmenname_spalte].apply(suche_unternehmen_online)
    return df

# Lade CSV-Datei und starte Extraktion in separatem Thread
def main():
    df = csvExtractor()
    if df is not None:
        df = process_data(df)
        print(df.head())
        df.to_csv("stellenangebote_mit_informationen.csv", index=False)

if __name__ == "__main__":
    thread = threading.Thread(target=main)
    thread.start()
