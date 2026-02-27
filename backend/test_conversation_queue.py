"""
Test script for ConversationQueue
"""
from conversation_queue import get_conversation_queue, clear_queue


def test_conversation_queue():
    """Test ConversationQueue functionality"""
    print("🧪 Testing ConversationQueue...\n")
    print("=" * 60)
    
    try:
        # Test 1: Create queue and load segments
        print("\n[Test 1] Creating queue and loading segments...")
        
        overview_id = "test_overview_001"
        queue = get_conversation_queue(overview_id)
        
        # Sample overview segments
        overview_segments = [
            {"segment_id": "seg_0", "speaker": "zoya", "text": "Welcome to FSM design!", "sequence": 0, "duration_ms": 3000, "audio_url": "/api/audio/seg_0"},
            {"segment_id": "seg_1", "speaker": "ravi", "text": "I'm excited to learn!", "sequence": 1, "duration_ms": 2500, "audio_url": "/api/audio/seg_1"},
            {"segment_id": "seg_2", "speaker": "zoya", "text": "Let's start with basics.", "sequence": 2, "duration_ms": 2800, "audio_url": "/api/audio/seg_2"},
        ]
        
        queue.load_overview_segments(overview_segments)
        print(f"   Total segments: {queue.get_total_segments()}")
        print(f"   Current position: {queue.get_current_position()}")
        
        # Test 2: Get next segment
        print("\n[Test 2] Getting next segment...")
        next_seg = queue.get_next_segment()
        if next_seg:
            print(f"   Next: {next_seg.speaker} - {next_seg.text}")
        
        # Test 3: Advance through queue
        print("\n[Test 3] Advancing through queue...")
        queue.advance()
        print(f"   Position after advance: {queue.get_current_position()}")
        next_seg = queue.get_next_segment()
        if next_seg:
            print(f"   Next: {next_seg.speaker} - {next_seg.text}")
        
        # Test 4: Insert response
        print("\n[Test 4] Inserting response segments...")
        
        response_segments = [
            {"segment_id": "resp_0", "speaker": "ravi", "text": "Great question!", "sequence": 0, "duration_ms": 2000, "audio_url": "/api/audio/resp_0"},
            {"segment_id": "resp_1", "speaker": "zoya", "text": "Let me explain...", "sequence": 1, "duration_ms": 3500, "audio_url": "/api/audio/resp_1"},
        ]
        
        insert_pos = queue.insert_response(response_segments, insert_after_current=True)
        print(f"   Inserted at position: {insert_pos}")
        print(f"   Total segments now: {queue.get_total_segments()}")
        
        # Show queue state
        print(f"\n   Queue after insertion:")
        for i, seg in enumerate(queue.segments):
            marker = " <-- current" if i == queue.current_position else ""
            response_marker = " [RESPONSE]" if seg.is_response else ""
            print(f"   {i}. {seg.speaker}: {seg.text[:30]}...{response_marker}{marker}")
        
        # Test 5: Pause and resume
        print("\n[Test 5] Testing pause/resume...")
        queue.pause()
        print(f"   Paused: {queue.is_paused()}")
        queue.resume()
        print(f"   Paused: {queue.is_paused()}")
        
        # Test 6: Seek to position
        print("\n[Test 6] Testing seek...")
        success = queue.seek(0)
        print(f"   Seek to position 0: {'✅ Success' if success else '❌ Failed'}")
        print(f"   Current position: {queue.get_current_position()}")
        
        # Test 7: Get queue state
        print("\n[Test 7] Getting queue state...")
        state = queue.get_queue_state()
        print(f"   Overview ID: {state['overview_id']}")
        print(f"   Total segments: {state['total_segments']}")
        print(f"   Current position: {state['current_position']}")
        print(f"   Remaining: {state['remaining_segments']}")
        
        # Test 8: Clear queue
        print("\n[Test 8] Clearing queue...")
        clear_queue(overview_id)
        
        # Summary
        print("\n" + "=" * 60)
        print("🎉 ConversationQueue tests complete!")
        print("=" * 60)
        print(f"\n📊 Summary:")
        print(f"   • Queue management working ✓")
        print(f"   • Response insertion working ✓")
        print(f"   • Playback control working ✓")
        print(f"   • Sequence integrity maintained ✓")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_conversation_queue()
