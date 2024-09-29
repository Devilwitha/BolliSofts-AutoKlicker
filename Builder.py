import os
import shutil
from cx_Freeze import setup, Executable

# Projektverzeichnis (ändern, falls nötig)
project_dir = os.path.dirname(os.path.abspath(__file__))

# Build-Verzeichnis
build_dir = os.path.join(project_dir, "build")


# Falls das Build-Verzeichnis existiert, lösche es, um sauber zu starten
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)

# Definiere die zu inkludierenden Dateien und Ordner
include_files = [
    os.path.join(project_dir, "Changelog.txt"),
    os.path.join(project_dir, "DLL"),
    os.path.join(project_dir, "Konfig"),
    os.path.join(project_dir, "Lizenz"),
    os.path.join(project_dir, "Bilder"),
    os.path.join(project_dir, "Sprache"),
    os.path.join(project_dir, "Exports"),
    os.path.join(project_dir, "Logs"),
]

# Definiere die Pakete, die inkludiert werden sollen
packages = [
    "babel", 
    "cryptography", 
    "pyaes", 
    "tkcalendar", 
    "keyboard", 
    "pyautogui", 
    "pynput",
    "six"  # Füge weitere Pakete hinzu, falls nötig
]

# cx_Freeze Setup
setup(
    name="Dein Programmname",  # Ändere dies zu deinem gewünschten Programmnamen
    version="1.0",  # Ändere die Versionsnummer nach Bedarf
    description="Beschreibung deines Programms",  # Füge eine kurze Beschreibung hinzu
    options={
        "build_exe": {
            "packages": packages,
            "include_files": include_files,
            #"images": os.path.join(project_dir, "Bilder", "FIcon.ico")  # Pfad zu deinem Icon
        }
    },
    executables=[Executable("main.py", base="Win32GUI", icon=os.path.join(project_dir, "Bilder", "FIcon.ico"))] 

)
