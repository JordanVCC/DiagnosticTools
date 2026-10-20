@echo off
rem Builds DLT Viewer (+ agent plugin) with MSVC 2022 and Qt 6.8.3, matching the official Windows release.
setlocal
set "ROOT=%~dp0"
set "QTDIR=%USERPROFILE%\Qt\6.8.3\msvc2022_64"
set "VCVARS=C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

if not exist "%VCVARS%" goto :no_msvc
if not exist "%QTDIR%\bin\qmake.exe" goto :no_qt

call "%VCVARS%" >nul || exit /b 1
set "PATH=%ROOT%.venv\Scripts;%QTDIR%\bin;%PATH%"

cmake -S "%ROOT%dlt-viewer" -B "%ROOT%build" -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="%QTDIR%" "-DCMAKE_PROJECT_dlt-viewer_INCLUDE=%ROOT%plugin\inject.cmake" || exit /b 1
cmake --build "%ROOT%build" || exit /b 1

rem Make the build runnable in place: copy Qt runtime DLLs next to the executable.
windeployqt --release --no-translations --no-system-d3d-compiler --no-opengl-sw "%ROOT%build\bin\dlt-viewer.exe" >nul || exit /b 1
rem Plugins can need Qt modules the executable doesn't (e.g. PrintSupport for filetransferplugin).
for %%P in ("%ROOT%build\bin\plugins\*.dll") do (
    windeployqt --release --no-translations --no-system-d3d-compiler --no-opengl-sw --dir "%ROOT%build\bin" --plugindir "%ROOT%build\bin" "%%~fP" >nul || exit /b 1
)
rem Silent (-s) command-line mode needs the offscreen platform, which windeployqt skips.
copy /y "%QTDIR%\plugins\platforms\qoffscreen.dll" "%ROOT%build\bin\platforms\" >nul || exit /b 1
echo.
echo Build OK: %ROOT%build\bin\dlt-viewer.exe
exit /b 0

:no_msvc
echo MSVC Build Tools not found: "%VCVARS%"
exit /b 1

:no_qt
echo Qt not found: "%QTDIR%"
exit /b 1
