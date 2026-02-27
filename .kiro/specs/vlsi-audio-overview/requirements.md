# Requirements Document: VLSI Audio Overview

## Introduction

This document specifies the requirements for a NotebookLM-style Audio Overview feature designed for VLSI education. The system generates podcast-style educational conversations between two AI hosts (Zoya - instructor, Ravi - student) about VLSI topics, with a focus on FSM Design for the prototype. Students can listen to the overview and join the conversation by speaking their questions.

## Glossary

- **Audio_Overview_Generator**: The component responsible for creating dialogue scripts and generating audio segments
- **Playback_Controller**: The component that manages audio playback, progress tracking, and speaker transitions
- **Voice_Input_Handler**: The component that captures and processes student voice input
- **Response_Generator**: The component that generates contextual AI responses to student questions
- **Audio_Synthesizer**: The component that converts text responses to audio using Coqui TTS
- **Transcript_Display**: The UI component showing real-time text of spoken content
- **Conversation_Queue**: The audio queue that manages playback order including student interruptions
- **Gemini_Client**: The interface to Google Gemini 2.0 Flash API (using REST API)
- **TTS_Engine**: The Coqui TTS engine running locally for text-to-speech conversion
- **Voice_Model**: A trained voice model in Coqui TTS, either fine-tuned from samples or pre-trained
- **Audio_Processor**: The component that handles audio file manipulation using pydub
- **Student**: The user interacting with the audio overview
- **Zoya**: The AI instructor persona (female voice)
- **Ravi**: The AI student persona (male voice)

## Requirements

### Requirement 1: Audio Overview Script Generation

**User Story:** As a VLSI instructor, I want the system to generate educational dialogue scripts, so that students receive structured conversational content about FSM Design.

#### Acceptance Criteria

1. WHEN the Audio_Overview_Generator receives a topic request, THE Audio_Overview_Generator SHALL generate a dialogue script between Zoya and Ravi covering FSM Design concepts
2. THE Audio_Overview_Generator SHALL create scripts with a target duration of 8 to 10 minutes
3. THE Audio_Overview_Generator SHALL use the Gemini_Client to generate conversational content
4. WHEN generating dialogue, THE Audio_Overview_Generator SHALL assign speaker roles alternating between Zoya and Ravi
5. THE Audio_Overview_Generator SHALL structure the dialogue to include concept introduction, examples, and student questions

### Requirement 2: Audio Synthesis and Voice Configuration

**User Story:** As a student, I want to hear natural-sounding voices for both AI hosts, so that the learning experience feels engaging and human-like.

#### Acceptance Criteria

1. WHEN the Audio_Synthesizer receives dialogue text with speaker assignment, THE Audio_Synthesizer SHALL generate audio using the TTS_Engine
2. THE Audio_Synthesizer SHALL use a fine-tuned Voice_Model for Zoya created from instructor voice samples using Coqui TTS voice cloning
3. THE Audio_Synthesizer SHALL use a pre-trained male Voice_Model from Coqui TTS for Ravi's dialogue segments
4. WHEN audio generation completes, THE Audio_Synthesizer SHALL store audio segments with metadata including speaker, text, duration, and sequence order
5. THE Audio_Synthesizer SHALL return audio in WAV or MP3 format compatible with Web Audio API
6. THE TTS_Engine SHALL run locally on the server without requiring external API calls
7. WHEN voice cloning is required, THE system SHALL support fine-tuning Coqui TTS models using audio samples of the instructor's voice

### Requirement 3: Audio Playback Control

**User Story:** As a student, I want to control audio playback, so that I can pause, resume, and track progress through the overview.

#### Acceptance Criteria

1. WHEN a student initiates playback, THE Playback_Controller SHALL play audio segments in sequence order
2. WHEN a student clicks pause, THE Playback_Controller SHALL pause playback at the current position
3. WHEN a student clicks play after pausing, THE Playback_Controller SHALL resume playback from the paused position
4. THE Playback_Controller SHALL display a progress bar showing elapsed time and total duration
5. WHEN playback position changes, THE Playback_Controller SHALL update the progress bar within 100 milliseconds
6. WHEN all audio segments complete, THE Playback_Controller SHALL stop playback and reset to the beginning

