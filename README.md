# VLSI Audio Overview

NotebookLM-style audio overview application for VLSI education, featuring AI-generated dialogues with voice cloning.

## 🎯 Features

- **AI-Generated Dialogues**: Uses Google Gemini 2.5 Flash to generate educational conversations between two AI hosts (Zoya and Ravi)
- **Voice Cloning**: High-quality text-to-speech with voice cloning using Coqui TTS XTTS-v2
- **Interactive Audio Player**: Play/pause controls, progress tracking, and segment navigation
- **Synchronized Transcript**: Real-time transcript display that highlights the current segment
- **Question Answering**: Ask questions and get contextual responses from the AI hosts
- **Responsive UI**: Clean, modern interface built with React and TypeScript

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **Gemini Client**: Generates educational dialogues using Google's Gemini API
- **TTS Service**: Bridges Python 3.11 (main backend) and Python 3.10 (TTS engine)
- **Audio Processor**: Manages audio files and metadata
- **Script Generator**: Orchestrates dialogue generation with validation
- **Response Generator**: Handles student questions with contextual responses

### Frontend (React/TypeScript/Vite)
- **AudioPlayer Component**: Controls audio playback
- **TranscriptDisplay Component**: Shows synchronized transcript
- **Main App**: Coordinates components and API communication

## 📋 Prerequisites

- **Python 3.11** (for main backend)
- **Python 3.10** (for TTS engine - Coqui TTS doesn't support 3.11+)
- **Node.js 18+** (for frontend)
- **Google Gemini API Key** (get from https://makersuite.google.com/app/apikey)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/chetan0021/vlsi-audio-overview.git
cd vlsi-audio-overview
```

### 2. Backend Setup

#### Install Python 3.11 Environment

```bash
cd backend

# Create virtual environment with Python 3.11
py -3.11 -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Install Python 3.10 Environment (for TTS)

```bash
# Create separate virtual environment with Python 3.10
py -3.10 -m venv venv_tts

# Activate virtual environment
# Windows:
venv_tts\Scripts\activate
# Linux/Mac:
source venv_tts/bin/activate

# Install TTS dependencies
pip install TTS torch torchaudio pydantic python-dotenv

# Deactivate
deactivate
```

#### Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

#### Add Voice Samples

Place voice samples for cloning in:
- `backend/voice_samples/zoya/` - Female voice samples (MP3 format)
- `backend/voice_samples/ravi/` - Male voice samples (MP3 format)

You need at least 1-3 MP3 files (10-30 seconds each) per speaker.

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Start Backend Server

```bash
cd backend

# Activate Python 3.11 environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Start server
python -m uvicorn main:app --reload --port 8000
```

### 5. Access the Application

Open your browser and navigate to:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🎮 Usage

### Generate Audio Overview

1. Click "Generate Dialogue" button
2. Wait for dialogue generation (5-10 seconds)
3. Wait for audio synthesis (1-2 minutes per segment)
4. Use audio player controls to play/pause and navigate

### Ask Questions

1. Type your question in the input field
2. Click "Ask" or press Enter
3. View the response from Zoya and Ravi

## 📁 Project Structure

```
vlsi-audio-overview/
├── backend/
│   ├── audio_processor.py      # Audio file management
│   ├── config.py               # Configuration loader
│   ├── conversation_queue.py   # Queue management
│   ├── gemini_client.py        # Gemini API integration
│   ├── main.py                 # FastAPI application
│   ├── response_generator.py   # Question answering
│   ├── script_generator.py     # Dialogue orchestration
│   ├── tts_engine.py           # TTS engine (Python 3.10)
│   ├── tts_engine_subprocess.py # Subprocess-friendly TTS
│   ├── tts_service.py          # TTS service bridge
│   ├── requirements.txt        # Python dependencies
│   └── .env.example            # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AudioPlayer.tsx
│   │   │   └── TranscriptDisplay.tsx
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── .gitignore
└── README.md
```

## 🔧 Configuration

### Environment Variables

Edit `backend/.env`:

```env
# Google Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Audio Storage Configuration
AUDIO_STORAGE_PATH=./audio_storage
METADATA_STORAGE_PATH=./metadata_storage

# Voice Samples Configuration
VOICE_SAMPLES_PATH=./voice_samples

# TTS Configuration
TTS_SAMPLE_RATE=22050

# Application Configuration
MAX_AUDIO_DURATION=600
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
venv\Scripts\activate

# Test Gemini integration
python test_gemini.py

# Test TTS service
python test_single_segment.py

# Test complete pipeline
python test_api_quick.py
```

## ⚡ Performance Notes

- **Audio Generation**: Takes 1-2 minutes per segment (high-quality voice cloning)
- **Dialogue Generation**: Takes 5-10 seconds (Gemini API)
- **Recommended**: Generate 5-7 segments (2-minute duration) for reasonable wait times

## 🐛 Troubleshooting

### TTS Not Available

**Error**: "Audio synthesis not available (requires Python 3.10 with TTS)"

**Solution**:
1. Ensure Python 3.10 is installed
2. Create `venv_tts` with Python 3.10
3. Install TTS library in that environment
4. Check that voice samples exist in `backend/voice_samples/`

### Voice Samples Not Found

**Error**: "Zoya/Ravi voice samples not found"

**Solution**:
1. Add MP3 files to `backend/voice_samples/zoya/` and `backend/voice_samples/ravi/`
2. Ensure files are in MP3 format
3. Use 10-30 second clips with clear speech

### Backend Connection Failed

**Error**: "Backend not connected"

**Solution**:
1. Ensure backend server is running on port 8000
2. Check that Python 3.11 environment is activated
3. Verify Gemini API key is set in `.env`

## 🚧 Known Limitations

- Audio synthesis is slow (1-2 minutes per segment)
- Requires both Python 3.11 and 3.10 environments
- Voice samples must be provided by user
- No audio caching yet (regenerates on each request)

## 🔮 Future Enhancements

- [ ] Async audio generation (return immediately, generate in background)
- [ ] Audio caching to avoid regeneration
- [ ] Pre-generated common segments
- [ ] Faster TTS models
- [ ] Voice input for questions (microphone support)
- [ ] Multiple topic support
- [ ] User authentication
- [ ] Progress indicators for audio generation

## 📝 License

MIT License

## 👥 Contributors

- Chetan - Initial development

## 🙏 Acknowledgments

- Google Gemini for dialogue generation
- Coqui TTS for voice cloning
- NotebookLM for inspiration

## 📧 Contact

For questions or issues, please open an issue on GitHub: https://github.com/chetan0021/vlsi-audio-overview/issues
