@echo off
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "PARENT_DIR=%SCRIPT_DIR%.."
set "VENV_DIR=%PARENT_DIR%\.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "REQUIREMENTS=%SCRIPT_DIR%requirements.txt"

echo Checking environment...

REM Check if venv exists
if not exist "%VENV_PY%" (
    echo Creating virtual environment...
    py -3 -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo Error: Failed to create virtual environment.
        echo Please ensure Python 3.8+ is installed.
        pause
        exit /b 1
    )
)

REM Install requirements if they haven't been installed
echo Checking dependencies...
"%VENV_PY%" -m pip install -q -r "%REQUIREMENTS%"
if errorlevel 1 (
    echo Error: Failed to install dependencies.
    echo Please check your internet connection.
    pause
    exit /b 1
)

REM Launch the application
echo Checking sign-in browser...
"%VENV_PY%" -m playwright install chromium
if errorlevel 1 (
    echo Error: Failed to install the NUC sign-in browser.
    pause
    exit /b 1
)

echo Launching NUC DLT Window Downloader...
"%VENV_PY%" "%SCRIPT_DIR%nuc_dlt_window_downloader.py"

endlocal
