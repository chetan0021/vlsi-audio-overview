"""
Gemini API Client for VLSI Audio Overview
Handles dialogue generation, transcription, and question answering
"""
import google.generativeai as genai
from typing import List, Dict, Optional
from pydantic import BaseModel
import json

from config import get_config


class DialogueSegment(BaseModel):
    """A single segment of dialogue"""
    speaker: str  # "zoya" or "ravi"
    text: str
    sequence: int = 0


class GeminiClient:
    """Client for interacting with Google Gemini API"""
    
    def __init__(self):
        """Initialize Gemini client with API key from config"""
        config = get_config()
        genai.configure(api_key=config.gemini_api_key)
        
        # Use Gemini 2.5 Flash for fast generation
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        print("✅ Gemini client initialized")
    
    async def generate_dialogue(
        self, 
        topic: str, 
        duration_minutes: int = 8,
        context: Optional[str] = None
    ) -> List[DialogueSegment]:
        """
        Generate educational dialogue script between Zoya and Ravi
        
        Args:
            topic: The topic to generate dialogue about (e.g., "FSM Design")
            duration_minutes: Target duration in minutes (default: 8)
            context: Optional additional context or specific points to cover
            
        Returns:
            List of DialogueSegment objects
        """
        prompt = self._build_dialogue_prompt(topic, duration_minutes, context)
        
        try:
            response = self.model.generate_content(prompt)
            dialogue_data = self._parse_dialogue_response(response.text)
            
            # Convert to DialogueSegment objects
            segments = []
            for i, item in enumerate(dialogue_data):
                segments.append(DialogueSegment(
                    speaker=item["speaker"],
                    text=item["text"],
                    sequence=i
                ))
            
            print(f"✅ Generated {len(segments)} dialogue segments for '{topic}'")
            return segments
            
        except Exception as e:
            print(f"❌ Error generating dialogue: {e}")
            raise
    
    def _build_dialogue_prompt(
        self, 
        topic: str, 
        duration_minutes: int,
        context: Optional[str]
    ) -> str:
        """Build the prompt for dialogue generation"""
        
        # Calculate target word count (NotebookLM style: ~150 words per minute)
        target_words = duration_minutes * 150
        
        base_prompt = f"""You are creating an engaging, in-depth podcast-style educational dialogue about {topic} for VLSI engineering students, similar to NotebookLM's audio overviews.

Create a natural, flowing conversation between:
- **Zoya**: Expert VLSI instructor (warm, enthusiastic, uses clear examples, builds understanding progressively)
- **Ravi**: Curious co-host who asks insightful questions students actually wonder about, relates concepts to real-world applications

CRITICAL REQUIREMENTS:
- Target duration: {duration_minutes} minutes (approximately {target_words} words total)
- Generate AT LEAST 15-20 dialogue segments for a {duration_minutes}-minute overview
- Natural, conversational podcast tone (like NotebookLM, not a lecture)
- Cover the topic comprehensively with depth and examples
- Ravi asks clarifying questions at natural points to deepen understanding
- Use real-world analogies and practical examples throughout
- Build understanding progressively from basics to advanced concepts
- Include "aha moment" insights and practical design tips
- End with a clear summary and actionable next steps

STRUCTURE:
1. Engaging introduction (Zoya welcomes, sets context)
2. Core concept explanation with Ravi's questions
3. Deep dive into key aspects with examples
4. Practical applications and real-world scenarios
5. Common pitfalls and best practices
6. Summary and next steps

Topic: {topic}
"""
        
        if context:
            base_prompt += f"\nSpecific aspects to cover:\n{context}\n"
        
        base_prompt += """
Format your response as a JSON array of dialogue segments:
[
  {"speaker": "zoya", "text": "Welcome! Today we're diving deep into Finite State Machines..."},
  {"speaker": "ravi", "text": "I've heard FSMs are fundamental - why is that exactly?"},
  {"speaker": "zoya", "text": "Great question! FSMs are the building blocks..."},
  ...
]

DIALOGUE GUIDELINES:
- Each turn should be 2-4 sentences (conversational, not too long)
- Alternate between speakers naturally (no more than 2 consecutive turns per speaker)
- Ravi's questions should reflect real student confusion points and curiosity
- Zoya's explanations should be clear, example-driven, and build on previous points
- Use "..." for natural pauses and emphasis
- Include enthusiasm and personality (this is a podcast, not a textbook!)
- Make it engaging enough that students want to keep listening

Generate a comprehensive {duration_minutes}-minute dialogue now (aim for {target_words} words):"""
        
        return base_prompt
    
    def _parse_dialogue_response(self, response_text: str) -> List[Dict]:
        """Parse Gemini's response into dialogue segments"""
        try:
            # Try to extract JSON from response
            # Sometimes Gemini wraps JSON in markdown code blocks
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            else:
                json_text = response_text.strip()
            
            dialogue_data = json.loads(json_text)
            
            # Validate structure
            if not isinstance(dialogue_data, list):
                raise ValueError("Response is not a list")
            
            for item in dialogue_data:
                if "speaker" not in item or "text" not in item:
                    raise ValueError("Missing required fields in dialogue segment")
                if item["speaker"] not in ["zoya", "ravi"]:
                    raise ValueError(f"Invalid speaker: {item['speaker']}")
            
            return dialogue_data
            
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON response: {e}")
            print(f"Response text: {response_text[:500]}...")
            raise ValueError("Failed to parse dialogue response as JSON")
    
    async def transcribe_audio(self, audio_data: bytes) -> str:
        """
        Transcribe audio input to text using Gemini
        
        Args:
            audio_data: Audio file bytes
            
        Returns:
            Transcribed text
        """
        # Note: Gemini 2.0 supports audio input
        # For now, we'll implement a placeholder
        # Full implementation will use Gemini's multimodal capabilities
        
        prompt = "Transcribe the following audio to text:"
        
        try:
            # TODO: Implement actual audio transcription with Gemini multimodal
            # For now, return placeholder
            print("⚠️  Audio transcription not yet implemented")
            return "[Audio transcription placeholder]"
            
        except Exception as e:
            print(f"❌ Error transcribing audio: {e}")
            raise
    
    async def generate_response(
        self, 
        question: str, 
        context: str,
        topic: str = "FSM Design"
    ) -> List[DialogueSegment]:
        """
        Generate contextual response to student question
        
        Args:
            question: Student's question
            context: Previous conversation context
            topic: Current topic being discussed
            
        Returns:
            List of DialogueSegment objects (response from both Zoya and Ravi)
        """
        prompt = f"""You are continuing a teaching podcast about {topic}.

Previous conversation context:
{context}

A student has joined and asked: "{question}"

Generate a natural response as a dialogue between:
- **Ravi** (curious student): Relates to the question, shows he had similar confusion
- **Zoya** (instructor): Provides clear answer with examples

Keep it conversational and warm. 2-4 exchanges maximum.

Format as JSON array:
[
  {{"speaker": "ravi", "text": "..."}},
  {{"speaker": "zoya", "text": "..."}},
  ...
]

Generate the response now:"""
        
        try:
            response = self.model.generate_content(prompt)
            dialogue_data = self._parse_dialogue_response(response.text)
            
            # Convert to DialogueSegment objects
            segments = []
            for i, item in enumerate(dialogue_data):
                segments.append(DialogueSegment(
                    speaker=item["speaker"],
                    text=item["text"],
                    sequence=i
                ))
            
            print(f"✅ Generated {len(segments)} response segments")
            return segments
            
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            raise


# Global client instance
_client: Optional[GeminiClient] = None

def get_gemini_client() -> GeminiClient:
    """Get the global Gemini client instance"""
    global _client
    if _client is None:
        _client = GeminiClient()
    return _client
