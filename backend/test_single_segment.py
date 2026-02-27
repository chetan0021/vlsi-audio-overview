"""
Test single segment TTS synthesis
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from tts_service import get_tts_service

print("=" * 60)
print("TESTING SINGLE SEGMENT TTS")
print("=" * 60)

# Initialize service
print("\n🎤 Initializing TTS Service...")
tts_service = get_tts_service()

if not tts_service.tts_available:
    print("❌ TTS Service not available")
    sys.exit(1)

print("✅ TTS Service initialized")

# Test Zoya
print("\n🎬 Testing Zoya voice...")
audio_path = tts_service.synthesize(
    text="Welcome to VLSI Unpacked! Today we're exploring Finite State Machines.",
    speaker="zoya",
    temperature=0.75,
    repetition_penalty=5.0
)

if audio_path:
    print(f"✅ Zoya audio generated: {audio_path}")
    if os.path.exists(audio_path):
        print(f"   File size: {os.path.getsize(audio_path):,} bytes")
else:
    print("❌ Failed")
    sys.exit(1)

# Test Ravi
print("\n🎬 Testing Ravi voice...")
audio_path = tts_service.synthesize(
    text="That sounds fascinating! I'm excited to learn about FSMs.",
    speaker="ravi",
    temperature=0.75,
    repetition_penalty=5.0
)

if audio_path:
    print(f"✅ Ravi audio generated: {audio_path}")
    if os.path.exists(audio_path):
        print(f"   File size: {os.path.getsize(audio_path):,} bytes")
else:
    print("❌ Failed")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED")
print("=" * 60)
