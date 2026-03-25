@echo off
cd /d "%~dp0"

:: Try pythonw first (hides the console window for a clean GUI experience)
where pythonw >nul 2>&1
if %errorlevel%==0 (
    start "" pythonw "%~dp0dtc_exovision_graph.py"
) else (
    python "%~dp0dtc_exovision_graph.py"
)
