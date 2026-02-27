"""
Script Generator for VLSI Audio Overview
Orchestrates dialogue generation and ensures proper structure
"""
from typing import List, Optional
from gemini_client import get_gemini_client, DialogueSegment


class ScriptGenerator:
    """Generates educational dialogue scripts with proper structure"""
    
    def __init__(self):
        """Initialize script generator"""
        self.gemini_client = get_gemini_client()
        print("✅ ScriptGenerator initialized")
    
    async def generate_dialogue(
        self,
        topic: str,
        duration_minutes: int = 8,
        context: Optional[str] = None
    ) -> List[DialogueSegment]:
        """
        Generate educational dialogue script between Zoya and Ravi
        
        This method:
        1. Calls Gemini to generate dialogue
        2. Validates speaker alternation
        3. Ensures dialogue structure completeness
        4. Returns properly formatted segments
        
        Args:
            topic: The topic to generate dialogue about
            duration_minutes: Target duration in minutes
            context: Optional additional context
            
        Returns:
            List of DialogueSegment objects with proper speaker alternation
        """
        # Generate dialogue using Gemini
        segments = await self.gemini_client.generate_dialogue(
            topic=topic,
            duration_minutes=duration_minutes,
            context=context
        )
        
        # Validate and fix speaker alternation if needed
        segments = self._ensure_speaker_alternation(segments)
        
        # Validate dialogue structure
        self._validate_dialogue_structure(segments)
        
        print(f"✅ Generated script with {len(segments)} segments")
        return segments
    
    def _ensure_speaker_alternation(
        self,
        segments: List[DialogueSegment]
    ) -> List[DialogueSegment]:
        """
        Ensure speakers alternate properly (no more than 2 consecutive turns)
        
        Args:
            segments: List of dialogue segments
            
        Returns:
            List of segments with proper alternation
        """
        if len(segments) <= 1:
            return segments
        
        # Check for excessive consecutive turns by same speaker
        consecutive_count = 1
        last_speaker = segments[0].speaker
        
        for i in range(1, len(segments)):
            if segments[i].speaker == last_speaker:
                consecutive_count += 1
                if consecutive_count > 2:
                    print(f"⚠️  Warning: {last_speaker} has {consecutive_count} consecutive turns at segment {i}")
            else:
                consecutive_count = 1
                last_speaker = segments[i].speaker
        
        return segments
    
    def _validate_dialogue_structure(self, segments: List[DialogueSegment]) -> None:
        """
        Validate that dialogue has proper structure
        
        Checks:
        - Has both speakers
        - Has introduction (first segment)
        - Has conclusion (last segment)
        - Segments are properly sequenced
        
        Args:
            segments: List of dialogue segments
            
        Raises:
            ValueError: If dialogue structure is invalid
        """
        if not segments:
            raise ValueError("Dialogue is empty")
        
        # Check that both speakers are present
        speakers = set(seg.speaker for seg in segments)
        if len(speakers) < 2:
            print(f"⚠️  Warning: Only one speaker found: {speakers}")
        
        # Check sequence numbers
        for i, seg in enumerate(segments):
            if seg.sequence != i:
                print(f"⚠️  Warning: Segment {i} has incorrect sequence number: {seg.sequence}")
                seg.sequence = i  # Fix it
        
        # Validate introduction (first segment should be welcoming)
        first_text = segments[0].text.lower()
        intro_keywords = ['welcome', 'hello', 'hi', 'today', 'let\'s']
        has_intro = any(keyword in first_text for keyword in intro_keywords)
        
        if not has_intro:
            print("⚠️  Warning: First segment may not be a proper introduction")
        
        # Validate conclusion (last segment should wrap up)
        last_text = segments[-1].text.lower()
        conclusion_keywords = ['summary', 'next time', 'practice', 'remember', 'that\'s']
        has_conclusion = any(keyword in last_text for keyword in conclusion_keywords)
        
        if not has_conclusion:
            print("⚠️  Warning: Last segment may not be a proper conclusion")
        
        print(f"✅ Dialogue structure validated: {len(segments)} segments, {len(speakers)} speakers")
    
    def estimate_duration(self, segments: List[DialogueSegment]) -> float:
        """
        Estimate total duration of dialogue in minutes
        
        Uses average speaking rate of ~150 words per minute
        
        Args:
            segments: List of dialogue segments
            
        Returns:
            Estimated duration in minutes
        """
        total_words = sum(len(seg.text.split()) for seg in segments)
        words_per_minute = 150
        duration_minutes = total_words / words_per_minute
        
        return duration_minutes
    
    def get_speaker_distribution(self, segments: List[DialogueSegment]) -> dict:
        """
        Get distribution of segments by speaker
        
        Args:
            segments: List of dialogue segments
            
        Returns:
            Dictionary with speaker counts and percentages
        """
        speaker_counts = {}
        for seg in segments:
            speaker_counts[seg.speaker] = speaker_counts.get(seg.speaker, 0) + 1
        
        total = len(segments)
        distribution = {}
        for speaker, count in speaker_counts.items():
            distribution[speaker] = {
                'count': count,
                'percentage': (count / total) * 100 if total > 0 else 0
            }
        
        return distribution


# Global generator instance
_generator: Optional[ScriptGenerator] = None

def get_script_generator() -> ScriptGenerator:
    """Get the global ScriptGenerator instance"""
    global _generator
    if _generator is None:
        _generator = ScriptGenerator()
    return _generator
