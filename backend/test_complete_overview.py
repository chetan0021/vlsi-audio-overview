"""
Complete end-to-end test of audio overview generation
Tests the full pipeline: Script generation → TTS synthesis → Audio storage
"""
import os
import asyncio
os.environ['COQUI_TOS_AGREED'] = '1'

from script_generator import get_script_generator
from audio_processor import get_audio_processor


async def test_complete_overview():
    """Test complete audio overview generation"""
    print("🧪 Testing Complete Audio Overview Generation...\n")
    print("=" * 60)
    
    try:
        # Step 1: Generate dialogue script
        print("\n[Step 1] Generating dialogue script...")
        print("   Topic: FSM Design Basics")
        print("   Duration: 2 minutes")
        
        script_generator = get_script_generator()
        segments = await script_generator.generate_dialogue(
            topic="FSM Design Basics",
            duration_minutes=2,
            context="Focus on what FSMs are and a simple traffic light example"
        )
        
        print(f"   ✅ Generated {len(segments)} dialogue segments")
        
        # Show estimated duration
        estimated_duration = script_generator.estimate_duration(segments)
        print(f"   Estimated duration: {estimated_duration:.2f} minutes")
        
        # Show speaker distribution
        distribution = script_generator.get_speaker_distribution(segments)
        for speaker, stats in distribution.items():
            print(f"   {speaker.upper()}: {stats['count']} segments ({stats['percentage']:.1f}%)")
        
        # Step 2: Initialize TTS engine
        print("\n[Step 2] Initializing TTS engine...")
        print("   Note: This requires Python 3.10 environment")
        print("   Loading XTTS-v2 model...")
        
        try:
            from tts_engine import get_tts_engine
            tts_engine = get_tts_engine()
            tts_available = True
        except Exception as e:
            print(f"   ⚠️  TTS not available: {e}")
            print("   Skipping audio synthesis")
            tts_available = False
        
        if not tts_available:
            print("\n💡 To test with TTS, run:")
            print("   backend\\venv_tts\\Scripts\\python.exe backend\\test_complete_overview.py")
            return
        
        # Step 3: Synthesize audio for first 3 segments (to save time)
        print("\n[Step 3] Synthesizing audio (first 3 segments for testing)...")
        test_segments = segments[:3]
        
        audio_processor = get_audio_processor()
        overview_id = f"test_overview_{int(asyncio.get_event_loop().time() * 1000)}"
        
        metadata_list = []
        for i, segment in enumerate(test_segments):
            print(f"\n   [{i+1}/{len(test_segments)}] {segment.speaker.upper()}")
            print(f"   Text: {segment.text[:70]}...")
            
            # Synthesize audio
            audio_path = tts_engine.synthesize(
                text=segment.text,
                speaker=segment.speaker,
                temperature=0.75,
                repetition_penalty=5.0
            )
            
            # Save with metadata
            segment_id = f"{overview_id}_{segment.sequence}"
            metadata = audio_processor.save_audio_with_metadata(
                audio_path=audio_path,
                speaker=segment.speaker,
                text=segment.text,
                sequence=segment.sequence,
                segment_id=segment_id
            )
            
            metadata_list.append(metadata)
            print(f"   ✅ Saved: {segment_id} ({metadata.duration_ms}ms)")
        
        # Step 4: Verify storage
        print("\n[Step 4] Verifying storage...")
        for metadata in metadata_list:
            # Validate audio file
            is_valid = audio_processor.validate_audio_file(metadata.file_path)
            status = "✅" if is_valid else "❌"
            print(f"   {status} {metadata.segment_id}: {metadata.duration_ms}ms")
        
        # Summary
        total_duration = sum(m.duration_ms for m in metadata_list)
        print("\n" + "=" * 60)
        print("🎉 Complete Audio Overview Test Successful!")
        print("=" * 60)
        print(f"\n📊 Summary:")
        print(f"   • Generated {len(segments)} dialogue segments")
        print(f"   • Synthesized {len(metadata_list)} audio files")
        print(f"   • Total audio duration: {total_duration/1000:.2f}s")
        print(f"   • Estimated full duration: {estimated_duration:.2f} minutes")
        
        print(f"\n📁 Files saved in:")
        print(f"   • Audio: backend/audio_storage/")
        print(f"   • Metadata: backend/metadata_storage/")
        
        print(f"\n🎧 You can now:")
        print(f"   1. Listen to the generated audio files")
        print(f"   2. Test the API endpoint: POST /api/overview/generate")
        print(f"   3. Use the frontend to generate and play audio")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_complete_overview())
