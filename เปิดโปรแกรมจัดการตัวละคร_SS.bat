@echo off
chcp 65001 > nul
title Ocean Saga - SS Roster Manager
cd /d "%~dp0"

echo ========================================================
echo   Ocean Saga - SS Roster Manager (GUI)
echo ========================================================
echo กำลังเปิดโปรแกรมจัดการตัวละครระดับ SS...
python roster_gui.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [เกิดข้อผิดพลาด] ไม่สามารถเปิดโปรแกรมได้ กรุณาตรวจสอบว่าติดตั้ง Python 3 แล้ว
    pause
)
