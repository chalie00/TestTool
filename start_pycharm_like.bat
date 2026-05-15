@echo off
setlocal

cd /d "%~dp0"
set "PYTHONUNBUFFERED=1"

if not exist "venv\Scripts\python.exe" (
    echo Python interpreter not found: venv\Scripts\python.exe
    exit /b 1
)

if not exist "main.py" (
    echo Main script not found: main.py
    exit /b 1
)

"venv\Scripts\python.exe" "main.py"
