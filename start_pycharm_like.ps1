$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonExe = Join-Path $projectRoot "venv\Scripts\python.exe"
$mainScript = Join-Path $projectRoot "main.py"

if (-not (Test-Path $pythonExe)) {
    throw "Python interpreter not found: $pythonExe"
}

if (-not (Test-Path $mainScript)) {
    throw "Main script not found: $mainScript"
}

Set-Location $projectRoot
$env:PYTHONUNBUFFERED = "1"

& $pythonExe $mainScript
