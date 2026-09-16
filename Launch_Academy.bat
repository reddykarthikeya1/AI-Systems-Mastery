@echo off
title AI & Systems Academy — Karthikeya Reddy
color 0B

echo ================================================================================
echo    AI ^& SYSTEMS ENGINEERING ACADEMY — BY KARTHIKEYA REDDY
echo    Ultra Gold Standard 12-Course Interactive Learning Platform
echo ================================================================================
echo.
echo [*] Checking Python environment...

python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    color 0C
    echo [!] Python is not detected in your system PATH.
    echo [!] Please install Python 3.10 or newer from https://www.python.org/
    echo [!] Be sure to check the box "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [✓] Python detected successfully.
echo [*] Launching Academy Platform on http://localhost:8000 ...
echo [*] Your default browser will open automatically.
echo.

python start_platform.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] Application exited with code %ERRORLEVEL%.
    pause
)
