# Implementation Plan: VLSI Audio Overview

## Overview

This implementation plan breaks down the VLSI Audio Overview feature into discrete coding tasks. The system will be built as a standalone web application with a Python/FastAPI backend and React/TypeScript frontend. The implementation follows an incremental approach, building core functionality first, then adding interactive features, and finally polishing with error handling and testing.

## Current Status

The backend core functionality is largely complete:
- ✅ Configuration management with API key validation
- ✅ Gemini API client for dialogue generation
- ✅ Coqui TTS engine with voice cloning (XTTS-v2)
- ✅ Audio processing and metadata storage
- ✅ Script generation with speaker alternation
- ✅ Audio overview generation endpoint

The frontend has basic structure but needs full implementation of audio player and interaction features.

## Tasks

- [x] 1. Set up project structure and development environment
  - Create backend directory with FastAPI project structure
  - Create frontend directory with React/TypeScript project
  - Set up Python virtual environment and install dependencies (fastapi, uvicorn, google-generativeai, TTS, pydub, python-dotenv, hypothesis)
  - Set up Node.js project and install dependencies (react, typescript, fast-check)
  - Create `.env.example` file documenting required API keys (GEMINI_API_KEY)
  - Create `.gitignore` to exclude `.env`, `node_modules`, `__pycache__`, and audio files
  - Create `voice_samples/zoya/` directory for instructor voice samples
  - Create `audio_storage/` directory for generated audio files
  - _Requirements: 13.1, 13.5, 14.3, 14.6_

- [x] 2. Implement configuration and API key management
  - [x] 2.1 Create configuration loader using python-dotenv
    - Write `config.py` to load environment variables from `.env`
    - Define Config model with all required fields (gemini_api_key, audio_storage_path, voice_samples_path, etc.)
    - _Requirements: 14.1, 14.2_
  
  - [x] 2.2 Implement API key validation on startup
    - Write validation function to check for required API keys
    - Display error message if GEMINI_API_KEY is missing
    - _Requirements: 14.4, 14.5_
  
  - [ ]* 2.3 Write unit tests for configuration loading
    - Test loading valid configuration
    - Test error handling for missing API keys
    - _Requirements: 14.4, 14.5_

- [x] 3. Implement Gemini API client
  - [x] 3.1 Create GeminiClient class
    - Initialize google-generativeai library with API key
    - Implement `generate_dialogue()` method for script generation
    - Implement `transcribe_audio()` method for voice transcription (placeholder)
    - Implement `generate_response()` method for question answering
    - Add error handling for API failures and rate limits
    - _Requirements: 1.1, 1.3, 6.1, 6.2, 9.1_
  
  - [ ]* 3.2 Write unit tests for GeminiClient
    - Test dialogue generation with mock responses
    - Test error handling for API failures
    - _Requirements: 9.1_

- [x] 4. Implement Coqui TTS integration and voice cloning
  - [x] 4.1 Create TTSEngine class
    - Initialize Coqui TTS with XTTS-v2 model
    - Implement voice cloning setup using instructor samples from `voice_samples/zoya/`
    - Configure voice cloning for Ravi using samples from `voice_samples/ravi/`
    - Implement `synthesize()` method to generate audio from text and speaker
    - Add error handling for TTS failures
    - _Requirements: 2.1, 2.2, 2.3, 2.7, 9.2_
  
  - [ ]* 4.2 Write property test for audio synthesis completeness
    - **Property 4: Audio Synthesis Completeness**
    - **Validates: Requirements 2.1**
  
  - [ ]* 4.3 Write unit tests for TTSEngine
    - Test audio generation for both speakers
    - Test error handling for TTS failures
    - _Requirements: 9.2_

- [x] 5. Implement audio processing and storage
  - [x] 5.1 Create AudioProcessor class
    - Implement audio format conversion using pydub
    - Implement audio file saving with metadata
    - Implement audio file loading and validation
    - Implement list_audio_segments method
    - _Requirements: 2.4, 2.5, 13.4, 13.8_
  
  - [ ]* 5.2 Write property test for audio metadata completeness
    - **Property 5: Audio Metadata Completeness**
    - **Validates: Requirements 2.4**
  
  - [ ]* 5.3 Write property test for audio format validity
    - **Property 6: Audio Format Validity**
    - **Validates: Requirements 2.5**
  
  - [ ]* 5.4 Write property test for audio storage format
    - **Property 7: Audio Storage Format**
    - **Validates: Requirements 13.8**
  
  - [ ]* 5.5 Write property test for audio bitrate minimum
    - **Property 26: Audio Bitrate Minimum**
    - **Validates: Requirements 12.3**

