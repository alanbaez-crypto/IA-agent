$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
if (-not (Test-Path '.venv\Scripts\python.exe')) {
    & py -3.12 -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Instala Python 3.12 de python.org con el lanzador py.' }
}
$python = '.\.venv\Scripts\python.exe'
& $python -c "import sys; assert sys.version_info[:2] == (3, 12), 'Se requiere Python 3.12'"
if ($LASTEXITCODE -ne 0) { throw 'El entorno virtual no usa Python 3.12.' }
& $python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Falló la instalación. Revisa conexión, certificados y requirements.txt.' }
& $python -m pip check
if ($LASTEXITCODE -ne 0) { throw 'Dependencias incompatibles.' }
Write-Host 'Instalación completada. Ejecuta scripts\test.ps1 y scripts\run.ps1.'
