@echo off
cd /d "%~dp0"
title Ocean Saga - SS Roster Manager

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    start "" python "โปรแกรม\roster_gui.py"
    exit /b 0
)

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    start "" py "โปรแกรม\roster_gui.py"
    exit /b 0
)

echo [ERROR] Python not found in system PATH.
pause