- [x] 6. Implement script generation service
  - [x] 6.1 Create ScriptGenerator class
    - Implement `generate_dialogue()` method using GeminiClient
    - Create prompt template for FSM Design educational dialogue
    - Parse Gemini response into dialogue segments with speaker assignments
    - Ensure speaker alternation validation
    - Implement dialogue structure validation
    - _Requirements: 1.1, 1.4, 1.5_
  
  - [ ]* 6.2 Write property test for script duration bounds
    - **Property 1: Script Duration Bounds**
    - **Validates: Requirements 1.2**
  
  - [ ]* 6.3 Write property test for speaker alternation
    - **Property 2: Speaker Alternation**
    - **Validates: Requirements 1.4**
  
  - [ ]* 6.4 Write property test for dialogue structure completeness
    - **Property 3: Dialogue Structure Completeness**
    - **Validates: Requirements 1.5**

- [x] 7. Implement audio overview generation endpoint
  - [x] 7.1 Create `/api/overview/generate` POST endpoint
    - Accept topic and duration parameters
    - Call ScriptGenerator to create dialogue
    - Call TTSEngine to synthesize audio for each segment
    - Call AudioProcessor to store audio files with metadata
    - Return overview_id and segment list with audio URLs
    - Add graceful fallback when TTS unavailable
    - _Requirements: 1.1, 1.2, 2.1, 2.4_
  
  - [x] 7.2 Create `/api/audio/{segment_id}` GET endpoint
    - Serve audio files from storage
    - Add appropriate headers for audio streaming
    - _Requirements: 2.5_
  
  - [x] 7.3 Create `/api/segments` GET endpoint
    - List all audio segments with optional filtering by overview_id
    - Return segment metadata
    - _Requirements: 2.4_
  
  - [ ]* 7.4 Write integration test for overview generation
    - Test end-to-end flow from request to audio files
    - _Requirements: 1.1, 2.1, 2.4_

- [x] 8. Checkpoint - Test audio overview generation
  - Backend core functionality tested with test scripts
  - Dialogue generation working ✓
  - API endpoints functional ✓
  - Frontend displaying dialogues ✓
  - Manual testing confirms dialogue generation and audio synthesis work

- [x] 9. Implement response generation service
  - [x] 9.1 Create ResponseGenerator class
    - Implement `transcribe_audio()` method using GeminiClient (complete placeholder implementation)
    - Implement `generate_response()` method with context awareness
    - Ensure responses include both Zoya and Ravi dialogue
    - Maintain conversation context from overview topic
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  
  - [ ]* 9.2 Write property test for response generation pipeline
    - **Property 16: Response Generation Pipeline**
    - **Validates: Requirements 6.1, 6.2, 6.5**
  
  - [ ]* 9.3 Write property test for dual-speaker responses
    - **Property 17: Dual-Speaker Responses**
    - **Validates: Requirements 6.3**
  
  - [ ]* 9.4 Write property test for contextual response relevance
    - **Property 18: Contextual Response Relevance**
    - **Validates: Requirements 6.4**

- [x] 10. Implement question endpoints
  - [x] 10.1 Create `/api/question/voice` POST endpoint
    - Accept audio file upload and overview context
    - Call ResponseGenerator to transcribe and generate response
    - Call TTSEngine to synthesize response audio
    - Return transcription and response segments
    - _Requirements: 6.1, 6.2, 6.5_
  
  - [x] 10.2 Create `/api/question/text` POST endpoint
    - Accept text question and overview context
    - Call ResponseGenerator to generate response
    - Call TTSEngine to synthesize response audio
    - Return response segments
    - _Requirements: 8.2, 8.3_
  
  - [ ]* 10.3 Write property test for input method equivalence
    - **Property 22: Input Method Equivalence**
    - **Validates: Requirements 8.2, 8.3**

- [ ] 11. Implement frontend audio player component
  - [ ] 11.1 Create AudioPlayer React component
    - Implement playback state management (isPlaying, currentSegmentIndex, currentTime)
    - Implement Web Audio API integration for audio playback
    - Implement play/pause controls
    - Implement progress bar with time tracking
    - Implement segment preloading for smooth transitions
    - Implement audio queue management for segment sequencing
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.6_
  
  - [ ]* 11.2 Write property test for pause-resume round trip
    - **Property 9: Pause-Resume Round Trip**
    - **Validates: Requirements 3.2, 3.3**
  
  - [ ]* 11.3 Write property test for playback completion behavior
    - **Property 10: Playback Completion Behavior**
    - **Validates: Requirements 3.6**
  
  - [ ]* 11.4 Write property test for progress display completeness
    - **Property 11: Progress Display Completeness**
    - **Validates: Requirements 3.4**
  
  - [ ]* 11.5 Write unit tests for AudioPlayer
    - Test play/pause functionality
    - Test progress tracking
    - Test segment transitions
    - _Requirements: 3.1, 3.2, 3.3, 3.6_

- [ ] 12. Implement transcript display component
  - [ ] 12.1 Create TranscriptDisplay React component
    - Display current speaker name (Zoya or Ravi)
    - Display visual indicator for each speaker (different colors/icons)
    - Display transcript text synchronized with audio
    - Update display when speaker changes
    - _Requirements: 4.1, 4.2, 4.4, 4.5_
  
  - [ ]* 12.2 Write property test for speaker information display
    - **Property 12: Speaker Information Display**
    - **Validates: Requirements 4.1, 4.2, 4.4**
  
  - [ ]* 12.3 Write property test for transcript synchronization
    - **Property 13: Transcript Synchronization**
    - **Validates: Requirements 4.5**

