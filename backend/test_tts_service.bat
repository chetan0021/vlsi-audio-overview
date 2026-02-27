@echo off
echo Testing TTS Service Integration...
echo.

REM Change to backend directory
cd /d %~dp0

REM Activate Python 3.11 virtual environment
call venv\Scripts\activate.bat

REM Run the test
python test_full_pipeline_simple.py

REM Deactivate
call venv\Scripts\deactivate.bat
pause
