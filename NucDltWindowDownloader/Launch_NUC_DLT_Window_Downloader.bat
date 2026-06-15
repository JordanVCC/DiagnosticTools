@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "VENV_PY=%SCRIPT_DIR%..\.venv\Scripts\python.exe"

if exist "%VENV_PY%" (
  "%VENV_PY%" "%SCRIPT_DIR%nuc_dlt_window_downloader.py"
) else (
  py -3 "%SCRIPT_DIR%nuc_dlt_window_downloader.py"
)

endlocal
