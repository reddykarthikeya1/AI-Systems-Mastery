@echo off
title AI & Systems Academy - Karthikeya Reddy
color 0B

echo ================================================================================
echo    AI & SYSTEMS ENGINEERING ACADEMY - BY KARTHIKEYA REDDY
echo    Ultra Gold Standard 12-Course Interactive Learning Platform
echo ================================================================================
echo.
echo [*] Locating Python runtime environment...

set "PY_CMD="

:: 1. Check if 'python' is in PATH
python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=python"
    goto :Found
)

:: 2. Check Windows Python Launcher 'py'
py -3 --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=py -3"
    goto :Found
)

:: 3. Check AppData Local Programs
for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do (
    if exist "%%D\python.exe" (
        set "PY_CMD=%%D\python.exe"
        goto :Found
    )
)

:: 4. Check Root Drive Python
for /d %%D in (C:\Python3*) do (
    if exist "%%D\python.exe" (
        set "PY_CMD=%%D\python.exe"
        goto :Found
    )
)

:: 5. Check Program Files
for /d %%D in ("%ProgramFiles%\Python3*") do (
    if exist "%%D\python.exe" (
        set "PY_CMD=%%D\python.exe"
        goto :Found
    )
)

:: 6. Check WindowsApps Store Python
if exist "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" (
    set "PY_CMD=%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe"
    goto :Found
)

:: If not found, alert user
color 0C
echo.
echo [!] Python 3.10+ was not automatically detected on this computer.
echo [!] To run the Academy, please install Python from:
echo     https://www.python.org/downloads/
echo [!] (Check the box "Add Python to PATH" during installation)
echo.
pause
exit /b 1

:Found
echo [OK] Python runtime detected: %PY_CMD%
echo [*] Launching Academy Platform on http://localhost:8000 ...
echo [*] Your default browser will open automatically.
echo.

%PY_CMD% start_platform.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] Application exited with code %ERRORLEVEL%.
    pause
)
