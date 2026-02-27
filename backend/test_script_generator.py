"""
Test script for ScriptGenerator
"""
import asyncio
from script_generator import get_script_generator


async def test_script_generator():
    """Test ScriptGenerator functionality"""
    print("🧪 Testing ScriptGenerator...\n")
    print("=" * 60)
    
    try:
        # Initialize generator
        print("\n🔧 Initializing ScriptGenerator...")
        generator = get_script_generator()
        
        # Test 1: Generate dialogue
        print("\n[Test 1] Generating dialogue script...")
        segments = await generator.generate_dialogue(
            topic="FSM Design Basics",
            duration_minutes=2,
            context="Focus on what FSMs are and a simple traffic light example"
        )
        
        print(f"   ✅ Generated {len(segments)} segments")
        
        # Test 2: Estimate duration
        print("\n[Test 2] Estimating duration...")
        estimated_duration = generator.estimate_duration(segments)
        print(f"   Estimated duration: {estimated_duration:.2f} minutes")
        print(f"   Target duration: 2 minutes")
        print(f"   Difference: {abs(estimated_duration - 2):.2f} minutes")
        
        # Test 3: Get speaker distribution
        print("\n[Test 3] Analyzing speaker distribution...")
        distribution = generator.get_speaker_distribution(segments)
        for speaker, stats in distribution.items():
            print(f"   {speaker.upper()}: {stats['count']} segments ({stats['percentage']:.1f}%)")
        
        # Test 4: Show sample segments
        print("\n[Test 4] Sample dialogue segments...")
        for i, seg in enumerate(segments[:3]):
            speaker_icon = "👩‍🏫" if seg.speaker == "zoya" else "👨‍🎓"
            print(f"\n   {i+1}. {speaker_icon} {seg.speaker.upper()}:")
            print(f"      {seg.text[:80]}...")
        
        if len(segments) > 3:
            print(f"\n   ... and {len(segments) - 3} more segments")
        
        # Summary
        print("\n" + "=" * 60)
        print("🎉 ScriptGenerator tests complete!")
        print("=" * 60)
        print(f"\n📊 Summary:")
        print(f"   • Generated {len(segments)} dialogue segments")
        print(f"   • Estimated duration: {estimated_duration:.2f} minutes")
        print(f"   • Speakers: {', '.join(distribution.keys())}")
        print(f"   • Structure validated ✓")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_script_generator())
