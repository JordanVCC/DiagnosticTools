@echo off
setlocal
cd /d "%~dp0"
set "LOG_DIR=%~dp0logs"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "TS=%%i"
set "OUT_LOG=%LOG_DIR%\launcher_%TS%.log"

echo Launching DTC correlator... > "%OUT_LOG%"
echo Working dir: %CD% >> "%OUT_LOG%"
echo Python path check: >> "%OUT_LOG%"
where python >> "%OUT_LOG%" 2>&1

python app.py >> "%OUT_LOG%" 2>&1
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
	echo.
	echo Application exited with error code %EXIT_CODE%.
	echo See log: "%OUT_LOG%"
	type "%OUT_LOG%"
	echo.
	pause
)
endlocal
