"""
TTS Engine for subprocess calls (no emoji output)
This version is used when called from TTS Service subprocess
"""
import os
import time
from typing import Optional
from pathlib import Path

# Accept Coqui TTS license automatically (non-commercial use)
os.environ['COQUI_TOS_AGREED'] = '1'

import torch
from TTS.api import TTS

from config import get_config


class TTSEngine:
    """Text-to-speech engine using Coqui TTS XTTS-v2 with voice cloning"""
    
    def __init__(self):
        """Initialize TTS engine with XTTS-v2 model"""
        self.config = get_config()
        
        # Check if CUDA is available for GPU acceleration
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize XTTS-v2 model
        try:
            self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        except Exception as e:
            raise
        
        # Set up voice samples for cloning - use absolute paths
        voice_samples_path = Path(self.config.voice_samples_path)
        if not voice_samples_path.is_absolute():
            # If relative, resolve from backend directory
            backend_dir = Path(__file__).parent
            voice_samples_path = (backend_dir / voice_samples_path).resolve()
        
        self.voice_samples_path = voice_samples_path
        
        # Zoya's voice samples
        zoya_samples_dir = self.voice_samples_path / "zoya"
        self.zoya_sample_files = list(zoya_samples_dir.glob("*.mp3"))
        
        if self.zoya_sample_files:
            self.zoya_speaker_wav = [str(f) for f in self.zoya_sample_files[:3]]
        else:
            self.zoya_speaker_wav = []
        
        # Ravi's voice samples
        ravi_samples_dir = self.voice_samples_path / "ravi"
        self.ravi_sample_files = list(ravi_samples_dir.glob("*.mp3"))
        
        if self.ravi_sample_files:
            self.ravi_speaker_wav = [str(f) for f in self.ravi_sample_files[:3]]
        else:
            self.ravi_speaker_wav = []
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for better expression and naturalness"""
        text = " ".join(text.split())
        
        import re
        intro_words = ['Well', 'So', 'Now', 'Actually', 'However', 'Therefore', 'Also']
        for word in intro_words:
            text = re.sub(f'\\b{word}\\b(?!,)', f'{word},', text)
        
        text = re.sub(r'\s*([,!?.])\s*', r'\1 ', text)
        text = text.strip()
        
        return text
    
    def synthesize(
        self,
        text: str,
        speaker: str,
        output_path: Optional[str] = None,
        temperature: float = 0.75,
        repetition_penalty: float = 5.0
    ) -> str:
        """Synthesize speech from text using voice cloning"""
        text = self._preprocess_text(text)
        
        if output_path is None:
            audio_storage = Path(self.config.audio_storage_path)
            if not audio_storage.is_absolute():
                # If relative, resolve from backend directory
                backend_dir = Path(__file__).parent
                audio_storage = (backend_dir / audio_storage).resolve()
            
            audio_storage.mkdir(exist_ok=True, parents=True)
            timestamp = int(time.time() * 1000)
            output_path = str(audio_storage / f"{speaker}_{timestamp}.wav")
        
        try:
            speaker_lower = speaker.lower()
            
            if speaker_lower == "zoya":
                if not self.zoya_speaker_wav:
                    raise ValueError("Zoya voice samples not found")
                speaker_wav = self.zoya_speaker_wav
            elif speaker_lower == "ravi":
                if not self.ravi_speaker_wav:
                    raise ValueError("Ravi voice samples not found")
                speaker_wav = self.ravi_speaker_wav
            else:
                raise ValueError(f"Unknown speaker: {speaker}")
            
            self.tts.tts_to_file(
                text=text,
                speaker_wav=speaker_wav,
                language="en",
                file_path=output_path,
                temperature=temperature,
                length_penalty=1.0,
                repetition_penalty=repetition_penalty,
                top_k=50,
                top_p=0.85
            )
            
            return output_path
            
        except Exception as e:
            raise


# Global TTS engine instance
_engine: Optional[TTSEngine] = None

def get_tts_engine() -> TTSEngine:
    """Get the global TTS engine instance"""
    global _engine
    if _engine is None:
        _engine = TTSEngine()
    return _engine
