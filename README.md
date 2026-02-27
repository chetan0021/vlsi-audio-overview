# VLSI Audio Overview

NotebookLM-style audio overview feature for VLSI education. Students can listen to podcast-style conversations between two AI hosts (Zoya - instructor, Ravi - student) and join the conversation by asking questions.

## Features

- 🎙️ **Audio Overview**: Listen to AI-generated educational conversations about FSM Design
- 🗣️ **Voice Interaction**: Ask questions using your microphone and get responses from both AI hosts
- 💬 **Text Fallback**: Type questions if microphone is unavailable
- 📝 **Real-time Transcript**: See what's being said as you listen
- 🎯 **Contextual Responses**: AI hosts respond based on the current topic and conversation flow

## Tech Stack

### Backend
- Python 3.10+
- FastAPI
- Google Gemini 2.0 Flash API
- Coqui TTS (local, unlimited voice synthesis)
- pydub (audio processing)

### Frontend
- React 18
- TypeScript
- Vite
- Web Audio API
- MediaRecorder API

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a Python virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create `.env` file from example:
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux
```

6. Edit `.env` and add your Google Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

7. Create required directories:
```bash
mkdir audio_storage metadata_storage voice_samples\zoya voice_models
```

8. Run the backend server:
```bash
python main.py
```

Backend will be available at: http://localhost:8000

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

Frontend will be available at: http://localhost:3000

## Voice Cloning Setup

To clone the instructor's voice for Zoya:

1. Place 5-10 minutes of instructor voice samples in `backend/voice_samples/zoya/`
2. Samples should be clear WAV or MP3 files
3. Coqui TTS will use these samples for voice cloning

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Running Tests

Backend tests:
```bash
cd backend
pytest
```

Frontend tests:
```bash
cd frontend
npm test
```

### Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment variables template
│   └── .gitignore
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main React component
│   │   ├── main.tsx         # Entry point
│   │   └── index.css        # Global styles
│   ├── package.json         # Node dependencies
│   ├── vite.config.ts       # Vite configuration
│   └── .gitignore
└── README.md
```

## License

MIT
