# BolliSofts-AutoKlicker

**Autor**

Nico Bollhalder (BolliSoft)

**Lizenz**

(c) by Nico Bollhalder

**Funktionsweise**

1.  **Lizenzprüfung:**
    *   Das Programm beginnt mit der Entschlüsselung und Überprüfung der Lizenzdatei.
    *   Wenn keine Lizenzen gültig sind, wird eine entsprechende Meldung angezeigt.
    *   Die Gültigkeit der Lizenzen bestimmt, welche Funktionen verfügbar sind.

2.  **Sprachdatei laden:**
    *   Die passende Sprachdatei wird basierend auf den Windows-Spracheinstellungen geladen.
    *   Die Texte aus der Sprachdatei werden im Programm verwendet.

3.  **Hauptfenster:**
    *   Das Hauptfenster wird erstellt und in verschiedene Bereiche (Frames) unterteilt.
    *   Die verfügbaren Funktionen werden je nach Lizenzstatus angezeigt.

4.  **Recorder:**
    *   Ermöglicht die Auswahl einer Aufnahmedatei aus einem Dropdown-Menü.
    *   Die Schaltflächen "Aufnahme" und "Wiedergabe" starten die entsprechenden Aktionen.

5.  **Info:**
    *   Die Schaltfläche "Lizenz" zeigt Informationen zur Lizenz an.
    *   Die Schaltfläche "Hilfe" öffnet ein Fenster mit einer Anleitung.

6.  **Keybindings:**
    *   Ermöglicht die Anpassung der Tastenkombinationen für "Pause" und "Stopp".
    *   Die Änderungen werden in einer Konfigurationsdatei gespeichert.

7.  **Automation:**
    *   Bietet Funktionen zur Datenbankverwaltung und zum CSV-Vergleich, falls die entsprechende Lizenz gültig ist.

**Abhängigkeiten**

*   **Python-Module:**
    *   `cryptography`
    *   `datetime`
    *   `tkinter`
    *   `ttk`
    *   `messagebox`
    *   `filedialog`
    *   `tkcalendar`
    *   `customtkinter`
    *   `play`
    *   `rec`
    *   `threading`
    *   `pyautogui`
    *   `time`
    *   `keyboard`
    *   `os`
    *   `locale`
    *   `csv`
    *   `RD`
    *   `CCsv`

**Konfiguration**

*   **Lizenzdatei:** `./Lizenz/Lizenz.key` und `./Lizenz/_Lizenz.enc`
*   **Sprachdateien:** `./Sprache/xx.txt` (wobei 'xx' der Sprachcode ist)
*   **Aufnahmedateien:** `./Konfig/Recorder/`
*   **Keybindings:** `./Konfig/Keybindings/Keybindings.txt`

**Verwendung**

1.  Stellen Sie sicher, dass Sie gültige Lizenzdateien haben.
2.  Passen Sie bei Bedarf die Tastenkombinationen an.
3.  Wählen Sie eine Aufnahmedatei aus und verwenden Sie die Schaltflächen "Aufnahme" und "Wiedergabe".
4.  Nutzen Sie die Funktionen zur Datenbankverwaltung und zum CSV-Vergleich, falls verfügbar.

**Hinweis:**

*   Die Verfügbarkeit bestimmter Funktionen hängt von den gültigen Lizenzen ab.
*   Lesen Sie die Hilfe für detaillierte Anweisungen zur Verwendung des Programms.

**Fehlerbehebung**

*   Wenn das Programm nicht startet, überprüfen Sie die Lizenzdateien und deren Gültigkeit.
*   Wenn Funktionen nicht verfügbar sind, stellen Sie sicher, dass Sie die entsprechende Lizenz besitzen.
*   Bei anderen Problemen konsultieren Sie die Hilfe oder wenden Sie sich an den Entwickler.
