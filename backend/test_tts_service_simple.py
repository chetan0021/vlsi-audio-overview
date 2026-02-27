"""
Simple test for TTS Service
"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from tts_service import get_tts_service


def test_tts_service():
    """Test TTS service initialization and simple synthesis"""
    
    print("=" * 60)
    print("TESTING TTS SERVICE")
    print("=" * 60)
    
    # Initialize service
    print("\n🎤 Initializing TTS Service...")
    tts_service = get_tts_service()
    
    if not tts_service.tts_available:
        print("❌ TTS Service not available")
        print(f"   Expected Python 3.10 environment at: {tts_service.venv_tts_python}")
        return False
    
    print("✅ TTS Service initialized")
    
    # Test synthesis for Zoya
    print("\n🎬 Testing Zoya voice synthesis...")
    audio_path = tts_service.synthesize(
        text="Hello! I'm Zoya, your VLSI instructor. Let's learn about FSM design.",
        speaker="zoya",
        temperature=0.75,
        repetition_penalty=5.0
    )
    
    if audio_path:
        print(f"✅ Zoya audio generated: {audio_path}")
        if os.path.exists(audio_path):
            file_size = os.path.getsize(audio_path)
            print(f"   File size: {file_size:,} bytes")
        else:
            print(f"⚠️  Warning: File not found")
            return False
    else:
        print("❌ Failed to generate Zoya audio")
        return False
    
    # Test synthesis for Ravi
    print("\n🎬 Testing Ravi voice synthesis...")
    audio_path = tts_service.synthesize(
        text="Hi! I'm Ravi, ready to explore FSM design with you.",
        speaker="ravi",
        temperature=0.75,
        repetition_penalty=5.0
    )
    
    if audio_path:
        print(f"✅ Ravi audio generated: {audio_path}")
        if os.path.exists(audio_path):
            file_size = os.path.getsize(audio_path)
            print(f"   File size: {file_size:,} bytes")
        else:
            print(f"⚠️  Warning: File not found")
            return False
    else:
        print("❌ Failed to generate Ravi audio")
        return False
    
    print("\n" + "=" * 60)
    print("✅ TTS SERVICE TEST PASSED")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_tts_service()
    sys.exit(0 if success else 1)