### Requirement 4: Speaker Visualization

**User Story:** As a student, I want to see who is currently speaking, so that I can follow the conversation between Zoya and Ravi.

#### Acceptance Criteria

1. WHEN an audio segment plays, THE Transcript_Display SHALL show the current speaker's name
2. THE Transcript_Display SHALL provide a visual indicator distinguishing Zoya from Ravi
3. WHEN the speaker changes, THE Transcript_Display SHALL update the visual indicator within 200 milliseconds
4. THE Transcript_Display SHALL display the transcript text of the current audio segment
5. WHEN playback progresses, THE Transcript_Display SHALL synchronize text display with audio playback

### Requirement 5: Voice Input Capture

**User Story:** As a student, I want to ask questions by speaking, so that I can naturally join the conversation.

#### Acceptance Criteria

1. WHEN a student clicks the "Join Conversation" button, THE Voice_Input_Handler SHALL request microphone access
2. WHEN microphone access is granted, THE Voice_Input_Handler SHALL activate audio recording using the MediaRecorder API
3. WHEN a student speaks, THE Voice_Input_Handler SHALL capture audio input
4. WHEN a student finishes speaking, THE Voice_Input_Handler SHALL stop recording and send the audio to the Response_Generator
5. IF microphone access is denied, THEN THE Voice_Input_Handler SHALL display an error message and offer text input as an alternative

### Requirement 6: Question Processing and Response Generation

**User Story:** As a student, I want the AI hosts to respond to my questions, so that I can get clarification on VLSI concepts.

#### Acceptance Criteria

1. WHEN the Response_Generator receives student audio input, THE Response_Generator SHALL send it to the Gemini_Client for transcription
2. WHEN transcription completes, THE Response_Generator SHALL generate a contextual response using the Gemini_Client
3. THE Response_Generator SHALL create responses that include dialogue from both Zoya and Ravi
4. THE Response_Generator SHALL maintain conversation context from the current audio overview topic
5. WHEN response generation completes, THE Response_Generator SHALL send the response text to the Audio_Synthesizer
6. THE Response_Generator SHALL complete the entire process within 5 seconds from receiving audio input

### Requirement 7: Response Audio Integration

**User Story:** As a student, I want AI responses to play seamlessly after I ask a question, so that the conversation flow feels natural.

#### Acceptance Criteria

1. WHEN the Audio_Synthesizer generates response audio, THE Conversation_Queue SHALL insert the response segments into the playback queue
2. THE Conversation_Queue SHALL pause the current audio overview playback when inserting response audio
3. WHEN response audio completes, THE Conversation_Queue SHALL resume the original audio overview from where it was paused
4. THE Conversation_Queue SHALL maintain the correct sequence order for all audio segments
5. THE Conversation_Queue SHALL allow multiple student questions without losing playback position

### Requirement 8: Text Chat Fallback

**User Story:** As a student without microphone access, I want to type my questions, so that I can still interact with the audio overview.

#### Acceptance Criteria

1. WHEN microphone access is unavailable, THE Voice_Input_Handler SHALL display a text input field
2. WHEN a student submits a text question, THE Response_Generator SHALL process it using the Gemini_Client
3. THE Response_Generator SHALL generate responses for text input following the same process as voice input
4. THE Transcript_Display SHALL provide a "Read Aloud" button for text-based responses
5. WHEN a student clicks "Read Aloud", THE Playback_Controller SHALL play the response audio

### Requirement 9: Error Handling

**User Story:** As a student, I want clear feedback when errors occur, so that I understand what went wrong and what to do next.

#### Acceptance Criteria

1. WHEN the Gemini_Client fails to respond, THE Response_Generator SHALL display an error message indicating the service is unavailable
2. WHEN the ElevenLabs_Client fails to generate audio, THE Audio_Synthesizer SHALL display an error message and offer text-only mode
3. WHEN network connectivity is lost, THE system SHALL display an error message indicating connection issues
4. WHEN audio playback fails, THE Playback_Controller SHALL display an error message and offer to retry
5. IF an error occurs during voice input, THEN THE Voice_Input_Handler SHALL display an error message and offer text input as an alternative

