@echo off
set BUILD_DIR=.\build\exe.win-amd64-3.12

python Builder.py build

if %errorlevel% == 0 (
    echo Build erfolgreich. Aufräumen...

    REM Lösche Dateien und Ordner, die nach dem Build nicht mehr benötigt werden (ohne Bestätigung)
    if exist "%BUILD_DIR%\Konfig\Recorder\*" (
        del /q "%BUILD_DIR%\Konfig\Recorder\*"
    )
    if exist "%BUILD_DIR%\Konfig\Keybindings\*" (
        del /q "%BUILD_DIR%\Konfig\Keybindings\*"
    )
    if exist "%BUILD_DIR%\Lizenz\*" (
        del /q "%BUILD_DIR%\Lizenz\*"
    )
) else (
    echo Fehler beim Bauen der Anwendung. Löschvorgänge wurden nicht ausgeführt.
    REM Hier könntest du weitere Fehlerbehandlung hinzufügen, um mehr Informationen über den Fehler zu erhalten.
)