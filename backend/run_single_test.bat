@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
python test_single_segment.py
pause
