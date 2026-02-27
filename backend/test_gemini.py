"""
Simple test script for Gemini dialogue generation
Run this to test if Gemini API is working
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Simple test without the full app
async def test_gemini():
    """Test Gemini API directly"""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env")
        return
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    print("\n🧪 Testing Gemini API...")
    print("Note: This test requires Python 3.9-3.11 for full compatibility")
    print("With Python 3.14, some features may not work\n")
    
    try:
        import google.generativeai as genai
        print("✅ google.generativeai imported successfully")
        
        genai.configure(api_key=api_key)
        print("✅ Gemini configured with API key")
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        print("✅ Model initialized: gemini-2.5-flash")
        
        # Simple test prompt
        print("\n📝 Generating test dialogue...")
        response = model.generate_content(
            "Generate a 2-line dialogue between a teacher and student about FSM. Format as JSON: [{\"speaker\": \"teacher\", \"text\": \"...\"}, {\"speaker\": \"student\", \"text\": \"...\"}]"
        )
        
        print("\n✅ Response received:")
        print(response.text)
        
        print("\n🎉 Gemini API is working!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nThis is likely due to Python 3.14 compatibility issues.")
        print("The Gemini client will work when we use Python 3.9-3.11")

if __name__ == "__main__":
    asyncio.run(test_gemini())
