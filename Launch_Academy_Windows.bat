@echo off
setlocal EnableDelayedExpansion
title AI & Systems Academy - Karthikeya Reddy
color 0B

echo ================================================================================
echo    AI ^& SYSTEMS ENGINEERING ACADEMY - BY KARTHIKEYA REDDY
echo    Ultra Gold Standard 12-Course Interactive Learning Platform
echo ================================================================================
echo.

:Detect
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

:: If not found, check if winget is available for 1-click automatic installation
winget --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo.
    echo [!] Python 3.10+ was not automatically detected on this computer.
    echo [*] Windows Package Manager (winget) is available!
    echo [*] We can automatically install Python 3.11 for you now.
    echo.
    set /p "AUTO_INSTALL=Would you like to install Python 3.11 automatically via winget? (Y/N): "
    if /i "!AUTO_INSTALL!"=="Y" (
        echo.
        echo [*] Installing Python 3.11 via winget...
        echo [*] (If Windows User Account Control prompts you, click 'Yes' to allow)
        winget install -e --id Python.Python.3.11 --accept-source-agreements --accept-package-agreements
        echo.
        echo [*] Installation finished. Detecting newly installed Python environment...
        timeout /t 2 /nobreak >nul
        goto :Detect
    )
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
cd /d "%~dp0"
echo [OK] Python runtime detected: %PY_CMD%
echo [*] Launching Academy Platform in Standalone Application Mode...
echo [*] A dedicated application window will open automatically.
echo [*] Close the window or press Ctrl+C to exit.
echo.

%PY_CMD% start_platform.py %*

if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] Application exited with code %ERRORLEVEL%.
    pause
)
