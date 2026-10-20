@echo off
rem Opens the agent-enabled DLT Viewer. Pass .dlt/.dlf/.dlp files as arguments, or drag them onto this file.
set "EXE=%~dp0build\bin\dlt-viewer.exe"
if not exist "%EXE%" (
    echo DLT Viewer is not built yet. Run build.bat first.
    pause
    exit /b 1
)
start "" "%EXE%" %*
