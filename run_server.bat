@echo off
REM One-click launcher for Windows: activates common virtualenvs and runs Flask app
SETLOCAL ENABLEDELAYEDEXPANSION

:: Look for common virtual environment folders and activate the first found
IF EXIST "env\Scripts\activate.bat" (
  call "env\Scripts\activate.bat"
) ELSE IF EXIST "venv\Scripts\activate.bat" (
  call "venv\Scripts\activate.bat"
) ELSE IF EXIST "medical_env\Scripts\activate.bat" (
  call "medical_env\Scripts\activate.bat"
) ELSE (
  REM No virtualenv detected; continuing with system Python
)

:: Set Flask env vars and run the app. Uses python -m flask to ensure the correct interpreter is used.
set FLASK_APP=Main.py
set FLASK_ENV=development

:: Start Flask in a new window so the batch file can continue and open browser
start "Flask Server" cmd /k "python -m flask run"

:: Wait a moment then open the default browser to the local URL
timeout /t 2 /nobreak >nul
start http://127.0.0.1:5000/

ENDLOCAL
