"""
Configuration management for VLSI Audio Overview
Loads environment variables and validates required settings
"""
import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config(BaseModel):
    """Application configuration model"""
    
    # API Keys
    gemini_api_key: str = Field(..., description="Google Gemini API key")
    
    # Storage Paths
    audio_storage_path: str = Field(default="./audio_storage", description="Path to store generated audio files")
    metadata_storage_path: str = Field(default="./metadata_storage", description="Path to store audio metadata")
    voice_samples_path: str = Field(default="./voice_samples", description="Path to voice sample files")
    
    # Voice Model Paths
    zoya_voice_model_path: str = Field(default="./voice_models/zoya", description="Path to Zoya voice model")
    ravi_voice_model_path: str = Field(default="./voice_models/ravi", description="Path to Ravi voice model")
    
    # TTS Configuration
    tts_sample_rate: int = Field(default=22050, description="Sample rate for TTS audio generation")
    
    # Application Settings
    max_audio_duration: int = Field(default=600, description="Maximum audio duration in seconds (10 minutes)")
    
    @validator('gemini_api_key')
    def validate_gemini_key(cls, v):
        """Validate that Gemini API key is not empty"""
        if not v or v == "your_gemini_api_key_here":
            raise ValueError("GEMINI_API_KEY must be set in .env file")
        return v
    
    @validator('audio_storage_path', 'metadata_storage_path', 'voice_samples_path', 
               'zoya_voice_model_path', 'ravi_voice_model_path')
    def ensure_path_exists(cls, v):
        """Ensure storage paths exist"""
        path = Path(v)
        path.mkdir(parents=True, exist_ok=True)
        return str(path)
    
    class Config:
        """Pydantic config"""
        env_file = '.env'
        env_file_encoding = 'utf-8'


def load_config() -> Config:
    """
    Load and validate configuration from environment variables
    
    Returns:
        Config: Validated configuration object
        
    Raises:
        ValueError: If required configuration is missing or invalid
    """
    try:
        config = Config(
            gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
            audio_storage_path=os.getenv("AUDIO_STORAGE_PATH", "./audio_storage"),
            metadata_storage_path=os.getenv("METADATA_STORAGE_PATH", "./metadata_storage"),
            voice_samples_path=os.getenv("VOICE_SAMPLES_PATH", "./voice_samples"),
            zoya_voice_model_path=os.getenv("ZOYA_VOICE_MODEL_PATH", "./voice_models/zoya"),
            ravi_voice_model_path=os.getenv("RAVI_VOICE_MODEL_PATH", "./voice_models/ravi"),
            tts_sample_rate=int(os.getenv("TTS_SAMPLE_RATE", "22050")),
            max_audio_duration=int(os.getenv("MAX_AUDIO_DURATION", "600"))
        )
        return config
    except ValueError as e:
        raise ValueError(f"Configuration error: {str(e)}")


# Global config instance
_config: Optional[Config] = None

def get_config() -> Config:
    """
    Get the global configuration instance
    
    Returns:
        Config: Global configuration object
    """
    global _config
    if _config is None:
        _config = load_config()
    return _config
