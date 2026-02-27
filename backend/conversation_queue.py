"""
Conversation Queue Manager for VLSI Audio Overview
Manages audio segment playback order and response insertion
"""
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class QueueSegment:
    """A segment in the conversation queue"""
    segment_id: str
    speaker: str
    text: str
    sequence: int
    duration_ms: int
    audio_url: Optional[str]
    is_response: bool = False  # True if this is a response to student question
    inserted_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "segment_id": self.segment_id,
            "speaker": self.speaker,
            "text": self.text,
            "sequence": self.sequence,
            "duration_ms": self.duration_ms,
            "audio_url": self.audio_url,
            "is_response": self.is_response,
            "inserted_at": self.inserted_at
        }


class ConversationQueue:
    """Manages the queue of audio segments for playback"""
    
    def __init__(self, overview_id: str):
        """
        Initialize conversation queue
        
        Args:
            overview_id: Identifier for the audio overview
        """
        self.overview_id = overview_id
        self.segments: List[QueueSegment] = []
        self.current_position = 0  # Current playback position
        self.playback_paused = False
        
        print(f"✅ ConversationQueue initialized for {overview_id}")
    
    def load_overview_segments(self, segments: List[Dict[str, Any]]) -> None:
        """
        Load initial overview segments into queue
        
        Args:
            segments: List of segment dictionaries from overview generation
        """
        self.segments = []
        for seg_data in segments:
            segment = QueueSegment(
                segment_id=seg_data["segment_id"],
                speaker=seg_data["speaker"],
                text=seg_data["text"],
                sequence=seg_data["sequence"],
                duration_ms=seg_data.get("duration_ms", 0),
                audio_url=seg_data.get("audio_url"),
                is_response=False
            )
            self.segments.append(segment)
        
        print(f"✅ Loaded {len(self.segments)} segments into queue")
    
    def insert_response(
        self,
        response_segments: List[Dict[str, Any]],
        insert_after_current: bool = True
    ) -> int:
        """
        Insert response segments into the queue
        
        This method:
        1. Takes response segments from question answering
        2. Inserts them after current playback position
        3. Updates sequence numbers for remaining segments
        4. Returns the insertion position
        
        Args:
            response_segments: List of response segment dictionaries
            insert_after_current: If True, insert after current position; 
                                 if False, append to end
            
        Returns:
            Position where segments were inserted
        """
        if not response_segments:
            return self.current_position
        
        # Determine insertion position
        if insert_after_current:
            insert_pos = self.current_position + 1
        else:
            insert_pos = len(self.segments)
        
        # Create QueueSegment objects for responses
        response_queue_segments = []
        for seg_data in response_segments:
            segment = QueueSegment(
                segment_id=seg_data["segment_id"],
                speaker=seg_data["speaker"],
                text=seg_data["text"],
                sequence=seg_data["sequence"],
                duration_ms=seg_data.get("duration_ms", 0),
                audio_url=seg_data.get("audio_url"),
                is_response=True,
                inserted_at=datetime.utcnow().isoformat()
            )
            response_queue_segments.append(segment)
        
        # Insert segments at position
        for i, segment in enumerate(response_queue_segments):
            self.segments.insert(insert_pos + i, segment)
        
        # Update sequence numbers for all segments after insertion
        self._resequence_segments(insert_pos + len(response_queue_segments))
        
        print(f"✅ Inserted {len(response_queue_segments)} response segments at position {insert_pos}")
        return insert_pos
    
    def _resequence_segments(self, start_pos: int) -> None:
        """
        Update sequence numbers for segments after insertion
        
        Args:
            start_pos: Position to start resequencing from
        """
        for i in range(start_pos, len(self.segments)):
            self.segments[i].sequence = i
    
    def get_next_segment(self) -> Optional[QueueSegment]:
        """
        Get the next segment for playback
        
        Returns:
            Next QueueSegment or None if at end
        """
        if self.current_position >= len(self.segments):
            return None
        
        segment = self.segments[self.current_position]
        return segment
    
    def advance(self) -> bool:
        """
        Advance to next segment
        
        Returns:
            True if advanced, False if at end
        """
        if self.current_position < len(self.segments) - 1:
            self.current_position += 1
            return True
        return False
    
    def seek(self, position: int) -> bool:
        """
        Seek to specific position in queue
        
        Args:
            position: Target position (0-indexed)
            
        Returns:
            True if seek successful, False if position invalid
        """
        if 0 <= position < len(self.segments):
            self.current_position = position
            return True
        return False
    
    def get_current_position(self) -> int:
        """Get current playback position"""
        return self.current_position
    
    def get_total_segments(self) -> int:
        """Get total number of segments in queue"""
        return len(self.segments)
    
    def get_remaining_segments(self) -> int:
        """Get number of segments remaining after current position"""
        return len(self.segments) - self.current_position - 1
    
    def get_queue_state(self) -> Dict[str, Any]:
        """
        Get complete queue state
        
        Returns:
            Dictionary with queue state information
        """
        return {
            "overview_id": self.overview_id,
            "total_segments": len(self.segments),
            "current_position": self.current_position,
            "remaining_segments": self.get_remaining_segments(),
            "playback_paused": self.playback_paused,
            "segments": [seg.to_dict() for seg in self.segments]
        }
    
    def get_segment_by_id(self, segment_id: str) -> Optional[QueueSegment]:
        """
        Get segment by ID
        
        Args:
            segment_id: Segment identifier
            
        Returns:
            QueueSegment or None if not found
        """
        for segment in self.segments:
            if segment.segment_id == segment_id:
                return segment
        return None
    
    def pause(self) -> None:
        """Pause playback"""
        self.playback_paused = True
    
    def resume(self) -> None:
        """Resume playback"""
        self.playback_paused = False
    
    def is_paused(self) -> bool:
        """Check if playback is paused"""
        return self.playback_paused


# Global queue manager
_queues: Dict[str, ConversationQueue] = {}

def get_conversation_queue(overview_id: str) -> ConversationQueue:
    """
    Get or create conversation queue for an overview
    
    Args:
        overview_id: Overview identifier
        
    Returns:
        ConversationQueue instance
    """
    if overview_id not in _queues:
        _queues[overview_id] = ConversationQueue(overview_id)
    return _queues[overview_id]

def clear_queue(overview_id: str) -> None:
    """
    Clear conversation queue for an overview
    
    Args:
        overview_id: Overview identifier
    """
    if overview_id in _queues:
        del _queues[overview_id]
        print(f"✅ Cleared queue for {overview_id}")
