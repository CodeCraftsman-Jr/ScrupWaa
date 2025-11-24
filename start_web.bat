@echo off
REM Kill any existing Python web app processes
echo Stopping any running web apps...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq web_app*" 2>nul

echo.
echo Starting Universal Phone Scraper Web Interface...
echo.
echo Opening browser to http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the web app
C:/Users/Vasanthan/AppData/Local/Programs/Python/Python310/python.exe web_app.py

pause