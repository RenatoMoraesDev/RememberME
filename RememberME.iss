[Setup]
AppName=RememberME
AppVersion=0.5
DefaultDirName={pf}\RememberME
DefaultGroupName=RememberME
OutputDir=.
OutputBaseFilename=RememberME
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\RememberME\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Atalho no menu iniciar
Name: "{group}\RememberME"; Filename: "{app}\RememberME.exe"

; Atalho no desktop
Name: "{commondesktop}\RememberME"; Filename: "{app}\RememberME.exe"

; AUTO-START GLOBAL (funciona sempre, mesmo instalando como administrador)
; --start arranca o servico (tray+agendador) direto, sem abrir a GUI
Name: "{commonstartup}\RememberME"; Filename: "{app}\RememberME.exe"; Parameters: "--start"; WorkingDir: "{app}"

[Run]
; Executar após instalar (arranca o servico, tray+agendador)
Filename: "{app}\RememberME.exe"; Parameters: "--start"; Flags: nowait postinstall skipifsilent