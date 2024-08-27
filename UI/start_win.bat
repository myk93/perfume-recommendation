@echo off
REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b
)

REM Check if pip is installed
pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo pip is not installed. Please install pip and try again.
    pause
    exit /b
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Open the web page in the default browser
start "" "http://127.0.0.1:5000/static/index.html"

REM Run the server
echo Starting the server...
start "" python server.py

REM Wait for the server to start (adjust the timeout if necessary)
timeout /t 3 > nul



