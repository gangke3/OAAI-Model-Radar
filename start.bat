@echo off
echo =========================================
echo       OAAI Model-Radar - by OAAI.xyz
echo =========================================
echo.
echo Starting server on http://127.0.0.1:5000
echo.

:: Automatically open browser after 2 seconds
start "" "http://127.0.0.1:5000"

:: Start the Python server
python server.py

pause
