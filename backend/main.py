"""
VLSI Audio Overview - FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sys

from config import get_config
from gemini_client import get_gemini_client
from audio_processor import get_audio_processor
from script_generator import get_script_generator
from response_generator import get_response_generator
from fastapi.responses import FileResponse
from fastapi import UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
import os
import time

# Validate configuration on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager - runs on startup and shutdown"""
    # Startup: Validate configuration
    try:
        config = get_config()
        print("✅ Configuration loaded successfully")
        print(f"✅ Gemini API Key: {config.gemini_api_key[:10]}...{config.gemini_api_key[-4:]}")
        print(f"✅ Audio storage: {config.audio_storage_path}")
        print(f"✅ Voice samples: {config.voice_samples_path}")
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n⚠️  Please check your .env file and ensure all required API keys are set.")
        print("   Required: GEMINI_API_KEY")
        sys.exit(1)
    
    yield
    
    # Shutdown: Cleanup if needed
    print("Shutting down...")

app = FastAPI(
    title="VLSI Audio Overview API",
    description="NotebookLM-style audio overview for VLSI education",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    config = get_config()
    return {
        "message": "VLSI Audio Overview API",
        "status": "running",
        "config_loaded": True,
        "gemini_configured": bool(config.gemini_api_key)
    }

@app.get("/api/")
async def api_root():
    """API root endpoint"""
    config = get_config()
    return {
        "message": "VLSI Audio Overview API",
        "status": "running",
        "config_loaded": True,
        "gemini_configured": bool(config.gemini_api_key)
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        config = get_config()
        return {
            "status": "healthy",
            "config_valid": True,
            "gemini_api_configured": bool(config.gemini_api_key)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@app.get("/api/test-dialogue")
async def test_dialogue_generation():
    """Test endpoint to generate sample dialogue"""
    try:
        client = get_gemini_client()
        segments = await client.generate_dialogue(
            topic="FSM Design",
            duration_minutes=2,  # Short test
            context="Focus on the basic concept of what an FSM is"
        )
        
        return {
            "success": True,
            "segments_count": len(segments),
            "segments": [
                {
                    "speaker": seg.speaker,
                    "text": seg.text,
                    "sequence": seg.sequence
                }
                for seg in segments
            ]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/test-tts")
async def test_tts_synthesis():
    """Test endpoint to generate sample audio with TTS"""
    try:
        engine = get_tts_engine()
        
        # Generate sample audio for both speakers
        test_segments = [
            {"speaker": "zoya", "text": "Hello! I'm Zoya, your VLSI instructor."},
            {"speaker": "ravi", "text": "Hi! I'm Ravi, ready to learn about FSMs."}
        ]
        
        results = engine.synthesize_dialogue(test_segments)
        
        return {
            "success": True,
            "audio_files_generated": len(results),
            "results": [
                {
                    "speaker": r["speaker"],
                    "text": r["text"],
                    "audio_path": r["audio_path"]
                }
                for r in results
            ]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# Request/Response models
class GenerateOverviewRequest(BaseModel):
    topic: str
    duration_minutes: Optional[int] = 8
    context: Optional[str] = None


class AudioSegmentResponse(BaseModel):
    segment_id: str
    speaker: str
    text: str
    sequence: int
    duration_ms: int
    audio_url: str


class TextQuestionRequest(BaseModel):
    question: str
    topic: str
    context: Optional[str] = None
    overview_id: Optional[str] = None


@app.post("/api/overview/generate")
async def generate_audio_overview(request: GenerateOverviewRequest):
    """
    Generate complete audio overview with dialogue and TTS synthesis.
    
    This endpoint orchestrates the complete audio overview generation process:
    1. Generates educational dialogue using Google Gemini AI
    2. Synthesizes audio for each segment using voice cloning (Coqui TTS)
    3. Saves audio files with metadata
    4. Returns segment list with audio URLs
    
    Args:
        request: GenerateOverviewRequest containing:
            - topic (str): The educational topic to generate dialogue about
            - duration_minutes (int, optional): Target duration in minutes (default: 8)
            - context (str, optional): Additional context to guide dialogue generation
    
    Returns:
        dict: Response containing:
            - success (bool): Whether generation succeeded
            - overview_id (str): Unique identifier for this overview
            - topic (str): The topic that was generated
            - segments_count (int): Number of dialogue segments
            - segments (list): List of segment objects with audio URLs
            - tts_enabled (bool): Whether TTS synthesis is available
            - note (str): Status message about audio generation
    
    Example:
        ```json
        {
            "topic": "FSM Design Basics",
            "duration_minutes": 2,
            "context": "Brief introduction to FSM fundamentals"
        }
        ```
    
    Note:
        - Audio synthesis requires Python 3.10 environment with TTS library
        - Generation takes 1-2 minutes per segment
        - Recommended: 5-7 segments (2-minute duration) for reasonable wait times
    """
    try:
        # Step 1: Generate dialogue using ScriptGenerator
        script_generator = get_script_generator()
        dialogue_segments = await script_generator.generate_dialogue(
            topic=request.topic,
            duration_minutes=request.duration_minutes,
            context=request.context
        )
        
        # Step 2: Prepare overview ID
        overview_id = f"overview_{int(time.time() * 1000)}"
        
        # Step 3: Try to synthesize audio using TTS Service
        audio_processor = get_audio_processor()
        segments_response = []
        
        # Use TTS Service to synthesize audio
        from tts_service import get_tts_service
        tts_service = get_tts_service()
        
        if tts_service.tts_available:
            # Synthesize audio for each segment
            for seg in dialogue_segments:
                # Generate audio using TTS service
                audio_path = tts_service.synthesize(
                    text=seg.text,
                    speaker=seg.speaker,
                    temperature=0.75,
                    repetition_penalty=5.0
                )
                
                if audio_path:
                    # Save metadata
                    segment_id = f"{overview_id}_{seg.sequence}"
                    metadata = audio_processor.save_audio_with_metadata(
                        audio_path=audio_path,
                        speaker=seg.speaker,
                        text=seg.text,
                        sequence=seg.sequence,
                        segment_id=segment_id
                    )
                    
                    segments_response.append({
                        "segment_id": segment_id,
                        "speaker": seg.speaker,
                        "text": seg.text,
                        "sequence": seg.sequence,
                        "duration_ms": metadata.duration_ms,
                        "audio_url": f"/api/audio/{segment_id}"
                    })
                else:
                    # Audio synthesis failed for this segment
                    segment_id = f"{overview_id}_{seg.sequence}"
                    segments_response.append({
                        "segment_id": segment_id,
                        "speaker": seg.speaker,
                        "text": seg.text,
                        "sequence": seg.sequence,
                        "duration_ms": 0,
                        "audio_url": None
                    })
        else:
            # TTS not available - return dialogue without audio
            print("⚠️  TTS not available")
            for seg in dialogue_segments:
                segment_id = f"{overview_id}_{seg.sequence}"
                segments_response.append({
                    "segment_id": segment_id,
                    "speaker": seg.speaker,
                    "text": seg.text,
                    "sequence": seg.sequence,
                    "duration_ms": 0,
                    "audio_url": None
                })
        
        return {
            "success": True,
            "overview_id": overview_id,
            "topic": request.topic,
            "segments_count": len(segments_response),
            "segments": segments_response,
            "tts_enabled": tts_service.tts_available,
            "note": "Audio synthesis requires Python 3.10 environment with TTS library" if not tts_service.tts_available else "Audio generated successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.get("/api/audio/{segment_id}")
async def get_audio_file(segment_id: str):
    """
    Serve audio file for a specific dialogue segment.
    
    This endpoint retrieves and streams the audio file for a given segment ID.
    Audio files are in WAV format with voice-cloned speech.
    
    Args:
        segment_id (str): The unique segment identifier (e.g., "overview_1234567890_0")
    
    Returns:
        FileResponse: Audio file in WAV format
        
    Raises:
        404: If segment not found or audio file doesn't exist
    
    Example:
        GET /api/audio/overview_1234567890_0
    """
    try:
        # Load metadata to get file path
        audio_processor = get_audio_processor()
        metadata = audio_processor.load_metadata(segment_id)
        
        if not metadata:
            return {
                "success": False,
                "error": f"Segment not found: {segment_id}"
            }
        
        # Check if file exists
        if not os.path.exists(metadata.file_path):
            return {
                "success": False,
                "error": f"Audio file not found: {metadata.file_path}"
            }
        
        # Serve the audio file
        return FileResponse(
            metadata.file_path,
            media_type="audio/wav",
            filename=f"{segment_id}.wav"
        )
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.get("/api/segments")
async def list_segments(overview_id: Optional[str] = None):
    """
    List all audio segments, optionally filtered by overview_id
    
    Args:
        overview_id: Optional overview identifier to filter by
        
    Returns:
        List of audio segments with metadata
    """
    try:
        audio_processor = get_audio_processor()
        segments = audio_processor.list_audio_segments(overview_id)
        
        segments_response = []
        for seg in segments:
            segments_response.append({
                "segment_id": seg.segment_id,
                "speaker": seg.speaker,
                "text": seg.text,
                "sequence": seg.sequence,
                "duration_ms": seg.duration_ms,
                "audio_url": f"/api/audio/{seg.segment_id}",
                "created_at": seg.created_at
            })
        
        return {
            "success": True,
            "segments_count": len(segments_response),
            "segments": segments_response
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }



@app.post("/api/question/text")
async def ask_text_question(request: TextQuestionRequest):
    """
    Handle text-based student question
    
    This endpoint:
    1. Receives text question from student
    2. Generates contextual response using ResponseGenerator
    3. Optionally synthesizes audio for response
    4. Returns response segments
    
    Args:
        request: TextQuestionRequest with question, topic, and context
        
    Returns:
        Response with transcription and dialogue segments
    """
    try:
        # Generate response
        response_generator = get_response_generator()
        response_segments = await response_generator.generate_response(
            question=request.question,
            topic=request.topic,
            context=request.context
        )
        
        # Prepare response ID
        response_id = f"response_{int(time.time() * 1000)}"
        
        # Try to synthesize audio using TTS Service
        audio_processor = get_audio_processor()
        segments_response = []
        
        # Use TTS Service to synthesize audio
        from tts_service import get_tts_service
        tts_service = get_tts_service()
        
        if tts_service.tts_available:
            # Synthesize audio for each segment
            for seg in response_segments:
                # Generate audio using TTS service
                audio_path = tts_service.synthesize(
                    text=seg.text,
                    speaker=seg.speaker,
                    temperature=0.75,
                    repetition_penalty=5.0
                )
                
                if audio_path:
                    # Save metadata
                    segment_id = f"{response_id}_{seg.sequence}"
                    metadata = audio_processor.save_audio_with_metadata(
                        audio_path=audio_path,
                        speaker=seg.speaker,
                        text=seg.text,
                        sequence=seg.sequence,
                        segment_id=segment_id
                    )
                    
                    segments_response.append({
                        "segment_id": segment_id,
                        "speaker": seg.speaker,
                        "text": seg.text,
                        "sequence": seg.sequence,
                        "duration_ms": metadata.duration_ms,
                        "audio_url": f"/api/audio/{segment_id}"
                    })
                else:
                    # Audio synthesis failed for this segment
                    segment_id = f"{response_id}_{seg.sequence}"
                    segments_response.append({
                        "segment_id": segment_id,
                        "speaker": seg.speaker,
                        "text": seg.text,
                        "sequence": seg.sequence,
                        "duration_ms": 0,
                        "audio_url": None
                    })
        else:
            # TTS not available - return response without audio
            print("⚠️  TTS not available")
            for seg in response_segments:
                segment_id = f"{response_id}_{seg.sequence}"
                segments_response.append({
                    "segment_id": segment_id,
                    "speaker": seg.speaker,
                    "text": seg.text,
                    "sequence": seg.sequence,
                    "duration_ms": 0,
                    "audio_url": None
                })
        
        return {
            "success": True,
            "response_id": response_id,
            "question": request.question,
            "segments_count": len(segments_response),
            "segments": segments_response,
            "tts_enabled": tts_service.tts_available
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.post("/api/question/voice")
async def ask_voice_question(
    audio: UploadFile = File(...),
    topic: str = Form(...),
    context: Optional[str] = Form(None),
    overview_id: Optional[str] = Form(None)
):
    """
    Handle voice-based student question
    
    This endpoint:
    1. Receives audio file from student
    2. Transcribes audio to text
    3. Generates contextual response using ResponseGenerator
    4. Optionally synthesizes audio for response
    5. Returns transcription and response segments
    
    Args:
        audio: Audio file upload
        topic: Current topic
        context: Optional conversation context
        overview_id: Optional overview identifier
        
    Returns:
        Response with transcription and dialogue segments
    """
    try:
        # Read audio file
        audio_data = await audio.read()
        
        # Process voice question
        response_generator = get_response_generator()
        transcription, response_segments = await response_generator.process_voice_question(
            audio_data=audio_data,
            topic=topic,
            context=context
        )
        
        # Prepare response ID
        response_id = f"response_{int(time.time() * 1000)}"
        
        # Try to synthesize audio using TTS Service
        audio_processor = get_audio_processor()
        segments_response = []
        
        # Use TTS Service to synthesize audio
        from tts_service import get_tts_service
        tts_service = get_tts_service()
        
        if tts_service.tts_available:
            # Synthesize audio for each segment
            for seg in response_segments:
                # Generate audio using TTS service
                audio_path = tts_service.synthesize(
                    text=seg.text,
                    speaker=seg.speaker,
                    temperature=0.75,
                    repetition_penalty=5.0
                )
                
                if audio_path:
                    # Save metadata
                    segment_id = f"{response_id}_{seg.sequence}"
                    metadata = audio_processor.save_audio_with_metadata(
                        audio_path=audio_path,
                        speaker=seg.speaker,
                        text=seg.text,
                        sequence=seg.sequence,
                        segment_id=segment_id
                    )
                    
                    segments_response.append({
                        "segment_id": segment_id,
                        "speaker": seg.speaker,
                        "text": seg.text,
                        "sequence": seg.sequence,
                        "duration_ms": metadata.duration_ms,
                        "audio_url": f"/api/audio/{segment_id}"
                    })
                else:
                    # Audio synthesis failed for this segment
                    segment_id = f"{response_id}_{seg.sequence}"
                    segments_response.append({
                        "segment_id": segment_id,
                        "speaker": seg.speaker,
                        "text": seg.text,
                        "sequence": seg.sequence,
                        "duration_ms": 0,
                        "audio_url": None
                    })
        else:
            # TTS not available - return response without audio
            print("⚠️  TTS not available")
            for seg in response_segments:
                segment_id = f"{response_id}_{seg.sequence}"
                segments_response.append({
                    "segment_id": segment_id,
                    "speaker": seg.speaker,
                    "text": seg.text,
                    "sequence": seg.sequence,
                    "duration_ms": 0,
                    "audio_url": None
                })
        
        return {
            "success": True,
            "response_id": response_id,
            "transcription": transcription,
            "segments_count": len(segments_response),
            "segments": segments_response,
            "tts_enabled": tts_service.tts_available
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
