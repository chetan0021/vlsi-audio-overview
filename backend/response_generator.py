"""
Response Generator for VLSI Audio Overview
Handles student question responses with context awareness
"""
from typing import List, Optional
from gemini_client import get_gemini_client, DialogueSegment


class ResponseGenerator:
    """Generates contextual responses to student questions"""
    
    def __init__(self):
        """Initialize response generator"""
        self.gemini_client = get_gemini_client()
        print("✅ ResponseGenerator initialized")
    
    async def transcribe_audio(self, audio_data: bytes) -> str:
        """
        Transcribe audio input to text using Gemini
        
        Args:
            audio_data: Audio file bytes
            
        Returns:
            Transcribed text
        """
        # Use Gemini client's transcription method
        transcription = await self.gemini_client.transcribe_audio(audio_data)
        return transcription
    
    async def generate_response(
        self,
        question: str,
        topic: str,
        context: Optional[str] = None
    ) -> List[DialogueSegment]:
        """
        Generate contextual response to student question
        
        This method:
        1. Takes student's question
        2. Considers the current topic and conversation context
        3. Generates a natural response as dialogue between Zoya and Ravi
        4. Ensures both speakers participate in the response
        
        Args:
            question: Student's question text
            topic: Current topic being discussed
            context: Optional conversation context (previous dialogue)
            
        Returns:
            List of DialogueSegment objects (response from both speakers)
        """
        # Build context string if not provided
        if context is None:
            context = f"We are discussing {topic} in an educational podcast format."
        
        # Generate response using Gemini
        response_segments = await self.gemini_client.generate_response(
            question=question,
            context=context,
            topic=topic
        )
        
        # Validate that both speakers are present
        speakers = set(seg.speaker for seg in response_segments)
        if len(speakers) < 2:
            print(f"⚠️  Warning: Response only has {len(speakers)} speaker(s)")
        
        print(f"✅ Generated response with {len(response_segments)} segments")
        return response_segments
    
    async def process_voice_question(
        self,
        audio_data: bytes,
        topic: str,
        context: Optional[str] = None
    ) -> tuple[str, List[DialogueSegment]]:
        """
        Process voice question: transcribe and generate response
        
        This is the complete pipeline for voice input:
        1. Transcribe audio to text
        2. Generate contextual response
        
        Args:
            audio_data: Audio file bytes
            topic: Current topic
            context: Optional conversation context
            
        Returns:
            Tuple of (transcribed_question, response_segments)
        """
        # Step 1: Transcribe audio
        print("🎤 Transcribing audio...")
        question = await self.transcribe_audio(audio_data)
        print(f"   Transcribed: {question}")
        
        # Step 2: Generate response
        print("💬 Generating response...")
        response_segments = await self.generate_response(
            question=question,
            topic=topic,
            context=context
        )
        
        return question, response_segments
    
    def validate_response_relevance(
        self,
        question: str,
        response_segments: List[DialogueSegment]
    ) -> bool:
        """
        Validate that response is relevant to the question
        
        Simple heuristic: check if key words from question appear in response
        
        Args:
            question: Original question
            response_segments: Generated response segments
            
        Returns:
            True if response appears relevant
        """
        # Extract key words from question (simple approach)
        question_words = set(
            word.lower() 
            for word in question.split() 
            if len(word) > 3 and word.isalpha()
        )
        
        # Get all response text
        response_text = " ".join(seg.text.lower() for seg in response_segments)
        
        # Check overlap
        matches = sum(1 for word in question_words if word in response_text)
        relevance_score = matches / len(question_words) if question_words else 0
        
        is_relevant = relevance_score > 0.2  # At least 20% word overlap
        
        if not is_relevant:
            print(f"⚠️  Warning: Response may not be relevant (score: {relevance_score:.2f})")
        
        return is_relevant


# Global generator instance
_generator: Optional[ResponseGenerator] = None

def get_response_generator() -> ResponseGenerator:
    """Get the global ResponseGenerator instance"""
    global _generator
    if _generator is None:
        _generator = ResponseGenerator()
    return _generator
