@echo off
echo Setting up VLSI Audio Overview project...
echo.

echo Creating backend directories...
cd backend
if not exist "audio_storage" mkdir audio_storage
if not exist "metadata_storage" mkdir metadata_storage
if not exist "voice_samples\zoya" mkdir voice_samples\zoya
if not exist "voice_models" mkdir voice_models

echo.
echo Creating .env file from example...
if not exist ".env" (
    copy .env.example .env
    echo .env file created. Please edit it and add your GEMINI_API_KEY
) else (
    echo .env file already exists
)

echo.
echo Backend setup complete!
echo.
echo Next steps:
echo 1. Edit backend\.env and add your GEMINI_API_KEY
echo 2. Create Python virtual environment: python -m venv venv
echo 3. Activate virtual environment: venv\Scripts\activate
echo 4. Install dependencies: pip install -r requirements.txt
echo 5. Run backend: python main.py
echo.
echo 6. In a new terminal, navigate to frontend directory
echo 7. Install frontend dependencies: npm install
echo 8. Run frontend: npm run dev
echo.
pause
