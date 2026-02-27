"""
Test script for TTS Engine
Run this to test voice synthesis with Coqui TTS XTTS-v2
"""
from tts_engine import get_tts_engine


def test_tts():
    """Test TTS engine with sample text"""
    print("🧪 Testing Coqui TTS Engine with XTTS-v2...\n")
    print("=" * 60)
    
    try:
        # Initialize TTS engine
        print("\n🔧 Initializing TTS engine...")
        engine = get_tts_engine()
        
        # Test Zoya's voice (cloned from samples)
        print("\n" + "=" * 60)
        print("📝 Testing Zoya's cloned voice...")
        print("=" * 60)
        zoya_text = "Hello! I'm Zoya, your VLSI instructor. Today we'll explore Finite State Machines and their applications in digital design."
        zoya_audio = engine.synthesize(zoya_text, "zoya")
        print(f"✅ Zoya audio generated: {zoya_audio}")
        
        # Test Ravi's voice (natural male voice)
        print("\n" + "=" * 60)
        print("📝 Testing Ravi's voice...")
        print("=" * 60)
        ravi_text = "Hi! I'm Ravi, your co-host. I'm excited to explore FSMs with you. Can you explain what makes them so fundamental?"
        ravi_audio = engine.synthesize(ravi_text, "ravi")
        print(f"✅ Ravi audio generated: {ravi_audio}")
        
        # Test dialogue synthesis
        print("\n" + "=" * 60)
        print("📝 Testing dialogue synthesis...")
        print("=" * 60)
        dialogue = [
            {"speaker": "zoya", "text": "Let's start with the basics of Finite State Machines. They're fundamental building blocks in digital design."},
            {"speaker": "ravi", "text": "I've heard FSMs are everywhere in digital systems. What exactly makes them so important?"},
            {"speaker": "zoya", "text": "Great question! An FSM is a mathematical model that can be in one of a finite number of states at any given time. Think of a traffic light - it has distinct states like red, yellow, and green."},
            {"speaker": "ravi", "text": "Ah, that's a perfect analogy! So the traffic light transitions between these states based on timing or sensors?"},
            {"speaker": "zoya", "text": "Exactly! Those transitions are what make FSMs powerful. They respond to inputs and change states in a predictable, controlled way."}
        ]
        
        results = engine.synthesize_dialogue(dialogue)
        
        print("\n" + "=" * 60)
        print(f"✅ Generated {len(results)} audio files:")
        print("=" * 60)
        
        for i, result in enumerate(results, 1):
            print(f"   [{i}] {result['speaker'].upper()}: {result['audio_path']}")
        
        print("\n" + "=" * 60)
        print("🎉 TTS Engine is working with Coqui TTS!")
        print("=" * 60)
        print("\n💡 Generated audio files are in the 'audio_storage' directory")
        print("💡 Play them to hear the natural, podcast-like voices!")
        print("💡 Zoya's voice is cloned from the samples in voice_samples/zoya/")
        print("\n📊 Voice Quality:")
        print("   - Zoya: Cloned from actual voice samples (natural)")
        print("   - Ravi: Natural male voice (co-host)")
        print("\n✨ This is much better than robotic TTS!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔍 Troubleshooting:")
        print("   1. Make sure you're running this with Python 3.10 environment:")
        print("      .\\venv_tts\\Scripts\\python.exe test_tts.py")
        print("   2. Ensure TTS library is installed:")
        print("      .\\venv_tts\\Scripts\\pip.exe install TTS")
        print("   3. Check that voice samples exist in voice_samples/zoya/")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_tts()
