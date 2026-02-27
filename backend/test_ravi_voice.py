"""
Test script for Ravi's voice only
"""
import os
os.environ['COQUI_TOS_AGREED'] = '1'

from tts_engine import get_tts_engine


def test_ravi_voice():
    """Test only Ravi's voice with the new sample"""
    print("🧪 Testing Ravi's Voice with New Sample...\n")
    print("=" * 60)
    
    try:
        # Initialize TTS engine
        print("\n🔧 Initializing TTS engine...")
        engine = get_tts_engine()
        
        # Test Ravi's voice with multiple sentences
        print("\n" + "=" * 60)
        print("📝 Testing Ravi's voice...")
        print("=" * 60)
        
        test_texts = [
            "Hi! I'm Ravi, your co-host for this VLSI learning journey.",
            "I'm excited to explore Finite State Machines with you today.",
            "Can you explain what makes FSMs so fundamental in digital design?"
        ]
        
        for i, text in enumerate(test_texts, 1):
            print(f"\n[Test {i}/3] Generating: {text[:50]}...")
            ravi_audio = engine.synthesize(text, "ravi")
            print(f"✅ Audio generated: {ravi_audio}")
        
        print("\n" + "=" * 60)
        print("🎉 Ravi's voice test complete!")
        print("=" * 60)
        print("\n💡 Check the audio files in 'backend/audio_storage/' directory")
        print("💡 Listen to verify the voice quality is better (less breathing)")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_ravi_voice()
