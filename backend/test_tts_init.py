"""
Simple test to initialize TTS engine and check if model downloads
"""
import os
os.environ['COQUI_TOS_AGREED'] = '1'

print("🧪 Testing TTS Engine Initialization...\n")
print("=" * 60)
print("This will download the XTTS-v2 model (~2GB) on first run.")
print("Please be patient, this may take 5-10 minutes depending on your connection.")
print("=" * 60)

try:
    from tts_engine import get_tts_engine
    
    print("\n🔧 Initializing TTS engine...")
    engine = get_tts_engine()
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS! TTS Engine initialized successfully!")
    print("=" * 60)
    print("\nYou can now run the full test:")
    print("   .\\venv_tts\\Scripts\\python.exe test_tts_auto.py")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