### Requirement 10: Loading States

**User Story:** As a student, I want to see when the system is processing my request, so that I know the system is working.

#### Acceptance Criteria

1. WHEN audio generation is in progress, THE system SHALL display a loading indicator
2. WHEN voice input is being processed, THE system SHALL display a "Processing your question" message
3. WHEN response generation is in progress, THE system SHALL display a loading indicator
4. THE system SHALL display estimated wait times when processing takes longer than 2 seconds
5. WHEN loading completes, THE system SHALL remove the loading indicator within 200 milliseconds

### Requirement 11: Browser Compatibility

**User Story:** As a student, I want the application to work on my browser, so that I can access the feature without technical issues.

#### Acceptance Criteria

1. THE system SHALL support Google Chrome version 90 or later
2. THE system SHALL support Microsoft Edge version 90 or later
3. WHEN running on an unsupported browser, THE system SHALL display a message indicating browser requirements
4. THE system SHALL use Web Audio API for audio playback
5. THE system SHALL use MediaRecorder API for voice input capture

### Requirement 12: Audio Quality and Performance

**User Story:** As a student, I want smooth audio playback without gaps or stuttering, so that the learning experience is not disrupted.

#### Acceptance Criteria

1. WHEN transitioning between audio segments, THE Playback_Controller SHALL maintain continuous playback without gaps longer than 50 milliseconds
2. THE Playback_Controller SHALL preload the next audio segment before the current segment completes
3. WHEN audio segments are stored, THE Audio_Synthesizer SHALL use a bitrate sufficient for clear speech (minimum 64 kbps)
4. THE Playback_Controller SHALL buffer audio to prevent stuttering during playback
5. WHEN network conditions degrade, THE Playback_Controller SHALL maintain playback quality by adjusting buffer size

### Requirement 13: Technical Implementation Stack

**User Story:** As a developer, I want clear technical specifications, so that I can implement the system using the correct libraries and APIs.

#### Acceptance Criteria

1. THE backend SHALL be implemented using Python with the FastAPI framework
2. THE Gemini_Client SHALL use the google-generativeai Python library to interact with Gemini 2.0 Flash API
3. THE TTS_Engine SHALL use the Coqui TTS library (TTS Python package) for text-to-speech generation
4. THE Audio_Processor SHALL use the pydub library for audio file manipulation and format conversion
5. THE frontend SHALL be implemented using React with TypeScript
6. THE frontend SHALL use the browser's native Web Audio API for audio playback
7. THE Voice_Input_Handler SHALL use the browser's native MediaRecorder API for voice capture
8. THE system SHALL store audio files in WAV or MP3 format with metadata in JSON format
9. THE TTS_Engine SHALL run locally without requiring external API calls or credit limits

### Requirement 14: API Key Configuration

**User Story:** As a developer, I want to securely configure API keys, so that I can connect to external services without hardcoding credentials.

#### Acceptance Criteria

1. THE system SHALL read API keys from a configuration file named `.env` in the project root
2. THE `.env` file SHALL contain the Google Gemini API key with the variable name `GEMINI_API_KEY`
3. THE system SHALL provide a `.env.example` file documenting all required API keys
4. WHEN the system starts, THE backend SHALL validate that all required API keys are present
5. IF required API keys are missing, THEN THE system SHALL display an error message indicating which keys are needed
6. THE `.env` file SHALL be excluded from version control via `.gitignore`
7. THE system SHALL use the python-dotenv library to load environment variables from the `.env` file

### Requirement 15: Prototype Scope Limitations

**User Story:** As a developer, I want clear boundaries for the prototype, so that I can focus on core functionality.

#### Acceptance Criteria

1. THE Audio_Overview_Generator SHALL generate content only for the FSM Design topic
2. THE system SHALL support a single pre-generated audio overview for demonstration purposes
3. THE system SHALL NOT implement user authentication in the prototype
4. THE system SHALL NOT save conversation history in the prototype
5. THE system SHALL target desktop Chrome browsers only, without mobile optimization

