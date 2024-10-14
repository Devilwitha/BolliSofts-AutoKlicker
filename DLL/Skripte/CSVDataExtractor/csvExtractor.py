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
    Verbessert die Extraktion relevanter Informationen aus einem Text (z.B. einer Stellenbeschreibung).

    Args:
        text (str): Der Text, aus dem die Informationen extrahiert werden sollen.

    Returns:
        dict: Ein Dictionary mit den extrahierten Informationen.
    """
    informationen = {}

    # Verbessere die Regex für Ansprechpartner (inkl. mehrteiliger Namen)
    ansprechpartner = re.findall(r"(?:Herr|Frau)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", text)
    informationen["Ansprechpartner"] = ansprechpartner[0] if ansprechpartner else None

    # Fange eine größere Vielfalt an Firmengrößen (inkl. Bereichsangaben)
    firmengroesse = re.findall(r"(\d{1,5})(?:\s*-\s*\d{1,5})?\s+(Mitarbeiter|Angestellte)", text)
    informationen["Firmengröße"] = firmengroesse[0][0] if firmengroesse else None

    # Extrahiere Standorte
    standorte = re.findall(r"(\d{1,3})\s+Standorte?", text)
    informationen["Standorte"] = standorte[0] if standorte else None

    # Telefonnummern in verschiedenen Formaten extrahieren
    telefonnummern = re.findall(r"(\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9})", text)
    informationen["Telefon"] = telefonnummern

    # E-Mail-Adressen auch bei komplexen Schreibweisen (inkl. Sonderzeichen)
    email_adressen = re.findall(r"([\w\.-]+@[\w\.-]+\.\w+)", text)
    informationen["EMail"] = email_adressen

    return informationen

def suche_unternehmen_online(firmenname):
    """
    Verbessert die Suche nach zusätzlichen Informationen über ein Unternehmen im Internet.

    Args:
        firmenname (str): Der Name des Unternehmens.

    Returns:
        dict: Ein Dictionary mit den gefundenen Informationen.
    """
    informationen = {}

    try:
        url = f"https://www.google.com/search?q={firmenname}"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.content, "html.parser")

        # Suche nach allgemeinen Links, die nicht nur auf Google-Dienste verweisen
        ergebnisse = soup.find_all("a", href=True)
        for ergebnis in ergebnisse:
            href = ergebnis['href']
            if 'http' in href and 'google' not in href:
                informationen["Webseite"] = href
                break
        else:
            informationen["Webseite"] = "Keine Webseite gefunden."
    except requests.RequestException as e:
        informationen["Fehler"] = f"Fehler bei der Online-Suche: {e}"

    return informationen

def process_data(df):
    """
    Führt die Extraktion von Informationen aus den CSV-Daten durch und zeigt den Fortschritt in Prozent an.
    
    Args:
        df (pandas.DataFrame): Der DataFrame mit den Stellenbeschreibungen und Firmennamen.

    Returns:
        pandas.DataFrame: Der DataFrame mit den extrahierten Informationen.
    """
    stellenbeschreibungen_spalte = "Stelle"  # Anpassen, falls die Spalte anders heißt
    firmenname_spalte = "Firmenname"  # Anpassen, falls die Spalte anders heißt

    total_rows = len(df)
    
    for idx, row in df.iterrows():
        df.at[idx, "Informationen"] = extrahiere_informationen(row[stellenbeschreibungen_spalte])
        df.at[idx, "Online-Informationen"] = suche_unternehmen_online(row[firmenname_spalte])
        
        # Fortschritt berechnen
        fortschritt = (idx + 1) / total_rows * 100
        print(f"Fortschritt: {fortschritt:.2f}%")

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
