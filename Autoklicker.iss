[Setup]
AppName=BolliSofts Autoklicker
AppVersion=0.96-alpha
DefaultDirName={userappdata}\BolliSofts Autoklicker
DefaultGroupName=BolliSofts Autoklicker
AllowNoIcons=yes
OutputDir=userdocs:Inno Setup Output
OutputBaseFilename=BolliSoftsAutoklickerInstaller
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest

[Files]
; Copy all files and subfolders
Source: "build\exe.win-amd64-3.12\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Create a shortcut for the program
Name: "{group}\BolliSofts Autoklicker"; Filename: "{app}\main.exe"
Name: "{userdesktop}\BolliSofts Autoklicker"; Filename: "{app}\main.exe"

[Run]
; Run the program after installation
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,BolliSofts Autoklicker}"; Flags: nowait postinstall skipifsilent
