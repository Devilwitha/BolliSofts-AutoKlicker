; Skript erstellt für die Ordnerstruktur und Dateien in ordnerstruktur.txt

[Setup]
AppName=BolliSofts Autoklicker
AppVersion=0.96 -alpha
DefaultDirName={pf}\BolliSofts Autoklicker
DefaultGroupName=BolliSofts Autoklicker
AllowNoIcons=yes
OutputDir=userdocs:Inno Setup Output
OutputBaseFilename=main
Compression=lzma2
SolidCompression=yes

[Files]
; Skripte
Source: "exe.win-amd64-3.12\*"; DestDir: "{app}"; Flags: ignoreversion

; Weitere Ordner und Dateien nach Bedarf hinzufügen...
; Du kannst auch die Ordner Exports, lib und Konfig auf dieselbe Weise hinzufügen.

[Icons]
; Erstelle eine Verknüpfung für das Programm
Name: "{group}\BollisoftsAutoklicker"; Filename: "{app}\main.exe"

[Run]
; Programm nach der Installation ausführen
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,DeinProgramm}"; Flags: nowait postinstall skipifsilent
