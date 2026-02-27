"""
Test script for AudioProcessor
"""
import os
from pathlib import Path
from audio_processor import get_audio_processor


def test_audio_processor():
    """Test AudioProcessor functionality"""
    print("🧪 Testing AudioProcessor...\n")
    print("=" * 60)
    
    try:
        # Initialize processor
        print("\n🔧 Initializing AudioProcessor...")
        processor = get_audio_processor()
        
        # Find an existing audio file to test with
        audio_storage = Path("./backend/audio_storage")
        audio_files = list(audio_storage.glob("*.wav"))
        
        if not audio_files:
            print("❌ No audio files found in audio_storage/")
            print("   Run test_tts_auto.py first to generate some audio files")
            return
        
        test_audio = audio_files[0]
        print(f"\n📁 Using test audio: {test_audio.name}")
        
        # Test 1: Validate audio file
        print("\n[Test 1] Validating audio file...")
        is_valid = processor.validate_audio_file(str(test_audio))
        print(f"   Result: {'✅ Valid' if is_valid else '❌ Invalid'}")
        
        # Test 2: Get audio duration
        print("\n[Test 2] Getting audio duration...")
        duration_ms = processor.get_audio_duration(str(test_audio))
        duration_sec = duration_ms / 1000
        print(f"   Duration: {duration_ms}ms ({duration_sec:.2f}s)")
        
        # Test 3: Save audio with metadata
        print("\n[Test 3] Saving audio with metadata...")
        metadata = processor.save_audio_with_metadata(
            audio_path=str(test_audio),
            speaker="zoya",
            text="This is a test audio segment for validation.",
            sequence=0,
            segment_id="test_segment_001"
        )
        print(f"   Segment ID: {metadata.segment_id}")
        print(f"   Speaker: {metadata.speaker}")
        print(f"   Duration: {metadata.duration_ms}ms")
        print(f"   Sample Rate: {metadata.sample_rate}Hz")
        print(f"   Channels: {metadata.channels}")
        print(f"   Bitrate: {metadata.bitrate}")
        
        # Test 4: Load metadata
        print("\n[Test 4] Loading metadata...")
        loaded_metadata = processor.load_metadata("test_segment_001")
        if loaded_metadata:
            print(f"   ✅ Loaded metadata for: {loaded_metadata.segment_id}")
            print(f"   Text: {loaded_metadata.text[:50]}...")
        else:
            print("   ❌ Failed to load metadata")
        
        # Test 5: List audio segments
        print("\n[Test 5] Listing audio segments...")
        segments = processor.list_audio_segments()
        print(f"   Found {len(segments)} segments")
        for seg in segments[:3]:  # Show first 3
            print(f"   - {seg.segment_id}: {seg.speaker} ({seg.duration_ms}ms)")
        
        # Test 6: Audio format conversion (optional)
        print("\n[Test 6] Testing audio format conversion...")
        try:
            converted_path = processor.convert_audio_format(
                input_path=str(test_audio),
                output_format="wav",
                sample_rate=22050,
                channels=1,
                bitrate="128k"
            )
            print(f"   ✅ Converted audio: {Path(converted_path).name}")
            
            # Validate converted file
            is_valid_converted = processor.validate_audio_file(converted_path)
            print(f"   Validation: {'✅ Valid' if is_valid_converted else '❌ Invalid'}")
            
        except Exception as e:
            print(f"   ⚠️  Conversion test skipped: {e}")
        
        print("\n" + "=" * 60)
        print("🎉 AudioProcessor tests complete!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_audio_processor()
