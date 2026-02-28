@echo off
cd /d "%~dp0"
echo =========================================
echo       OAAI Model-Radar - by OAAI.xyz
echo =========================================
echo.
echo Starting server on http://127.0.0.1:5000
echo.

:: Start the Python server
python server.py

pause
