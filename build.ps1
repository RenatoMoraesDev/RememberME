# Gera o exe portatil e o instalador de uma vez.
#   powershell -ExecutionPolicy Bypass -File build.ps1 -Versao 1.0
# Resultado em dist\: RememberME-Portable-v<Versao>.exe e RememberME-Setup-v<Versao>.exe
param([string]$Versao = "1.0")
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# 1. exe unico (--onefile, definido no RememberME.spec)
uv run pyinstaller --noconfirm --clean RememberME.spec
if ($LASTEXITCODE) { throw "PyInstaller falhou" }

# 2. portatil = copia renomeada do mesmo exe
Copy-Item dist\RememberME.exe "dist\RememberME-Portable-v$Versao.exe" -Force

# 3. instalador
$iscc = (Get-Command ISCC.exe -ErrorAction SilentlyContinue).Source
if (-not $iscc) {
    $iscc = @("$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe",
              "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
              "$env:ProgramFiles\Inno Setup 6\ISCC.exe") |
            Where-Object { Test-Path $_ } | Select-Object -First 1
}
if (-not $iscc) { throw "ISCC.exe (Inno Setup 6) nao encontrado. Instale com: winget install JRSoftware.InnoSetup" }
& $iscc "/DMyAppVersion=$Versao" RememberME.iss
if ($LASTEXITCODE) { throw "Inno Setup falhou" }

Write-Host "Pronto:" -ForegroundColor Green
Get-ChildItem dist\RememberME-*-v$Versao.exe | Format-Table Name, Length
