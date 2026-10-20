@echo off
setlocal
cd /d "%~dp0"
if exist "..\.venv\Scripts\python.exe" (
    "..\.venv\Scripts\python.exe" app.py
) else (
    py -3 app.py
)
if errorlevel 1 (
    echo Zeta Job Alarm could not start. Python 3.10 or newer with Tk is required.
    pause
)