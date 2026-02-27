"""
Test the API endpoint for audio overview generation
"""
import requests
import json


def test_generate_overview_endpoint():
    """Test the /api/overview/generate endpoint"""
    print("🧪 Testing API Endpoint: /api/overview/generate\n")
    print("=" * 60)
    
    try:
        # API endpoint
        url = "http://localhost:8000/api/overview/generate"
        
        # Request payload
        payload = {
            "topic": "FSM Design Basics",
            "duration_minutes": 2,
            "context": "Focus on what FSMs are and a simple traffic light example"
        }
        
        print("\n[Request]")
        print(f"   URL: {url}")
        print(f"   Payload: {json.dumps(payload, indent=2)}")
        
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
                print(f"\n   Overview ID: {data.get('overview_id')}")
                print(f"   Topic: {data.get('topic')}")
                print(f"   Segments: {data.get('segments_count')}")
                print(f"   TTS Enabled: {data.get('tts_enabled', False)}")
                print(f"   Note: {data.get('note')}")
                
                # Show first 3 segments
                segments = data.get('segments', [])
                print(f"\n   📝 Sample Segments:")
                for i, seg in enumerate(segments[:3]):
                    speaker_icon = "👩‍🏫" if seg['speaker'] == "zoya" else "👨‍🎓"
                    print(f"\n   {i+1}. {speaker_icon} {seg['speaker'].upper()}:")
                    print(f"      {seg['text'][:70]}...")
                    if seg.get('audio_url'):
                        print(f"      Audio: {seg['audio_url']}")
                
                if len(segments) > 3:
                    print(f"\n   ... and {len(segments) - 3} more segments")
                
                print("\n" + "=" * 60)
                print("🎉 API Endpoint Test Successful!")
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


if __name__ == "__main__":
    test_generate_overview_endpoint()
