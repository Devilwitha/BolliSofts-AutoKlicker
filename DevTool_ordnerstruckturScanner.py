import os
import tkinter as tk
from tkinter import filedialog

def print_directory_structure(root_dir, file_handle, indent=""):
    """
    Gibt die Ordnerstruktur eines angegebenen Ordners rekursiv in eine Datei aus.

    Args:
        root_dir: Der Pfad zum Stammverzeichnis, dessen Struktur ausgegeben werden soll.
        file_handle: Das Dateihandle der geöffneten Textdatei.
        indent: Ein String, der zur Einrückung der Ausgabe verwendet wird.
    """
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            file_handle.write(f"{indent}{item}/\n") 
            print_directory_structure(item_path, file_handle, indent + "  ") 
        else:
            file_handle.write(f"{indent}{item}\n")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Versteckt das Hauptfenster

    folder_path = filedialog.askdirectory(title="Wählen Sie einen Ordner aus")

    if folder_path:
        with open("ordnerstruktur.txt", "w", encoding="utf-8") as f:
            print_directory_structure(folder_path, f)
        print("Die Ordnerstruktur wurde in 'ordnerstruktur.txt' gespeichert.")
    else:
        print("Kein Ordner ausgewählt.")
