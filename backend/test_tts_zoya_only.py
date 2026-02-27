"""
Test script specifically for Zoya's voice with multi-sample cloning
"""
import os
os.environ['COQUI_TOS_AGREED'] = '1'

from tts_engine import get_tts_engine


def test_zoya_expression():
    """Test Zoya's voice with improved multi-sample cloning"""
    print("🧪 Testing Zoya's Voice Expression with Multi-Sample Cloning...\n")
    print("=" * 60)
    
    try:
        # Initialize TTS engine
        print("\n🔧 Initializing TTS engine...")
        engine = get_tts_engine()
        
        # Test texts with different emotions
        test_cases = [
            {
                "text": "Welcome to our VLSI design overview! I'm so excited to dive into FSM design with you today.",
                "emotion": "Excited/Welcoming"
            },
            {
                "text": "Now, let's carefully examine the state transition diagram. Notice how each state connects to the next.",
                "emotion": "Instructional/Calm"
            },
            {
                "text": "That's a fantastic question! The Moore machine outputs depend only on the current state.",
                "emotion": "Enthusiastic/Responsive"
            }
        ]
        
        print("\n" + "=" * 60)
        print("📝 Testing Zoya's voice with different emotional contexts...")
        print("=" * 60)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n[Test {i}/3] {test_case['emotion']}")
            print(f"   Text: \"{test_case['text'][:60]}...\"")
            
            # Use balanced settings (good for most content)
            audio_file = engine.synthesize(
                test_case['text'], 
                "zoya",
                temperature=0.75,
                repetition_penalty=5.0
            )
            print(f"   ✅ Generated: {audio_file}")
        
        print("\n" + "=" * 60)
        print("🎉 Zoya expression test complete!")
        print("=" * 60)
        print("\n💡 The multi-sample approach should provide:")
        print("   ✓ Better emotional range")
        print("   ✓ More natural expression")
        print("   ✓ Consistent voice quality")
        print("\n📁 Files are in: backend/audio_storage/")
        print("\n🎧 Listen to the 3 audio files and check if expressions sound natural")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_zoya_expression()
