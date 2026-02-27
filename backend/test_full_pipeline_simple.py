"""
Test complete pipeline with TTS Service
Tests dialogue generation and audio synthesis using the TTS service bridge
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from script_generator import get_script_generator
from tts_service import get_tts_service
from audio_processor import get_audio_processor


async def test_complete_pipeline():
    """Test the complete pipeline from dialogue generation to audio synthesis"""
    
    print("=" * 60)
    print("TESTING COMPLETE PIPELINE WITH TTS SERVICE")
    print("=" * 60)
    
    # Step 1: Generate dialogue
    print("\n📝 Step 1: Generating dialogue...")
    script_generator = get_script_generator()
    
    segments = await script_generator.generate_dialogue(
        topic="FSM Design Basics",
        duration_minutes=2,  # Short test
        context="Focus on what an FSM is and one simple example"
    )
    
    print(f"✅ Generated {len(segments)} dialogue segments")
    
    # Step 2: Initialize TTS Service
    print("\n🎤 Step 2: Initializing TTS Service...")
    tts_service = get_tts_service()
    
    if not tts_service.tts_available:
        print("❌ TTS Service not available")
        print("   Make sure Python 3.10 environment exists at: backend/venv_tts/")
        return
    
    print("✅ TTS Service initialized")
    
    # Step 3: Synthesize first 2 segments as a test
    print("\n🎬 Step 3: Synthesizing audio (first 2 segments)...")
    
    test_segments = segments[:2]
    
    for i, seg in enumerate(test_segments):
        print(f"\n[{i+1}/{len(test_segments)}] {seg.speaker}: {seg.text[:60]}...")
        
        audio_path = tts_service.synthesize(
            text=seg.text,
            speaker=seg.speaker,
            temperature=0.75,
            repetition_penalty=5.0
        )
        
        if audio_path:
            print(f"✅ Audio generated: {audio_path}")
            
            # Verify file exists
            if os.path.exists(audio_path):
                file_size = os.path.getsize(audio_path)
                print(f"   File size: {file_size:,} bytes")
            else:
                print(f"⚠️  Warning: File not found at {audio_path}")
        else:
            print(f"❌ Failed to generate audio")
    
    print("\n" + "=" * 60)
    print("✅ PIPELINE TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_complete_pipeline())
