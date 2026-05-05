@echo off
cd /d "%~dp0"
pythonw dlt_searcher_gui.py
if %errorlevel% neq 0 (
    python dlt_searcher_gui.py
    pause
)