- [ ] 13. Implement voice input handler component
  - [ ] 13.1 Create VoiceInputHandler React component
    - Implement "Join Conversation" button
    - Request microphone access using MediaRecorder API
    - Implement audio recording state management
    - Capture audio input and send to backend
    - Handle microphone permission denial with error message
    - Show text input fallback when microphone unavailable
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 8.1_
  
  - [ ]* 13.2 Write property test for voice input capture
    - **Property 14: Voice Input Capture**
    - **Validates: Requirements 5.3, 5.4**
  
  - [ ]* 13.3 Write property test for recording state activation
    - **Property 15: Recording State Activation**
    - **Validates: Requirements 5.2**
  
  - [ ]* 13.4 Write unit tests for VoiceInputHandler
    - Test microphone permission request
    - Test recording start/stop
    - Test error handling for denied permission
    - _Requirements: 5.1, 5.5_

- [ ] 14. Implement text input handler component
  - [ ] 14.1 Create TextInputHandler React component
    - Implement text input field
    - Implement submit button
    - Send text question to backend
    - Display "Read Aloud" button for responses
    - _Requirements: 8.1, 8.2, 8.4, 8.5_
  
  - [ ]* 14.2 Write property test for text response UI elements
    - **Property 23: Text Response UI Elements**
    - **Validates: Requirements 8.4**

- [ ] 15. Implement loading states and indicators
  - [ ] 15.1 Create LoadingIndicator React component
    - Display loading spinner during audio generation
    - Display "Processing your question" message during voice processing
    - Display loading indicator during response generation
    - Display estimated wait time for operations > 2 seconds
    - Remove indicator when operation completes
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
  
  - [ ]* 15.2 Write property test for loading indicator presence
    - **Property 24: Loading Indicator Presence**
    - **Validates: Requirements 10.1, 10.2, 10.3**
  
  - [ ]* 15.3 Write property test for wait time display
    - **Property 25: Wait Time Display**
    - **Validates: Requirements 10.4**

- [ ] 16. Implement error handling and display
  - [ ] 16.1 Create ErrorDisplay React component
    - Display user-friendly error messages
    - Implement retry buttons for recoverable errors
    - Handle Gemini API failures
    - Handle TTS engine failures with text-only fallback
    - Handle network connectivity issues
    - Handle audio playback failures
    - Handle voice input errors with text fallback
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_
  
  - [ ]* 16.2 Write unit tests for error handling
    - Test error display for each error type
    - Test fallback mechanisms
    - Test retry functionality
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 17. Implement main application component
  - [ ] 17.1 Update App React component
    - Integrate AudioPlayer, TranscriptDisplay, VoiceInputHandler, TextInputHandler
    - Implement state management for audio overview and responses
    - Implement API calls to backend endpoints
    - Wire up conversation queue with audio player
    - Handle response insertion into playback queue
    - Replace basic dialogue display with full audio player
    - _Requirements: 3.1, 5.1, 6.1, 7.1, 8.1_
  
  - [ ]* 17.2 Write integration tests for main app
    - Test complete user flow: play overview → ask question → hear response
    - Test multiple questions during playback
    - _Requirements: 7.5_

- [ ] 18. Implement browser compatibility checks
  - [ ] 18.1 Add browser detection and compatibility warnings
    - Detect browser type and version
    - Display warning for unsupported browsers
    - Verify Web Audio API support
    - Verify MediaRecorder API support
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [ ] 19. Create pre-generated demo audio overview
  - [ ] 19.1 Generate FSM Design audio overview
    - Run script generation for FSM Design topic
    - Generate audio for all segments using cloned Zoya voice and Ravi voice
    - Store audio files and metadata
    - Create demo endpoint to serve pre-generated overview
    - _Requirements: 15.1, 15.2_

- [ ] 20. Implement API documentation
  - [ ] 20.1 Add FastAPI automatic documentation
    - Add docstrings to all API endpoints
    - Configure OpenAPI/Swagger UI
    - Document request/response schemas
    - Add example requests and responses

- [ ] 21. Final checkpoint - End-to-end testing
  - Test complete application flow on Chrome and Edge
  - Verify voice cloning quality with instructor samples
  - Test error handling and recovery
  - Verify all property tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at key milestones
- Property tests validate universal correctness properties using hypothesis (Python) and fast-check (TypeScript)
- Unit tests validate specific examples and edge cases
- Voice cloning requires instructor voice samples in `voice_samples/zoya/` directory
- The system uses Coqui TTS (free, unlimited) instead of ElevenLabs to avoid API credit limits
- Configuration uses `.env` file for API keys (GEMINI_API_KEY required)
- Backend core functionality is complete and tested
- Frontend needs full implementation of audio player and interaction features

