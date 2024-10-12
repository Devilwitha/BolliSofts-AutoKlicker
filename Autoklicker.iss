; Skript erstellt für die Ordnerstruktur und Dateien in ordnerstruktur.txt

[Setup]
AppName=BolliSofts Autoklicker
AppVersion=0.96 -alpha
DefaultDirName={pf}\BolliSofts Autoklicker
DefaultGroupName=BolliSofts Autoklicker
AllowNoIcons=yes
OutputDir=userdocs:Inno Setup Output
OutputBaseFilename=BolliSoftsAutoklickerInstaller
Compression=lzma2
SolidCompression=yes

[Files]
; Kopiere alle Dateien und Unterordner
Source: "build\exe.win-amd64-3.12\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Weitere Ordner und Dateien nach Bedarf hinzufügen...

[Icons]
; Erstelle eine Verknüpfung für das Programm
Name: "{group}\BolliSofts Autoklicker"; Filename: "{app}\main.exe"

[Run]
; Programm nach der Installation ausführen
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,BolliSofts Autoklicker}"; Flags: nowait postinstall skipifsilent
