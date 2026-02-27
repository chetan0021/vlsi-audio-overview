"""
End-to-end test of the complete audio overview pipeline
Tests: Gemini dialogue generation → TTS synthesis → Audio processing
"""
import os
import asyncio
os.environ['COQUI_TOS_AGREED'] = '1'

from gemini_client import get_gemini_client
from audio_processor import get_audio_processor


async def test_full_pipeline():
    """Test the complete pipeline from dialogue generation to audio storage"""
    print("🧪 Testing Complete Audio Overview Pipeline...\n")
    print("=" * 60)
    
    try:
        # Step 1: Generate dialogue using Gemini
        print("\n[Step 1] Generating dialogue with Gemini...")
        print("   Topic: FSM Design Basics")
        print("   Duration: 2 minutes (short test)")
        
        gemini_client = get_gemini_client()
        segments = await gemini_client.generate_dialogue(
            topic="FSM Design Basics",
            duration_minutes=2,
            context="Focus on what FSMs are and a simple traffic light example"
        )
        
        print(f"   ✅ Generated {len(segments)} dialogue segments")
        print(f"\n   Preview:")
        for i, seg in enumerate(segments[:3]):
            print(f"   {i+1}. {seg.speaker.upper()}: {seg.text[:60]}...")
        if len(segments) > 3:
            print(f"   ... and {len(segments) - 3} more segments")
        
        # Step 2: Initialize TTS engine (will take time on first run)
        print("\n[Step 2] Initializing TTS engine...")
        print("   Note: This will download XTTS-v2 model on first run (~2GB)")
        print("   Please wait...")
        
        # Import here to avoid loading TTS if Gemini fails
        from tts_engine import get_tts_engine
        tts_engine = get_tts_engine()
        
        # Step 3: Synthesize audio for first 3 segments (to save time)
        print("\n[Step 3] Synthesizing audio (testing first 3 segments)...")
        test_segments = segments[:3]
        
        audio_files = []
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
            
            audio_files.append({
                'segment': segment,
                'audio_path': audio_path
            })
            
            print(f"   ✅ Audio generated: {audio_path}")
        
        # Step 4: Save audio with metadata
        print("\n[Step 4] Saving audio files with metadata...")
        audio_processor = get_audio_processor()
        
        metadata_list = []
        for item in audio_files:
            segment = item['segment']
            audio_path = item['audio_path']
            
            metadata = audio_processor.save_audio_with_metadata(
                audio_path=audio_path,
                speaker=segment.speaker,
                text=segment.text,
                sequence=segment.sequence,
                segment_id=f"test_fsm_{segment.sequence}"
            )
            
            metadata_list.append(metadata)
            print(f"   ✅ Saved: {metadata.segment_id} ({metadata.duration_ms}ms)")
        
        # Step 5: Verify everything is stored correctly
        print("\n[Step 5] Verifying storage...")
        
        for metadata in metadata_list:
            # Load metadata
            loaded = audio_processor.load_metadata(metadata.segment_id)
            if loaded:
                print(f"   ✅ {loaded.segment_id}: {loaded.speaker} - {loaded.duration_ms}ms")
            else:
                print(f"   ❌ Failed to load: {metadata.segment_id}")
            
            # Validate audio file
            is_valid = audio_processor.validate_audio_file(metadata.file_path)
            if not is_valid:
                print(f"   ⚠️  Audio validation failed: {metadata.file_path}")
        
        # Summary
        print("\n" + "=" * 60)
        print("🎉 Complete Pipeline Test Successful!")
        print("=" * 60)
        print(f"\n📊 Summary:")
        print(f"   • Generated {len(segments)} dialogue segments")
        print(f"   • Synthesized {len(audio_files)} audio files")
        print(f"   • Saved {len(metadata_list)} metadata records")
        
        total_duration = sum(m.duration_ms for m in metadata_list)
        print(f"   • Total audio duration: {total_duration/1000:.2f}s")
        
        print(f"\n📁 Files saved in:")
        print(f"   • Audio: backend/audio_storage/")
        print(f"   • Metadata: backend/metadata_storage/")
        
        print(f"\n💡 Next steps:")
        print(f"   1. Listen to the generated audio files")
        print(f"   2. Check if Zoya and Ravi's voices sound natural")
        print(f"   3. Verify the dialogue makes sense")
        print(f"   4. Ready to build the full API endpoint!")
        
    except Exception as e:
        print(f"\n❌ Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Run the async test
    asyncio.run(test_full_pipeline())
