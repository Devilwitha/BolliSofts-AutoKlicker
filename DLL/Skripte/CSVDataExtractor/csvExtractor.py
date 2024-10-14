
# Google Places API key (Replace with your actual key)
API_KEY = "AIzaSyBCIfmqSj9lgotw_a6zFgKtzl9E4Oh7mlw"


import pandas as pd
from tkinter import filedialog, Tk
import googlemaps
import threading
import requests
from bs4 import BeautifulSoup
import re


# Initialize the Google Maps Client
gmaps = googlemaps.Client(key=API_KEY)

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

def scrape_email_from_website(website_url):
    """
    Versucht, eine E-Mail-Adresse von der Webseite zu extrahieren.

    Args:
        website_url (str): Die URL der Webseite.

    Returns:
        str: Die gefundene E-Mail-Adresse oder "Nicht gefunden", falls keine E-Mail-Adresse extrahiert werden konnte.
    """
    try:
        response = requests.get(website_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Suche nach E-Mail-Adressen im Webseiteninhalt
        email_addresses = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', soup.get_text())
        if email_addresses:
            return email_addresses[0]  # Return the first found email address
        else:
            return "Nicht gefunden"
    
    except requests.RequestException as e:
        print(f"Fehler beim Abrufen der Webseite {website_url}: {e}")
        return "Nicht gefunden"

def scrape_ceo_team_and_size(website_url):
    """
    Versucht, den Geschäftsführer, das Team und die Firmengröße von der Webseite zu extrahieren.

    Args:
        website_url (str): Die URL der Webseite.

    Returns:
        dict: Ein Dictionary mit dem Geschäftsführer, Team und Firmengröße, falls gefunden.
    """
    informationen = {
        "Geschäftsführer/Ansprechpartner": "Nicht gefunden",
        "Team": "Nicht gefunden",
        "Firmengröße": "Nicht gefunden"
    }

    try:
        response = requests.get(website_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()

        # Suche nach Geschäftsführer/Ansprechpartner (Beispiele)
        ceo_match = re.findall(r"(Geschäftsführer|CEO|Manager|Ansprechpartner)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", text)
        if ceo_match:
            informationen["Geschäftsführer/Ansprechpartner"] = ceo_match[0][1]

        # Suche nach Firmengröße (Beispiele)
        size_match = re.findall(r"(\d+)\s+(Mitarbeiter|Angestellte|Beschäftigte|Personen)", text)
        if size_match:
            informationen["Firmengröße"] = f"{size_match[0][0]} {size_match[0][1]}"

        # Suche nach Team (Beispielhaft: versucht auf "Team" oder ähnliche Seiten zuzugreifen)
        team_section = soup.find_all(string=re.compile("Team|Über uns"))
        if team_section:
            informationen["Team"] = "Team gefunden"  # You could extract more details if available.
    
    except requests.RequestException as e:
        print(f"Fehler beim Abrufen der Webseite {website_url}: {e}")

    return informationen

def suche_unternehmen_online(firmenname):
    """
    Sucht nach zusätzlichen Informationen über ein Unternehmen mit der Google Places API, inklusive Telefonnummer, Webseite, Öffnungszeiten und E-Mail-Adresse.

    Args:
        firmenname (str): Der Name des Unternehmens.

    Returns:
        dict: Ein Dictionary mit den gefundenen Informationen wie Telefonnummer, Webseite, Öffnungszeiten, E-Mail, Geschäftsführer und Firmengröße.
    """
    informationen = {}
    try:
        # Sucht nach dem Unternehmen mit der Google Places API
        places_result = gmaps.places(query=firmenname)
        
        if places_result["status"] == "OK" and places_result["results"]:
            # Nimmt das erste Ergebnis als das relevante Unternehmen
            place_id = places_result["results"][0]["place_id"]
            place_details = gmaps.place(place_id=place_id)

            if place_details["status"] == "OK":
                details = place_details["result"]
                informationen["Telefonnummer"] = details.get("formatted_phone_number", "Nicht gefunden")
                informationen["Webseite"] = details.get("website", "Nicht gefunden")
                
                # Öffnungszeiten extrahieren
                opening_hours = details.get("opening_hours", {}).get("weekday_text", [])
                informationen["Öffnungszeiten"] = opening_hours if opening_hours else "Nicht gefunden"

                # Wenn eine Webseite vorhanden ist, versuche E-Mail-Adresse, Geschäftsführer und Firmengröße zu extrahieren
                if "Webseite" in informationen and informationen["Webseite"] != "Nicht gefunden":
                    informationen["E-Mail"] = scrape_email_from_website(informationen["Webseite"])
                    additional_info = scrape_ceo_team_and_size(informationen["Webseite"])
                    informationen.update(additional_info)
                else:
                    informationen["E-Mail"] = "Nicht gefunden"
                    informationen["Geschäftsführer/Ansprechpartner"] = "Nicht gefunden"
                    informationen["Firmengröße"] = "Nicht gefunden"
                    informationen["Team"] = "Nicht gefunden"
            else:
                print(f"Details nicht für {firmenname} gefunden.")
        else:
            print(f"Kein Unternehmen für {firmenname} gefunden.")

    except Exception as e:
        print(f"Fehler bei der Google Places API-Suche für {firmenname}: {e}")
    
    return informationen

def process_data(df):
    """
    Führt die Extraktion von Informationen aus den CSV-Daten durch und sucht online nach zusätzlichen Informationen.
    
    Args:
        df (pandas.DataFrame): Der DataFrame mit den Stellenbeschreibungen und Firmennamen.

    Returns:
        pandas.DataFrame: Der DataFrame mit den extrahierten Informationen.
    """
    firmenname_spalte = "Firmenname"  # Anpassen, falls die Spalte anders heißt

    # Suche nach Online-Informationen für jedes Unternehmen in der CSV-Datei
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
