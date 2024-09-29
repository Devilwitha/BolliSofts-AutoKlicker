import os
from datetime import datetime

def erstelle_log_datei(praefix="Logs"):
    """
    Erstellt eine neue Log-Datei mit einem eindeutigen Namen basierend auf Datum und Uhrzeit.

    Args:
        praefix: Ein optionaler Präfix für den Dateinamen (Standard: "MeineLogs").

    Returns:
        Den vollständigen Pfad zur erstellten Log-Datei.
    """

    # Aktuelles Datum und Uhrzeit im gewünschten Format
    jetzt = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Dateiname mit Präfix, Datum und Uhrzeit
    dateiname = f"{praefix}_{jetzt}.txt"

    # Pfad zu den übergeordneten Ordnern erstellen (falls nicht vorhanden)
    ordnerpfad = "./Logs/" 
    os.makedirs(ordnerpfad, exist_ok=True)

    # Vollständiger Pfad zur Log-Datei
    dateipfad = os.path.join(ordnerpfad, dateiname)

    # Leere Datei erstellen (um sicherzustellen, dass sie existiert)
    open(dateipfad, "w", encoding="utf-8").close()

    return dateipfad

def log(dateipfad, text):
    """
    Schreibt Text in eine bestehende Log-Datei und nummeriert jeden Eintrag.

    Args:
        dateipfad: Der vollständige Pfad zur Log-Datei.
        text: Der Text, der in die Log-Datei geschrieben werden soll.
    """
    
    # Eintragsnummer aus der Datei lesen oder initialisieren
    try:
        with open(dateipfad, "r", encoding="utf-8") as f:
            letzte_zeile = f.readlines()[-1]
            eintragsnummer = int(letzte_zeile.split(".")[0]) + 1 
    except (FileNotFoundError, IndexError, ValueError):
        eintragsnummer = 1

    # Text mit Eintragsnummer in die Datei schreiben (im Append-Modus)
    with open(dateipfad, "a", encoding="utf-8") as f:
        f.write(f"{eintragsnummer}. {text}\n") 
    print(str(text))

# Beispielverwendung
#log_dateipfad = erstelle_log_datei(praefix="MeinProjekt")
#log(log_dateipfad, "Dies ist ein Testeintrag in der Log-Datei.")
#log(log_dateipfad, "Dies ist ein weiterer Eintrag.")