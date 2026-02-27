"""
Audio Processor for VLSI Audio Overview
Handles audio format conversion, file storage, and metadata management
"""
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from pydub import AudioSegment
from pydub.utils import mediainfo

from config import get_config


class AudioMetadata:
    """Metadata for an audio segment"""
    
    def __init__(
        self,
        segment_id: str,
        speaker: str,
        text: str,
        sequence: int,
        duration_ms: int,
        file_path: str,
        format: str = "wav",
        sample_rate: int = 22050,
        channels: int = 1,
        bitrate: str = "128k",
        created_at: Optional[str] = None
    ):
        self.segment_id = segment_id
        self.speaker = speaker
        self.text = text
        self.sequence = sequence
        self.duration_ms = duration_ms
        self.file_path = file_path
        self.format = format
        self.sample_rate = sample_rate
        self.channels = channels
        self.bitrate = bitrate
        self.created_at = created_at or datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary"""
        return {
            "segment_id": self.segment_id,
            "speaker": self.speaker,
            "text": self.text,
            "sequence": self.sequence,
            "duration_ms": self.duration_ms,
            "file_path": self.file_path,
            "format": self.format,
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "bitrate": self.bitrate,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AudioMetadata':
        """Create metadata from dictionary"""
        return cls(**data)


class AudioProcessor:
    """Handles audio file processing, conversion, and storage"""
    
    def __init__(self):
        """Initialize audio processor with config"""
        self.config = get_config()
        self.audio_storage_path = Path(self.config.audio_storage_path)
        self.metadata_storage_path = Path(self.config.metadata_storage_path)
        
        # Ensure directories exist
        self.audio_storage_path.mkdir(parents=True, exist_ok=True)
        self.metadata_storage_path.mkdir(parents=True, exist_ok=True)
        
        print("✅ AudioProcessor initialized")
        print(f"   Audio storage: {self.audio_storage_path}")
        print(f"   Metadata storage: {self.metadata_storage_path}")
    
    def save_audio_with_metadata(
        self,
        audio_path: str,
        speaker: str,
        text: str,
        sequence: int,
        segment_id: Optional[str] = None
    ) -> AudioMetadata:
        """
        Save audio file with metadata
        
        Args:
            audio_path: Path to the audio file
            speaker: Speaker name ("zoya" or "ravi")
            text: Transcript text
            sequence: Sequence number in dialogue
            segment_id: Optional segment ID (auto-generated if not provided)
            
        Returns:
            AudioMetadata object
        """
        try:
            # Generate segment ID if not provided
            if segment_id is None:
                timestamp = int(datetime.utcnow().timestamp() * 1000)
                segment_id = f"{speaker}_{sequence}_{timestamp}"
            
            # Load audio file to get metadata
            audio = AudioSegment.from_file(audio_path)
            duration_ms = len(audio)
            
            # Get audio file info (use pydub properties if ffmpeg not available)
            try:
                info = mediainfo(audio_path)
                sample_rate = int(info.get('sample_rate', audio.frame_rate))
                channels = int(info.get('channels', audio.channels))
                bitrate = info.get('bit_rate', '128000')
                
                # Convert bitrate to readable format (e.g., "128k")
                if bitrate and bitrate.isdigit():
                    bitrate_kbps = int(bitrate) // 1000
                    bitrate = f"{bitrate_kbps}k"
            except Exception:
                # Fallback to pydub properties if ffmpeg not available
                sample_rate = audio.frame_rate
                channels = audio.channels
                bitrate = "128k"  # Default assumption
            
            # Create metadata
            metadata = AudioMetadata(
                segment_id=segment_id,
                speaker=speaker,
                text=text,
                sequence=sequence,
                duration_ms=duration_ms,
                file_path=audio_path,
                format="wav",
                sample_rate=sample_rate,
                channels=channels,
                bitrate=bitrate
            )
            
            # Save metadata to JSON file
            metadata_file = self.metadata_storage_path / f"{segment_id}.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata.to_dict(), f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved audio metadata: {segment_id}")
            return metadata
            
        except Exception as e:
            print(f"❌ Error saving audio metadata: {e}")
            raise

    
    def load_metadata(self, segment_id: str) -> Optional[AudioMetadata]:
        """
        Load metadata for an audio segment
        
        Args:
            segment_id: Segment identifier
            
        Returns:
            AudioMetadata object or None if not found
        """
        try:
            metadata_file = self.metadata_storage_path / f"{segment_id}.json"
            
            if not metadata_file.exists():
                print(f"⚠️  Metadata not found: {segment_id}")
                return None
            
            with open(metadata_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return AudioMetadata.from_dict(data)
            
        except Exception as e:
            print(f"❌ Error loading metadata: {e}")
            return None
    
    def convert_audio_format(
        self,
        input_path: str,
        output_format: str = "wav",
        sample_rate: int = 22050,
        channels: int = 1,
        bitrate: str = "128k"
    ) -> str:
        """
        Convert audio file to specified format
        
        Args:
            input_path: Path to input audio file
            output_format: Target format (wav, mp3, etc.)
            sample_rate: Target sample rate in Hz
            channels: Number of audio channels (1=mono, 2=stereo)
            bitrate: Target bitrate (e.g., "128k")
            
        Returns:
            Path to converted audio file
        """
        try:
            # Load audio file
            audio = AudioSegment.from_file(input_path)
            
            # Apply conversions
            if audio.frame_rate != sample_rate:
                audio = audio.set_frame_rate(sample_rate)
            
            if audio.channels != channels:
                audio = audio.set_channels(channels)
            
            # Generate output path
            input_file = Path(input_path)
            output_path = input_file.parent / f"{input_file.stem}_converted.{output_format}"
            
            # Export with specified format and bitrate
            audio.export(
                output_path,
                format=output_format,
                bitrate=bitrate
            )
            
            print(f"✅ Converted audio: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"❌ Error converting audio: {e}")
            raise
    
    def validate_audio_file(self, audio_path: str) -> bool:
        """
        Validate audio file format and properties
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check if file exists
            if not Path(audio_path).exists():
                print(f"❌ Audio file not found: {audio_path}")
                return False
            
            # Try to load audio file
            audio = AudioSegment.from_file(audio_path)
            
            # Check basic properties
            if len(audio) == 0:
                print(f"❌ Audio file is empty: {audio_path}")
                return False
            
            # Get file info (use pydub properties if ffmpeg not available)
            try:
                info = mediainfo(audio_path)
                sample_rate = int(info.get('sample_rate', audio.frame_rate))
                bitrate = info.get('bit_rate', '0')
            except Exception:
                # Fallback to pydub properties
                sample_rate = audio.frame_rate
                bitrate = None
            
            # Validate sample rate (should be at least 8kHz for speech)
            if sample_rate < 8000:
                print(f"❌ Sample rate too low: {sample_rate}Hz")
                return False
            
            # Validate bitrate if available (should be at least 64kbps for decent quality)
            if bitrate and bitrate.isdigit():
                bitrate_kbps = int(bitrate) // 1000
                if bitrate_kbps < 64:
                    print(f"⚠️  Low bitrate: {bitrate_kbps}kbps (recommended: 128kbps+)")
            
            print(f"✅ Audio file valid: {audio_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error validating audio: {e}")
            return False
    
    def get_audio_duration(self, audio_path: str) -> int:
        """
        Get audio file duration in milliseconds
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Duration in milliseconds
        """
        try:
            audio = AudioSegment.from_file(audio_path)
            return len(audio)
        except Exception as e:
            print(f"❌ Error getting audio duration: {e}")
            return 0
    
    def list_audio_segments(self, overview_id: Optional[str] = None) -> list:
        """
        List all audio segments, optionally filtered by overview_id
        
        Args:
            overview_id: Optional overview identifier to filter by
            
        Returns:
            List of AudioMetadata objects
        """
        try:
            segments = []
            
            # Iterate through metadata files
            for metadata_file in self.metadata_storage_path.glob("*.json"):
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Filter by overview_id if provided
                if overview_id and not data.get('segment_id', '').startswith(overview_id):
                    continue
                
                segments.append(AudioMetadata.from_dict(data))
            
            # Sort by sequence
            segments.sort(key=lambda x: x.sequence)
            
            return segments
            
        except Exception as e:
            print(f"❌ Error listing audio segments: {e}")
            return []


# Global processor instance
_processor: Optional[AudioProcessor] = None

def get_audio_processor() -> AudioProcessor:
    """Get the global AudioProcessor instance"""
    global _processor
    if _processor is None:
        _processor = AudioProcessor()
    return _processor
