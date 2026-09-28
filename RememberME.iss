; Instalador do RememberME (Inno Setup 6.3+).
; Gerado pelo build.ps1, que passa a versao: ISCC /DMyAppVersion=1.0 RememberME.iss
#ifndef MyAppVersion
  #define MyAppVersion "1.0"
#endif

[Setup]
; mesmo AppId implicito do v0.5 (= AppName), para as versoes se reconhecerem
AppId=RememberME
AppName=RememberME
AppVersion={#MyAppVersion}
; o exe e' de 64 bits: instala em C:\Program Files\RememberME
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
DefaultDirName={autopf}\RememberME
DefaultGroupName=RememberME
PrivilegesRequired=admin
OutputDir=dist
OutputBaseFilename=RememberME-Setup-v{#MyAppVersion}
UninstallDisplayIcon={app}\RememberME.exe
Compression=lzma
SolidCompression=yes

[Tasks]
Name: "desktopicon"; Description: "Criar atalho no ambiente de trabalho"
Name: "autostart"; Description: "Iniciar o RememberME com o Windows"

[InstallDelete]
; restos de um build onedir antigo (v0.5), se existirem
Type: filesandordirs; Name: "{app}\_internal"

[Files]
; build --onefile: um unico exe (a base de dados fica em %APPDATA%\RememberME)
Source: "dist\RememberME.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Atalho no menu iniciar
Name: "{group}\RememberME"; Filename: "{app}\RememberME.exe"
; Atalho no desktop (opcional)
Name: "{commondesktop}\RememberME"; Filename: "{app}\RememberME.exe"; Tasks: desktopicon
; Arranque com o Windows (opcional, todos os utilizadores).
; --start arranca o servico (tray+agendador) direto, sem abrir a GUI
Name: "{commonstartup}\RememberME"; Filename: "{app}\RememberME.exe"; Parameters: "--start"; WorkingDir: "{app}"; Tasks: autostart

[Run]
; sem argumentos: garante o tray e abre a janela
Filename: "{app}\RememberME.exe"; Description: "Abrir o RememberME agora"; Flags: nowait postinstall skipifsilent

[UninstallRun]
; 1) paragem limpa; 2) se nao resultou (ou o servico e' de outro utilizador), forca
Filename: "{app}\RememberME.exe"; Parameters: "--stop"; Flags: runhidden waituntilterminated; RunOnceId: "PararServico"
Filename: "{sys}\taskkill.exe"; Parameters: "/F /T /IM RememberME.exe"; Flags: runhidden waituntilterminated; RunOnceId: "ForcarParagem"

[Code]
{ Ao atualizar: o exe em uso nao pode ser substituido. Mesma ordem do desinstalador. }
function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  Exe: String;
  R: Integer;
begin
  Exe := ExpandConstant('{app}\RememberME.exe');
  if FileExists(Exe) then
    Exec(Exe, '--stop', '', SW_HIDE, ewWaitUntilTerminated, R);
  Exec(ExpandConstant('{sys}\taskkill.exe'), '/F /T /IM RememberME.exe', '',
       SW_HIDE, ewWaitUntilTerminated, R);
  Result := '';
end;
