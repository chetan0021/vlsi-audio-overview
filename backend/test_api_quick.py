"""
Quick API test - just check if TTS service is available
"""
import requests
import json

print("Testing API with 2-minute dialogue...")

# Test dialogue generation (without waiting for TTS)
response = requests.post(
    "http://localhost:8000/api/overview/generate",
    json={
        "topic": "FSM Design Basics",
        "duration_minutes": 2,
        "context": "Brief introduction to FSM fundamentals and one simple example"
    },
    timeout=300  # 5 minutes timeout
)

data = response.json()

print(f"\nSuccess: {data.get('success')}")
print(f"TTS Enabled: {data.get('tts_enabled')}")
print(f"Segments: {data.get('segments_count')}")
print(f"Note: {data.get('note')}")

if data.get('segments'):
    print(f"\nSegment details:")
    for i, seg in enumerate(data['segments'][:5]):  # Show first 5
        print(f"\n  [{i+1}] {seg['speaker']}: {seg['text'][:80]}...")
        print(f"      Audio URL: {seg['audio_url']}")
        print(f"      Duration: {seg['duration_ms']}ms")
    
    # Count how many have audio
    with_audio = sum(1 for s in data['segments'] if s['audio_url'])
    print(f"\n✅ Segments with audio: {with_audio}/{data.get('segments_count')}")
