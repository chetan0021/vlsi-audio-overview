"""
TTS Service Wrapper
Handles TTS synthesis by calling the Python 3.10 environment
"""
import subprocess
import json
import os
from pathlib import Path
from typing import Optional


class TTSService:
    """Service to handle TTS synthesis using Python 3.10 environment"""
    
    def __init__(self):
        """Initialize TTS service"""
        # Get absolute path to venv_tts
        backend_dir = Path(__file__).parent
        self.venv_tts_python = backend_dir / "venv_tts" / "Scripts" / "python.exe"
        self.tts_available = self.venv_tts_python.exists()
        
        if self.tts_available:
            print("✅ TTS Service initialized (Python 3.10 environment found)")
        else:
            print("⚠️  TTS Service: Python 3.10 environment not found")
            print(f"   Expected: {self.venv_tts_python}")
    
    def synthesize(
        self,
        text: str,
        speaker: str,
        output_path: Optional[str] = None,
        temperature: float = 0.75,
        repetition_penalty: float = 5.0
    ) -> Optional[str]:
        """
        Synthesize speech using TTS engine in Python 3.10 environment
        
        Args:
            text: Text to synthesize
            speaker: Speaker name ("zoya" or "ravi")
            output_path: Optional output file path
            temperature: TTS temperature parameter
            repetition_penalty: TTS repetition penalty
            
        Returns:
            Path to generated audio file or None if failed
        """
        if not self.tts_available:
            print("⚠️  TTS not available")
            return None
        
        try:
            # Create a temporary Python script to run TTS
            # Handle None/null for output_path
            output_path_str = "None" if output_path is None else json.dumps(output_path)
            
            script_content = f"""
import os
import sys
os.environ['COQUI_TOS_AGREED'] = '1'

# Suppress all print output except SUCCESS/ERROR
import io
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()

from tts_engine_subprocess import get_tts_engine
import json

try:
    engine = get_tts_engine()
    audio_path = engine.synthesize(
        text={json.dumps(text)},
        speaker={json.dumps(speaker)},
        output_path={output_path_str},
        temperature={temperature},
        repetition_penalty={repetition_penalty}
    )
    # Restore stdout for final output
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    print("SUCCESS:" + audio_path)
except Exception as e:
    # Restore stdout for error output
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    print("ERROR:" + str(e))
"""
            
            # Write script to temp file
            backend_dir = Path(__file__).parent
            script_path = backend_dir / "temp_tts_script.py"
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            # Run script with Python 3.10 (increase timeout for TTS)
            result = subprocess.run(
                [str(self.venv_tts_python), str(script_path)],
                cwd=str(backend_dir),
                capture_output=True,
                text=True,
                timeout=180  # 3 minutes per segment
            )
            
            # Clean up temp script
            script_path.unlink(missing_ok=True)
            
            # Parse output
            output = result.stdout + result.stderr
            
            if "SUCCESS:" in output:
                audio_path = output.split("SUCCESS:")[1].strip().split("\n")[0]
                print(f"✅ TTS synthesis successful: {audio_path}")
                return audio_path
            else:
                print(f"❌ TTS synthesis failed: {output}")
                return None
                
        except subprocess.TimeoutExpired:
            print("❌ TTS synthesis timeout")
            return None
        except Exception as e:
            print(f"❌ TTS service error: {e}")
            return None
    
    def synthesize_dialogue(self, segments: list) -> list:
        """
        Synthesize audio for multiple dialogue segments
        
        Args:
            segments: List of dialogue segments
            
        Returns:
            List of segments with audio_path added
        """
        results = []
        
        print(f"\n🎬 Starting TTS synthesis for {len(segments)} segments...")
        
        for i, segment in enumerate(segments):
            speaker = segment.get("speaker", "zoya")
            text = segment.get("text", "")
            
            if not text:
                print(f"⚠️  Skipping empty segment {i}")
                continue
            
            print(f"\n[{i+1}/{len(segments)}] {speaker}: {text[:50]}...")
            
            audio_path = self.synthesize(text, speaker)
            
            if audio_path:
                result = {
                    **segment,
                    "audio_path": audio_path
                }
                results.append(result)
            else:
                print(f"⚠️  Failed to synthesize segment {i}")
        
        print(f"\n✅ Synthesized {len(results)}/{len(segments)} segments")
        return results


# Global service instance
_service: Optional[TTSService] = None

def get_tts_service() -> TTSService:
    """Get the global TTS service instance"""
    global _service
    if _service is None:
        _service = TTSService()
    return _service
