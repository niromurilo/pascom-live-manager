#define MyAppName "Pascom Live Manager"
#define MyAppVersion "0.1.0 Beta"
#define MyAppPublisher "Murilo Niro"
#define MyAppExeName "Pascom Live Manager.exe"

[Setup]
AppId={{8A4E6D73-1B84-4D59-92E7-6A9D2D1F0B52}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

OutputDir=Installer
OutputBaseFilename=PascomLiveManager_Setup_v0.1.0

Compression=lzma
SolidCompression=yes

WizardStyle=modern

SetupIconFile=assets\icon.ico

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Files]
Source: "dist\Pascom Live Manager\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Atalhos:"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Executar Pascom Live Manager"; Flags: nowait postinstall skipifsilent