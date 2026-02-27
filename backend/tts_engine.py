"""
TTS Engine for VLSI Audio Overview
Handles text-to-speech synthesis using Coqui TTS with XTTS-v2 for voice cloning
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
        
        print("🎤 Initializing Coqui TTS with XTTS-v2...")
        print("   Note: First run will download the model (~2GB), please wait...")
        
        # Check if CUDA is available for GPU acceleration
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"   Using device: {device}")
        
        # Initialize XTTS-v2 model
        # This model supports voice cloning from audio samples
        try:
            print("   Loading XTTS-v2 model (this may take a few minutes on first run)...")
            self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
            print("✅ XTTS-v2 model loaded successfully")
        except Exception as e:
            print(f"❌ Error loading XTTS-v2 model: {e}")
            raise
        
        # Set up voice samples for cloning
        self.voice_samples_path = Path(self.config.voice_samples_path)
        
        # Zoya's voice samples (instructor - will be cloned from samples)
        zoya_samples_dir = self.voice_samples_path / "zoya"
        self.zoya_sample_files = list(zoya_samples_dir.glob("*.mp3"))
        
        if not self.zoya_sample_files:
            print("⚠️  Warning: No voice samples found for Zoya")
            print(f"   Expected location: {zoya_samples_dir}")
            self.zoya_speaker_wav = []
        else:
            # Use ALL samples for better voice cloning (up to 3 samples)
            # Multiple samples help capture emotional range
            self.zoya_speaker_wav = [str(f) for f in self.zoya_sample_files[:3]]
            print(f"✅ Zoya voice samples loaded: {len(self.zoya_speaker_wav)} files")
            print(f"   Found {len(self.zoya_sample_files)} total samples")
            for sample in self.zoya_speaker_wav:
                print(f"   - {sample}")
        
        # Ravi's voice - use a pre-trained male voice from XTTS
        # XTTS-v2 has built-in speaker embeddings we can use
        # For now, we'll use a reference audio or let XTTS use default male voice
        self.ravi_speaker_wav = None  # Will use default or can add samples later
        
        print("🎤 TTS Engine initialized (Coqui TTS XTTS-v2)")
        print("   Zoya: Cloned voice from samples (instructor)")
        print("   Ravi: Natural male voice (co-host)")
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text for better expression and naturalness
        
        Args:
            text: Input text
            
        Returns:
            Preprocessed text with better punctuation for natural speech
        """
        # Add slight pauses for better expression
        # Replace multiple spaces with single space
        text = " ".join(text.split())
        
        # Add commas for natural pauses if missing
        # This helps with expression and breathing
        import re
        
        # Add comma after common introductory words if not present
        intro_words = ['Well', 'So', 'Now', 'Actually', 'However', 'Therefore', 'Also']
        for word in intro_words:
            text = re.sub(f'\\b{word}\\b(?!,)', f'{word},', text)
        
        # Ensure proper spacing around punctuation
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
        """
        Synthesize speech from text using voice cloning
        
        Args:
            text: Text to synthesize
            speaker: Speaker name ("zoya" or "ravi")
            output_path: Optional output file path. If None, auto-generates path
            temperature: Controls expressiveness (0.1-1.0). Lower=consistent, Higher=expressive
            repetition_penalty: Prevents repetitive patterns (2.0-10.0). Higher=less repetition
            
        Returns:
            Path to generated audio file
        """
        # Preprocess text for better expression
        text = self._preprocess_text(text)
        
        # Generate output path if not provided
        if output_path is None:
            audio_storage = Path(self.config.audio_storage_path)
            audio_storage.mkdir(exist_ok=True)
            
            # Create unique filename
            timestamp = int(time.time() * 1000)
            output_path = str(audio_storage / f"{speaker}_{timestamp}.wav")
        
        try:
            # Select speaker configuration
            speaker_lower = speaker.lower()
            
            if speaker_lower == "zoya":
                if not self.zoya_speaker_wav:
                    raise ValueError("Zoya voice samples not found. Please add samples to voice_samples/zoya/")
                speaker_wav = self.zoya_speaker_wav  # Can be list or string
                print(f"🎙️  Synthesizing with Zoya's cloned voice (using {len(self.zoya_speaker_wav) if isinstance(self.zoya_speaker_wav, list) else 1} sample(s))...")
            elif speaker_lower == "ravi":
                # For Ravi, check if samples exist
                ravi_samples_dir = self.voice_samples_path / "ravi"
                ravi_samples = list(ravi_samples_dir.glob("*.mp3")) if ravi_samples_dir.exists() else []
                
                if ravi_samples:
                    # Use multiple samples if available (up to 3)
                    speaker_wav = [str(f) for f in ravi_samples[:3]]
                    print(f"🎙️  Synthesizing with Ravi's cloned voice (using {len(speaker_wav)} sample(s))...")
                else:
                    # No Ravi samples - need to add them for proper male voice
                    print("⚠️  No Ravi voice samples found. Skipping Ravi synthesis.")
                    print("   To add Ravi's voice:")
                    print("   1. Create directory: backend/voice_samples/ravi/")
                    print("   2. Add male voice MP3 samples to that directory")
                    raise ValueError("Ravi voice samples not found. Please add samples to voice_samples/ravi/")
            else:
                raise ValueError(f"Unknown speaker: {speaker}")
            
            # Generate speech using XTTS-v2
            # XTTS supports multiple languages and voice cloning
            # Adjust parameters for more natural expression
            self.tts.tts_to_file(
                text=text,
                speaker_wav=speaker_wav,
                language="en",
                file_path=output_path,
                # Temperature controls randomness/expressiveness (0.1-1.0)
                # Lower = more consistent, Higher = more expressive
                temperature=temperature,
                # Length penalty affects speech speed
                length_penalty=1.0,
                # Repetition penalty prevents repetitive patterns
                repetition_penalty=repetition_penalty,
                # Top-k and top-p control diversity
                top_k=50,
                top_p=0.85
            )
            
            print(f"✅ Audio generated: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error synthesizing speech: {e}")
            raise
    
    def synthesize_dialogue(self, segments: list) -> list:
        """
        Synthesize audio for multiple dialogue segments
        
        Args:
            segments: List of dialogue segments with 'speaker' and 'text' fields
            
        Returns:
            List of segments with added 'audio_path' field
        """
        results = []
        
        print(f"\n🎬 Starting synthesis of {len(segments)} dialogue segments...")
        
        for i, segment in enumerate(segments):
            speaker = segment.get("speaker", "zoya")
            text = segment.get("text", "")
            
            if not text:
                print(f"⚠️  Skipping empty segment {i}")
                continue
            
            try:
                print(f"\n[{i+1}/{len(segments)}] {speaker}: {text[:50]}...")
                audio_path = self.synthesize(text, speaker)
                
                result = {
                    **segment,
                    "audio_path": audio_path,
                    "sequence": i
                }
                results.append(result)
                
            except Exception as e:
                print(f"❌ Error synthesizing segment {i}: {e}")
                # Continue with other segments
                continue
        
        print(f"\n✅ Synthesized {len(results)}/{len(segments)} segments")
        return results


# Global TTS engine instance
_engine: Optional[TTSEngine] = None

def get_tts_engine() -> TTSEngine:
    """Get the global TTS engine instance"""
    global _engine
    if _engine is None:
        _engine = TTSEngine()
    return _engine
