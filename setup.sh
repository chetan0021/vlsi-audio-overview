#!/bin/bash

echo "Setting up VLSI Audio Overview project..."
echo ""

echo "Creating backend directories..."
cd backend
mkdir -p audio_storage
mkdir -p metadata_storage
mkdir -p voice_samples/zoya
mkdir -p voice_models

echo ""
echo "Creating .env file from example..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ".env file created. Please edit it and add your GEMINI_API_KEY"
else
    echo ".env file already exists"
fi

echo ""
echo "Backend setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env and add your GEMINI_API_KEY"
echo "2. Create Python virtual environment: python -m venv venv"
echo "3. Activate virtual environment: source venv/bin/activate"
echo "4. Install dependencies: pip install -r requirements.txt"
echo "5. Run backend: python main.py"
echo ""
echo "6. In a new terminal, navigate to frontend directory"
echo "7. Install frontend dependencies: npm install"
echo "8. Run frontend: npm run dev"
echo ""
