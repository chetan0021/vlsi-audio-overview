"""
Test script for question endpoints
"""
import requests
import json


def test_text_question_endpoint():
    """Test the /api/question/text endpoint"""
    print("🧪 Testing Text Question Endpoint\n")
    print("=" * 60)
    
    try:
        # API endpoint
        url = "http://localhost:8000/api/question/text"
        
        # Request payload
        payload = {
            "question": "What's the difference between Moore and Mealy machines?",
            "topic": "FSM Design",
            "context": "We've been discussing Finite State Machines and their basic concepts."
        }
        
        print("\n[Request]")
        print(f"   URL: {url}")
        print(f"   Question: {payload['question']}")
        
        # Make request
        print("\n[Sending request...]")
        response = requests.post(url, json=payload, timeout=60)
        
        # Check response
        print(f"\n[Response]")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success"):
                print(f"   ✅ Success!")
                print(f"\n   Response ID: {data.get('response_id')}")
                print(f"   Question: {data.get('question')}")
                print(f"   Segments: {data.get('segments_count')}")
                print(f"   TTS Enabled: {data.get('tts_enabled', False)}")
                
                # Show response segments
                segments = data.get('segments', [])
                print(f"\n   📝 Response:")
                for i, seg in enumerate(segments):
                    speaker_icon = "👩‍🏫" if seg['speaker'] == "zoya" else "👨‍🎓"
                    print(f"\n   {i+1}. {speaker_icon} {seg['speaker'].upper()}:")
                    print(f"      {seg['text'][:100]}...")
                    if seg.get('audio_url'):
                        print(f"      Audio: {seg['audio_url']}")
                
                print("\n" + "=" * 60)
                print("🎉 Text Question Endpoint Test Successful!")
                print("=" * 60)
                
            else:
                print(f"   ❌ API returned error: {data.get('error')}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error: Backend server not running")
        print("   Start the backend server first:")
        print("   > cd backend")
        print("   > venv\\Scripts\\python.exe -m uvicorn main:app --reload --port 8000")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


def test_voice_question_endpoint():
    """Test the /api/question/voice endpoint (placeholder)"""
    print("\n\n🧪 Testing Voice Question Endpoint\n")
    print("=" * 60)
    
    print("\n⚠️  Voice question endpoint requires:")
    print("   1. Audio file upload")
    print("   2. Audio transcription (Gemini multimodal)")
    print("   3. Microphone access from frontend")
    
    print("\n💡 This endpoint will be tested from the frontend UI")
    print("   when the 'Join Conversation' feature is implemented.")


if __name__ == "__main__":
    test_text_question_endpoint()
    test_voice_question_endpoint()
