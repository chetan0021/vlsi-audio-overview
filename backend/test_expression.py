"""
Test script to compare different expression settings
"""
import os
os.environ['COQUI_TOS_AGREED'] = '1'

from tts_engine import get_tts_engine


def test_expression_settings():
    """Test different temperature and repetition penalty settings"""
    print("🧪 Testing Expression Settings for Natural Speech...\n")
    print("=" * 60)
    
    try:
        # Initialize TTS engine
        print("\n🔧 Initializing TTS engine...")
        engine = get_tts_engine()
        
        # Test text with emotion/expression
        test_text = "Great question! I'm really excited to explain this. FSMs are absolutely fundamental in digital design!"
        
        # Test different settings
        settings = [
            {"name": "Balanced (Default)", "temp": 0.75, "rep_pen": 5.0},
            {"name": "More Expressive", "temp": 0.85, "rep_pen": 7.0},
            {"name": "More Consistent", "temp": 0.65, "rep_pen": 3.0},
        ]
        
        # Test both Zoya and Ravi
        for speaker in ["zoya", "ravi"]:
            print("\n" + "=" * 60)
            print(f"📝 Testing {speaker.capitalize()}'s voice with different expression settings...")
            print("=" * 60)
            print(f"\nTest text: \"{test_text}\"")
            
            for i, setting in enumerate(settings, 1):
                print(f"\n[Test {i}/3] {setting['name']}")
                print(f"   Temperature: {setting['temp']}, Repetition Penalty: {setting['rep_pen']}")
                
                audio_file = engine.synthesize(
                    test_text, 
                    speaker,
                    temperature=setting['temp'],
                    repetition_penalty=setting['rep_pen']
                )
                print(f"   ✅ Generated: {audio_file}")
        
        print("\n" + "=" * 60)
        print("🎉 Expression test complete!")
        print("=" * 60)
        print("\n💡 Listen to the 6 audio files (3 for each speaker) and compare:")
        print("   1. Balanced - Good for most content")
        print("   2. More Expressive - Better for emotional/excited speech")
        print("   3. More Consistent - Better for technical/formal content")
        print("\n📁 Files are in: backend/audio_storage/")
        print("\n🔍 Compare Zoya and Ravi's expression quality with these settings")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_expression_settings()
