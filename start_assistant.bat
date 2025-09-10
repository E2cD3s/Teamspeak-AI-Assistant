@echo off
:: ===============================================
::  AI Companion Launcher Script
:: ===============================================

:: Set the title of the command prompt window
title AI Companion

:: Use a cool color scheme (Green text on Black background)
color 0a

echo.
echo  ===============================================
echo      AI Companion Assistant - Launching...
echo  ===============================================
echo.

:: --- Prerequisite Check: Ensure Ollama is running ---
echo Checking if Ollama service is active...
tasklist | find "ollama.exe" >nul
if errorlevel 1 (
    echo.
    echo  [ERROR] Ollama application is not running!
    echo  Please start Ollama from your Start Menu and ensure the
    echo  icon is in your system tray before running this script.
    echo.
    pause
    goto :EOF
)
echo Ollama service found.
echo.

:: --- Step 1: Navigate to the project directory ---
:: The /d switch ensures we change drives if necessary
cd /d C:\tsai

:: --- Step 2: Activate the Python virtual environment ---
echo Activating Python virtual environment...
call .venv\Scripts\activate
if not defined VIRTUAL_ENV (
    echo.
    echo  [ERROR] Failed to activate the virtual environment.
    echo  Please ensure the .venv folder exists in C:\tsai.
    echo.
    pause
    goto :EOF
)
echo Environment activated.
echo.

:: --- Step 3: Launch the main Python script ---
echo Starting the AI Assistant...
echo Please choose your AI brain in this window.
echo.
python teamspeak_ai.py

:: --- Final Step: Pause before closing ---
echo.
echo The AI Assistant script has finished.
pause