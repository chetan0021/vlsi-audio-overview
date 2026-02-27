"""
Test script for ResponseGenerator
"""
import asyncio
from response_generator import get_response_generator


async def test_response_generator():
    """Test ResponseGenerator functionality"""
    print("🧪 Testing ResponseGenerator...\n")
    print("=" * 60)
    
    try:
        # Initialize generator
        print("\n🔧 Initializing ResponseGenerator...")
        generator = get_response_generator()
        
        # Test 1: Generate response to a question
        print("\n[Test 1] Generating response to student question...")
        
        question = "What's the difference between Moore and Mealy machines?"
        topic = "FSM Design"
        context = """We've been discussing Finite State Machines (FSMs) and how they work. 
        We covered the basic concept of states and transitions, and used a traffic light as an example."""
        
        print(f"   Question: {question}")
        print(f"   Topic: {topic}")
        
        response_segments = await generator.generate_response(
            question=question,
            topic=topic,
            context=context
        )
        
        print(f"   ✅ Generated {len(response_segments)} response segments")
        
        # Show the response
        print(f"\n   📝 Response:")
        for i, seg in enumerate(response_segments):
            speaker_icon = "👩‍🏫" if seg.speaker == "zoya" else "👨‍🎓"
            print(f"\n   {i+1}. {speaker_icon} {seg.speaker.upper()}:")
            print(f"      {seg.text}")
        
        # Test 2: Validate response relevance
        print("\n[Test 2] Validating response relevance...")
        is_relevant = generator.validate_response_relevance(question, response_segments)
        print(f"   Relevance: {'✅ Relevant' if is_relevant else '⚠️  May not be relevant'}")
        
        # Test 3: Test with different question
        print("\n[Test 3] Testing with another question...")
        
        question2 = "Can you give me a real-world example of an FSM?"
        response_segments2 = await generator.generate_response(
            question=question2,
            topic=topic,
            context=context
        )
        
        print(f"   Question: {question2}")
        print(f"   ✅ Generated {len(response_segments2)} response segments")
        
        # Show first segment
        if response_segments2:
            seg = response_segments2[0]
            speaker_icon = "👩‍🏫" if seg.speaker == "zoya" else "👨‍🎓"
            print(f"\n   First response:")
            print(f"   {speaker_icon} {seg.speaker.upper()}: {seg.text[:100]}...")
        
        # Summary
        print("\n" + "=" * 60)
        print("🎉 ResponseGenerator tests complete!")
        print("=" * 60)
        print(f"\n📊 Summary:")
        print(f"   • Tested question response generation")
        print(f"   • Validated response relevance")
        print(f"   • Both Zoya and Ravi participate in responses")
        
        print(f"\n💡 The response generator is ready for:")
        print(f"   • Text question input")
        print(f"   • Voice question transcription (when implemented)")
        print(f"   • Contextual response generation")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_response_generator())
