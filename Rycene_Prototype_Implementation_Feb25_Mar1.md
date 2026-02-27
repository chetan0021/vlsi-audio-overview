# Rycene AI Skills Lab — Prototype Implementation Document
### AMD Slingshot 2026 | Feb 25 → Mar 1, 2026

---

## Document Purpose

This document is the complete implementation blueprint for building the Rycene AI Skills Lab prototype by March 1, 2026. It is written for individual module-by-module development followed by final integration. Each module is self-contained and can be built and tested independently before combining.

**Build philosophy**: Each module must work correctly and look polished on its own. Integration is the last step — not the first. A clean demo of 3 working features is stronger than 6 half-built ones.

---

## What the Prototype Must Demonstrate (AMD Submission)

The Mar 1 prototype is not the full app. It must demonstrate the **core learning loop** convincingly using **one topic only** — FSM Design (Finite State Machine). Every feature is built around this single topic so the demo feels complete and intentional, not scattered.

**The prototype must show:**

1. Student login → topic locked until instructor unlocks it (after Zoom class)
2. Instructor unlocks FSM topic → student dashboard updates in real-time
3. Student opens Circuit Whiteboard → uses hand gesture to point at a circuit component → AI explains it with voice
4. Student clicks "Audio Overview" → NotebookLM-style two-voice conversation plays (Zoya + Ravi discussing FSM concepts)
5. Student clicks "Join Conversation" → speaks their question → AI hosts respond naturally in real-time
6. Student attempts a Verilog practice task → gets stuck → uses progressive hints → submits code → receives rubric feedback
7. Skill Competency for FSM updates on the student's dashboard after task completion

**These 7 moments are the demo.** Everything else is supporting infrastructure.

---

## Architecture Overview

```
Frontend (React)
│
├── Student Dashboard
├── Circuit Whiteboard (MediaPipe)
├── Concept Conversation Player
├── Code Practice Editor
├── Rubric Feedback View
└── Skill Map / Job Readiness Panel

Backend (Python FastAPI)
│
├── Auth API (login, session)
├── Topic Lock/Unlock API
├── LLM Conversation API (hint engine + dialogue generator)
├── Rubric Engine API
├── TTS API (voice synthesis)
└── Mastery/Competency Tracker API

External Services
├── LLM: Google Gemini 2.0 Flash (dialogue generation, Q&A, hints, rubric)
├── TTS: ElevenLabs API (prototype) — two voice profiles (Zoya + Ravi)
├── Voice Input: Gemini 2.0 Flash multimodal API (student voice questions)
└── MediaPipe: Google MediaPipe Gesture Recognizer (browser JS, no server)
```

**Why ElevenLabs for prototype TTS**: ElevenLabs has a free tier, extremely fast latency, and you can create two distinct voice profiles (Zoya Instructor + Ravi Student) in minutes. Can also clone real instructor voice. Coqui XTTS-v2 is better for production (local, private, free) but takes time to fine-tune. Use ElevenLabs for Mar 1 prototype, migrate to Coqui later.

**Why Gemini 2.0 Flash**: Single well-prompted LLM handles dialogue generation, student question responses, hint generation, and rubric scoring. Gemini 2.0 Flash has native multimodal capabilities including voice input/output, making it perfect for the "Join Conversation" feature. Fast enough for real-time interaction (~1-2 second response time).

---

## Module Breakdown

There are **7 modules** to build independently and then integrate.

---

## MODULE 1 — Authentication & Topic Gate

### What it does
Simple login system. Student account. Instructor account. Instructor can mark a topic as "taught in live class." Only after that does the topic unlock in the student's dashboard. Before unlock, the topic shows as locked with the message: *"This topic unlocks after your live class session."*

### Why it matters for AMD demo
This is the first thing judges see. It immediately communicates: *"This is not a generic AI chatbot. This is tightly integrated with real classroom delivery."* It must work cleanly.

### Data model

```
User {
  id
  email
  password_hash
  role: "student" | "instructor"
  enrolled_topics: [topic_id]   // for student
}

Topic {
  id
  name: "FSM Design"
  is_unlocked: boolean          // instructor sets this to true
  unlocked_at: timestamp
}

StudentTopicAccess {
  student_id
  topic_id
  unlocked: boolean             // derives from Topic.is_unlocked + enrollment
  mastery_level: "locked" | "beginner" | "intermediate" | "job-ready"
  competency_score: 0-100
}
```

### Build steps

**Step 1.1 — Backend**
- FastAPI app with `/auth/login`, `/auth/logout` endpoints
- JWT token stored in httpOnly cookie
- `/instructor/unlock-topic` endpoint — sets `Topic.is_unlocked = true`
- `/student/dashboard` endpoint — returns topics list with lock status for the logged-in student
- Use SQLite for prototype (no setup required, swap to PostgreSQL later)

**Step 1.2 — Frontend: Login Page**
- Clean two-field form: email + password
- On submit: POST to `/auth/login`, store JWT, redirect to dashboard
- Two buttons for quick demo: "Login as Student" / "Login as Instructor" (pre-fills demo credentials)
- No registration flow needed for prototype — seed demo accounts in DB

**Step 1.3 — Frontend: Student Dashboard**
- Shows one topic card: "FSM Design"
- Locked state: grey card, lock icon, message: *"Unlocks after live class"*
- Unlocked state: coloured card, "Start Learning" button
- Skill competency badge updates here after practice

**Step 1.4 — Frontend: Instructor Panel**
- Single page (not the focus of the demo)
- Shows current batch info and enrolled students
- Topic list with status: "FSM Design — [Mark as Taught]" button
- On click: calls `/instructor/unlock-topic`, shows confirmation
- For demo: instructor unlocks → student dashboard refreshes (poll every 5 seconds or use WebSocket)
- Displays student progress overview (how many completed practice, average competency)

### Acceptance criteria
- Student cannot access FSM content before instructor unlocks
- After instructor unlocks, student dashboard shows the topic as active within 5 seconds
- JWT auth works across page refreshes
- Demo credentials work reliably

---

## MODULE 2 — MediaPipe Circuit Whiteboard

### What it does
Student opens an interactive FSM circuit diagram in the browser. Their webcam is activated. Google MediaPipe Gesture Recognizer tracks their hand. When the student **points at a component** (a state, a transition arrow, a flip-flop), the AI explains that specific component with text + voice.

This is the single most visually impressive feature of the prototype. It must be smooth and reliable.

### Why MediaPipe here specifically
Circuit diagrams are inherently spatial. Students naturally point at things they don't understand — exactly like they would on a physical whiteboard with an instructor. A mouse click is functionally similar but feels passive and cold. Hand gesture pointing feels like the instructor is actually *there*. This is the right use of MediaPipe: it replaces a physical, natural human interaction that mouse/keyboard cannot replicate with the same feeling.

### Technical approach

**MediaPipe in browser (JavaScript)**
- Use `@mediapipe/tasks-vision` npm package — runs entirely in browser via WebAssembly
- No server call for gesture detection — everything is client-side
- Low latency (~30ms) on standard laptop webcam

**Gesture mapping**
- **Index finger pointing (1 finger extended)** → pointing gesture detected → check which circuit hotspot the finger is pointing at → trigger explanation
- Do not use complex multi-finger gestures — pointing is universal and obvious to any student

**Circuit diagram approach**
- Build the FSM circuit as an **SVG** (not a raster image)
- SVG allows you to define clickable/hoverable regions precisely
- Each component in the SVG has an ID: `state-S0`, `state-S1`, `transition-S0-S1`, `flipflop-D`, `output-Z`
- Overlay a transparent canvas over the SVG where MediaPipe draws the hand skeleton
- Calculate pointing direction from index fingertip + MCP joint → project a ray → detect which SVG element it intersects

**Hotspot zones for FSM prototype**
Define 6 zones on the FSM diagram (a simple 2-state Moore FSM is enough for demo):
1. State S0 (idle state)
2. State S1 (active state)
3. Transition arrow S0→S1 (input = 1)
4. Transition arrow S1→S0 (input = 0)
5. D flip-flop symbol
6. Output Z

Each zone has a pre-written explanation stored in the frontend (no LLM call needed for this — latency must be near-zero):

```javascript
const explanations = {
  "state-S0": "This is State S0 — the idle state. The machine starts here and stays here when the input is 0. Output Z is 0 in this state.",
  "state-S1": "This is State S1 — the active state. The machine moves here when input becomes 1. Output Z is 1 in this state.",
  "transition-S0-S1": "This arrow shows the transition from S0 to S1. It fires when the input signal X equals 1.",
  "transition-S1-S0": "This arrow shows the transition from S1 back to S0. It fires when the input signal X equals 0.",
  "flipflop-D": "This is the D flip-flop. It stores the current state of the FSM. Its output Q holds either S0 or S1 until the next clock edge.",
  "output-Z": "This is the output logic. In a Moore machine, output depends only on the current state — not the input. Z is 1 only in S1."
}
```

When a zone is triggered by gesture pointing, the explanation text appears AND the TTS voice reads it aloud (ElevenLabs API call with instructor voice profile).

### Build steps

**Step 2.1 — MediaPipe setup**
```javascript
// Install
npm install @mediapipe/tasks-vision

// Initialize in component
import { GestureRecognizer, FilesetResolver } from "@mediapipe/tasks-vision";

const gestureRecognizer = await GestureRecognizer.createFromOptions(vision, {
  baseOptions: {
    modelAssetPath: "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task",
    delegate: "GPU"
  },
  runningMode: "VIDEO",
  numHands: 1
});
```

**Step 2.2 — SVG circuit diagram**
- Design the FSM circuit as SVG in Figma or draw.io, export as SVG
- Keep it clean and large — nodes clearly labelled S0, S1, transitions labelled with conditions
- Make it look like a professional textbook diagram, not a hand-drawn sketch
- Each element gets an `id` attribute matching the hotspot keys above

**Step 2.3 — Pointing detection**
```javascript
// In animation frame loop:
const results = gestureRecognizer.recognizeForVideo(videoElement, timestamp);

if (results.landmarks && results.landmarks[0]) {
  const landmarks = results.landmarks[0];
  const indexTip = landmarks[8];    // INDEX_FINGER_TIP
  const indexMCP = landmarks[5];    // INDEX_FINGER_MCP
  
  // Project pointing direction onto SVG canvas
  const pointX = indexTip.x * canvasWidth;
  const pointY = indexTip.y * canvasHeight;
  
  // Check which SVG zone contains this point
  const hitElement = document.elementFromPoint(pointX, pointY);
  if (hitElement && hitElement.id in explanations) {
    triggerExplanation(hitElement.id);  // debounce: 1.5 second dwell before triggering
  }
}
```

**Step 2.4 — Explanation trigger with voice**
- Dwell time: student must point at a zone for **1.5 seconds** before triggering (prevents accidental triggers)
- Visual feedback: zone highlights in yellow when pointed at, turns green when dwell completes and explanation triggers
- Text explanation appears in a side panel
- TTS call plays explanation in instructor voice
- While audio plays, highlight the active zone with a pulsing border

**Step 2.5 — Webcam permissions UX**
- Show a clear "Enable Camera" screen before opening the whiteboard
- Explain in one line why: *"Your camera lets you point at the circuit to explore it naturally"*
- If permission denied, fall back to click-to-explain mode (student clicks zone → same explanation triggers)
- This fallback is important — not every demo environment will have working webcam

### Acceptance criteria
- Pointing at each of the 6 zones triggers the correct explanation
- Dwell detection prevents accidental triggers
- Voice plays within 2 seconds of zone activation
- Fallback click mode works identically
- No camera permission = graceful fallback, not a broken page
- Works on Chrome (demo browser)

---

## MODULE 3 — NotebookLM-Style Audio Overview with "Join Conversation"

### What it does
Student opens the FSM topic and has three modes of interaction:

**Mode 1: Text Chat (Default)**
- Student types questions to Gemini AI
- Gemini responds in text format
- Fast, searchable, can copy code snippets
- Optional "Read Aloud" button to hear any response

**Mode 2: Audio Overview (NotebookLM-Style)**
- Student clicks **"Generate Audio Overview"** button
- System generates a natural podcast-style conversation between two AI hosts:
  - **Host 1 (Zoya - Instructor)**: Expert VLSI instructor, warm and clear
  - **Host 2 (Ravi - Curious Student)**: Engineering student who asks the questions real students wonder about
- Covers all key FSM concepts through engaging dialogue
- 8-10 minute overview with natural back-and-forth
- Play button to listen to the full conversation

**Mode 3: Join Conversation (The Innovation!)**
- While audio overview is playing (or after completion)
- Student clicks **"Join Conversation"** button
- Microphone activates - student can speak their question
- **The two AI hosts respond to the student's question in real-time**
- Student becomes the third participant in the conversation
- Can ask follow-up questions, interrupt, or let conversation continue
- Maintains the natural podcast feel with student as active participant

### Why this approach
- **NotebookLM familiarity**: Judges recognize the proven format, but applied to VLSI education
- **Novel innovation**: "Join Conversation" doesn't exist in NotebookLM - this is unique
- **Removes learning anxiety**: Students too shy to ask in Zoom class can ask AI hosts
- **Engaging format**: Two-voice dialogue is more engaging than single-voice lecture
- **Scalable**: Works for any topic by feeding curriculum content to Gemini

### Three interaction modes explained

**Text Chat Mode** - For quick questions and code snippets:
```
Student: "What's the difference between Moore and Mealy?"
Gemini: "In a Moore FSM, output depends only on current state..."
[Read Aloud button available]
```

**Audio Overview Mode** - For comprehensive topic learning:
```
🎙️ Zoya: "Today we're exploring Finite State Machines"
🎙️ Ravi: "I've heard FSMs are fundamental - why is that?"
🎙️ Zoya: "Great question! FSMs are the building blocks..."
[8-10 minute natural conversation covering all concepts]
```

**Join Conversation Mode** - For interactive learning:
```
[Audio overview playing...]
🎙️ Zoya: "...and that's how state transitions work"

[Student clicks "Join Conversation" and speaks]
🎤 Student: "Wait, what if input changes between clock edges?"

🎙️ Ravi: "Oh good question! I was wondering that too"
🎙️ Zoya: "Excellent question! This is about setup and hold time..."
[Conversation continues with student as participant]
```

### Audio Overview generation approach

**For prototype (Mar 1 demo):**
Pre-generate one complete audio overview for FSM Design topic to ensure smooth playback during demo. This removes generation latency and ensures reliability.

**For production (Phase 2):**
Generate audio overviews on-demand based on:
- Topic curriculum content
- Student's competency level
- Previously asked questions
- Learning pace and preferences

### Dialogue script format

Each audio overview has a structured script generated by Gemini:

```json
{
  "topic": "FSM Design",
  "duration_minutes": 8,
  "segments": [
    {
      "speaker": "zoya",
      "text": "Welcome! Today we're diving into Finite State Machines - one of the most fundamental concepts in digital design.",
      "audio_url": "/audio/fsm/overview-01-zoya.mp3",
      "timestamp": 0
    },
    {
      "speaker": "ravi",
      "text": "I've heard FSMs are everywhere in digital circuits. What makes them so important?",
      "audio_url": "/audio/fsm/overview-02-ravi.mp3",
      "timestamp": 6.2
    },
    {
      "speaker": "zoya",
      "text": "Great question! FSMs are the backbone of sequential logic. Think of them as the brain that remembers and makes decisions...",
      "audio_url": "/audio/fsm/overview-03-zoya.mp3",
      "timestamp": 10.5
    }
  ]
}
```

**How to generate the audio overview:**

1. **Generate dialogue script using Gemini:**
```python
prompt = f"""You are creating a podcast-style teaching dialogue about {topic_name} for VLSI students.

Create a natural conversation between:
- Zoya: Expert VLSI instructor (warm, clear, uses examples)
- Ravi: Curious engineering student (asks questions students actually wonder about)

Topic content to cover:
{topic_curriculum_content}

Requirements:
- 8-10 minutes total duration
- Natural, conversational tone (like NotebookLM)
- Cover all key concepts with examples
- Ravi asks clarifying questions at natural points
- Use real-world analogies (traffic lights, vending machines, etc.)
- Build from basics to advanced concepts
- End with a summary and transition to practice

Format as JSON array:
[
  {{"speaker": "zoya", "text": "..."}},
  {{"speaker": "ravi", "text": "..."}},
  ...
]
"""

script = gemini.generate_content(prompt)
```

2. **Generate audio using ElevenLabs with two distinct voices:**
   - **Zoya voice**: Female, warm instructor tone (clone from real instructor or use ElevenLabs "Rachel")
   - **Ravi voice**: Male, curious student tone (ElevenLabs "Josh" or similar)

3. **Store audio segments** in `/public/audio/{topic_id}/` with metadata

### "Join Conversation" implementation

When student clicks "Join Conversation" button:

**Step 1: Initialize Gemini Live session**
```javascript
const liveSession = await gemini.startLiveSession({
  model: "gemini-2.0-flash-exp",
  systemInstruction: `You are continuing a teaching conversation about FSM Design.

Context: You (Zoya, VLSI instructor) and Ravi (curious student) have been discussing FSMs in a podcast format.
A real student is now joining the conversation with their question.

Previous conversation summary:
${conversationHistory}

Current topic being discussed: ${currentSegmentTopic}

When the student asks a question:
1. Acknowledge their question warmly (as Zoya)
2. Have Ravi respond if the question relates to his previous confusion
3. Provide a clear, example-based answer (as Zoya)
4. Check understanding with a follow-up question
5. Maintain the warm, conversational podcast tone

Use two distinct speaking styles:
- Zoya: Instructor voice, clear explanations, uses analogies
- Ravi: Student voice, relates to the new student's confusion

Generate responses as dialogue between both voices when appropriate.`,
  
  voiceConfig: {
    voices: {
      zoya: "female-instructor-warm",
      ravi: "male-student-curious"
    }
  }
});
```

**Step 2: Enable microphone and capture student question**
```javascript
const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
const mediaRecorder = new MediaRecorder(stream);

// Visual feedback: show "Listening..." indicator
showListeningIndicator();

mediaRecorder.ondataavailable = async (event) => {
  const audioBlob = event.data;
  
  // Send to Gemini Live API
  const response = await liveSession.sendAudio(audioBlob);
  
  // Response contains dialogue between Zoya and Ravi addressing the question
  playDialogueResponse(response);
};
```

**Step 3: Play AI hosts' response**
```javascript
const playDialogueResponse = (response) => {
  // Response format:
  // [
  //   { speaker: "ravi", text: "Oh that's a good question!", audio: <blob> },
  //   { speaker: "zoya", text: "Let me explain...", audio: <blob> }
  // ]
  
  response.segments.forEach((segment, index) => {
    setTimeout(() => {
      updateSpeakerUI(segment.speaker);
      showTranscript(segment.text);
      playAudio(segment.audio);
    }, segment.delay);
  });
  
  // After response, keep mic active for follow-up questions
  enableFollowUpMode();
};
```

**Example conversation flow:**
```
[Audio overview playing...]
🎙️ Zoya: "...and that's how state transitions work on clock edges"
🎙️ Ravi: "So the FSM only looks at inputs at specific moments?"

[Student clicks "Join Conversation" and speaks]
🎤 Student: "What if the input changes right at the clock edge?"

[Gemini generates multi-voice response]
🎙️ Ravi: "Oh! I was actually wondering the same thing"
🎙️ Zoya: "Excellent question - this is about setup and hold time. The input must be stable for a small window around the clock edge..."
🎙️ Zoya: "Think of it like taking a photograph - if your subject moves during the exposure, the photo is blurry. Same with FSMs."
🎙️ Ravi: "So there's a 'safe window' where the input can't change?"
🎙️ Zoya: "Exactly! That's the setup time before the clock edge and hold time after. Does that make sense?"

[Student can respond or let conversation continue]
```

### Build steps

**Step 3.1 — Pre-generate audio overview for FSM Design (do this first)**
- Use Gemini to generate 8-10 minute dialogue script covering all FSM concepts
- Generate audio via ElevenLabs API with two distinct voices (Zoya + Ravi)
- Store MP3 files in `/public/audio/fsm/overview/`
- Build JSON manifest with timestamps and speaker info

**Step 3.2 — Audio Overview Player UI**
```jsx
<div className="audio-overview-container">
  {/* Mode selector */}
  <div className="interaction-modes">
    <button className={mode === 'text' ? 'active' : ''}>💬 Text Chat</button>
    <button className={mode === 'audio' ? 'active' : ''}>🎙️ Audio Overview</button>
  </div>

  {/* Audio Overview Mode */}
  {mode === 'audio' && (
    <div className="audio-player">
      <h3>🎙️ FSM Design - Audio Overview</h3>
      <p>Listen to Zoya and Ravi discuss the key concepts</p>
      
      {/* Player controls */}
      <div className="player-controls">
        <button onClick={togglePlay}>
          {isPlaying ? '⏸️ Pause' : '▶️ Play'}
        </button>
        <progress value={currentTime} max={totalDuration} />
        <span>{formatTime(currentTime)} / {formatTime(totalDuration)}</span>
      </div>
      
      {/* Current speaker display */}
      <div className="current-speaker">
        <div className={`avatar ${currentSpeaker}`}>
          {currentSpeaker === 'zoya' ? '👩‍🏫' : '👨‍🎓'}
        </div>
        <div className="speaker-info">
          <strong>{currentSpeaker === 'zoya' ? 'Zoya' : 'Ravi'}</strong>
          <p className="transcript">{currentText}</p>
        </div>
      </div>
      
      {/* Join Conversation button */}
      <button 
        className="join-conversation-btn"
        onClick={enableJoinMode}
        disabled={!isPlaying && currentTime === 0}
      >
        🎤 Join Conversation
        <span className="hint">Ask Zoya & Ravi your questions</span>
      </button>
      
      {/* Microphone active state */}
      {micActive && (
        <div className="mic-active">
          <div className="listening-indicator">
            <span className="pulse"></span>
            Listening...
          </div>
          <button onClick={stopListening}>Stop</button>
        </div>
      )}
    </div>
  )}
  
  {/* Text Chat Mode */}
  {mode === 'text' && (
    <div className="text-chat">
      <div className="messages">
        {messages.map(msg => (
          <div className={`message ${msg.role}`}>
            <p>{msg.content}</p>
            {msg.role === 'assistant' && (
              <button onClick={() => readAloud(msg.content)}>
                🔊 Read Aloud
              </button>
            )}
          </div>
        ))}
      </div>
      <div className="input-area">
        <input 
          type="text" 
          placeholder="Ask about FSM Design..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  )}
</div>
```

**Step 3.3 — Audio queue player with speaker tracking**
```javascript
class AudioOverviewPlayer {
  constructor(segments) {
    this.segments = segments;
    this.currentIndex = 0;
    this.audio = new Audio();
    this.onSpeakerChange = null;
    this.onTranscriptUpdate = null;
  }
  
  playNext() {
    if (this.currentIndex >= this.segments.length) {
      this.onComplete?.();
      return;
    }
    
    const segment = this.segments[this.currentIndex];
    
    // Update UI
    this.onSpeakerChange?.(segment.speaker);
    this.onTranscriptUpdate?.(segment.text);
    
    // Play audio
    this.audio.src = segment.audio_url;
    this.audio.play();
    
    this.audio.onended = () => {
      this.currentIndex++;
      this.playNext();
    };
  }
  
  pause() { 
    this.audio.pause(); 
  }
  
  resume() {
    this.audio.play();
  }
  
  // Insert student question response segments
  insertConversationSegments(newSegments) {
    // Pause current playback
    this.pause();
    
    // Insert new segments after current position
    this.segments.splice(this.currentIndex + 1, 0, ...newSegments);
    
    // Continue with inserted segments
    this.currentIndex++;
    this.playNext();
  }
  
  getCurrentContext() {
    // Return last 3 segments for context
    const start = Math.max(0, this.currentIndex - 3);
    return this.segments.slice(start, this.currentIndex + 1);
  }
}
```

**Step 3.4 — Join Conversation backend endpoint**
```python
# FastAPI endpoint
@app.post("/conversation/join")
async def join_conversation(request: JoinConversationRequest):
    """
    Handle student joining the audio overview conversation
    """
    # Get conversation context
    context = request.conversation_history
    student_audio = request.audio_data
    
    # Transcribe student question (if audio)
    if student_audio:
        student_question = await transcribe_audio(student_audio)
    else:
        student_question = request.text_question
    
    # Generate multi-voice response using Gemini
    prompt = f"""You are continuing a teaching podcast about FSM Design.

Previous conversation:
{format_conversation_history(context)}

A student has joined and asked: "{student_question}"

Generate a natural response as a dialogue between:
- Ravi (curious student): Relates to the question, shows he had similar confusion
- Zoya (instructor): Provides clear answer with examples

Keep it conversational and warm. 2-4 exchanges maximum.

Format as JSON:
[
  {{"speaker": "ravi", "text": "..."}},
  {{"speaker": "zoya", "text": "..."}},
  ...
]
"""
    
    # Get response from Gemini
    response = await gemini.generate_content(prompt)
    dialogue_segments = json.loads(response.text)
    
    # Generate audio for each segment
    audio_segments = []
    for segment in dialogue_segments:
        voice_id = VOICE_MAP[segment["speaker"]]  # zoya or ravi
        audio_url = await generate_speech(
            text=segment["text"],
            voice_id=voice_id
        )
        audio_segments.append({
            "speaker": segment["speaker"],
            "text": segment["text"],
            "audio_url": audio_url
        })
    
    return {
        "segments": audio_segments,
        "student_question": student_question
    }
```

**Step 3.5 — Microphone handling and voice input**
```javascript
const enableJoinMode = async () => {
  try {
    // Request microphone permission
    const stream = await navigator.mediaDevices.getUserMedia({ 
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        sampleRate: 44100
      } 
    });
    
    setMicActive(true);
    
    // Create media recorder
    const mediaRecorder = new MediaRecorder(stream, {
      mimeType: 'audio/webm'
    });
    
    const audioChunks = [];
    
    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };
    
    mediaRecorder.onstop = async () => {
      // Create audio blob
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
      
      // Show processing indicator
      setProcessing(true);
      
      // Send to backend
      const formData = new FormData();
      formData.append('audio_data', audioBlob);
      formData.append('conversation_history', JSON.stringify(
        audioPlayer.getCurrentContext()
      ));
      
      const response = await fetch('/conversation/join', {
        method: 'POST',
        body: formData
      });
      
      const result = await response.json();
      
      // Insert response segments into audio player
      audioPlayer.insertConversationSegments(result.segments);
      
      setProcessing(false);
      setMicActive(false);
    };
    
    // Start recording
    mediaRecorder.start();
    
    // Auto-stop after 10 seconds or manual stop
    setTimeout(() => {
      if (mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
      }
    }, 10000);
    
  } catch (error) {
    console.error('Microphone access denied:', error);
    // Fallback to text input
    showTextInputFallback();
  }
};
```

### Acceptance criteria
- Audio overview plays smoothly with clear speaker transitions
- Current speaker and transcript display updates in real-time
- "Join Conversation" button activates microphone successfully
- Student's spoken question is transcribed and processed
- AI hosts (Zoya & Ravi) respond naturally to student's question
- Response audio plays seamlessly, maintaining conversation flow
- Student can ask multiple follow-up questions
- Fallback to text input if microphone unavailable
- Full transcript available for review
- Works on Chrome and Edge browsers

---

## MODULE 4 — Verilog Practice Task with Progressive Hints

### What it does
Student is given a Verilog coding task related to FSM Design. They write code in an in-browser code editor. If stuck, they can request hints — but hints are released progressively (3 levels), never the full answer directly. After submission, the rubric engine scores their code.

### Practice task for prototype

```
Task: Write a Verilog module for a 2-state Moore FSM.
- States: S0 (idle), S1 (active)
- Input: X (1-bit)
- Output: Z (1-bit), Z=1 only in S1
- Synchronous reset (active high)
- Next state logic: if X=1, go to S1; if X=0, go to S0
```

This task is directly linked to what the student just explored in the Circuit Whiteboard — same FSM, now they implement it. This coherence matters for the demo narrative.

### Three-level hint system

Hints are not pre-written. They are LLM-generated based on what the student has written so far (or a blank if they haven't started).

**Level 1 — Conceptual hint** (after first "I'm stuck" click):
```
Prompt to LLM:
"A student is trying to write a Verilog module for a 2-state Moore FSM (S0, S1, input X, output Z).
Their current code is: [student_code_so_far]
Give them a conceptual hint — remind them of the structure they need (module declaration, state register, next state logic, output logic) without writing any code. 2-3 sentences maximum."
```

**Level 2 — Directional hint** (after second click):
```
Prompt to LLM:
"Same student, same task. They've now read the conceptual hint but are still stuck.
Their current code is: [student_code_so_far]
Give them a directional hint — point them at the specific part that is missing or wrong. You can mention the Verilog construct they need (always block, case statement, etc.) but do not write the code for them. 2-3 sentences."
```

**Level 3 — Specific hint** (after third click):
```
Prompt to LLM:
"Same student, same task. They need more help.
Their current code is: [student_code_so_far]
Give them a specific hint — show them the skeleton/template with blanks for the critical parts. Fill in non-critical parts but leave the logic they need to figure out as comments like // your logic here."
```

**Important**: After Level 3, the student has all the structural help they need. If they still can't solve it, the rubric feedback after submission will show them exactly what was wrong. Full solution is never given.

### Code editor

Use **Monaco Editor** (the VS Code editor, available as a React component):
```
npm install @monaco-editor/react
```
- Set language to `verilog` (or `plaintext` if Verilog syntax highlighting is unavailable in Monaco)
- Dark theme
- Set a starting template:
```verilog
module fsm_moore (
    input clk,
    input reset,
    input X,
    output reg Z
);

// State declaration
// Your code here

endmodule
```

### Build steps

**Step 4.1 — Code editor component**
- Monaco Editor with Verilog/plaintext syntax
- "Run" button (for prototype: just shows a "Simulation coming in Phase 2" message — do not block on building a Verilog simulator for Mar 1)
- "I'm Stuck" button with a counter showing current hint level (1/3, 2/3, 3/3)
- "Submit for Feedback" button

**Step 4.2 — Hint endpoint**
```
POST /practice/hint
{
  "task_id": "fsm-moore-2state",
  "student_code": "...",
  "hint_level": 1 | 2 | 3
}
→ returns { "hint_text": "..." }
```

**Step 4.3 — Hint display**
- Hint appears in a panel below the editor (not a modal — student should see code + hint simultaneously)
- Each hint level shows a different colour label: Level 1 (blue), Level 2 (amber), Level 3 (orange)
- Previous hints stay visible — student sees the full progression

**Step 4.4 — Submission**
```
POST /practice/submit
{
  "task_id": "fsm-moore-2state",
  "student_code": "..."
}
→ returns rubric_result (see Module 5)
```

### Acceptance criteria
- Monaco editor loads and is editable
- Three hint levels deliver progressively more specific help
- Hints are responsive to what the student has actually written (LLM reads their code)
- Submit button sends code to rubric engine
- Hint counter is visible and accurate

---

## MODULE 5 — Rubric Engine & Feedback View

### What it does
When the student submits their Verilog code, the rubric engine scores it on 4 criteria and returns specific, actionable feedback per criterion. Not a grade — a learning feedback report.

### Rubric criteria for FSM task

| Criterion | What is checked | Max score |
|---|---|---|
| Correctness | Is the next state logic correct? Does output Z match the spec? | 40 |
| Code Style | Are non-blocking assignments used in sequential blocks? Is reset handled correctly? Are state names used (not magic numbers)? | 25 |
| Structural Completeness | Is there a state register? Separate next state logic? Separate output logic? | 25 |
| Clarity | Are signals named clearly? Is the code readable without comments? | 10 |

### LLM rubric prompt

```
You are a VLSI instructor grading a student's Verilog code submission for a 2-state Moore FSM.

Task specification:
- Module: fsm_moore with inputs clk, reset (sync active-high), X; output Z
- States: S0 (idle, Z=0), S1 (active, Z=1)
- Transitions: X=1 → go to S1, X=0 → go to S0 (from any state)

Student's code:
[student_code]

Score this on exactly these 4 criteria. For each:
- Give a score out of the maximum
- Write 1-2 sentences of specific feedback mentioning the exact line or construct that is good or needs improvement
- If something is missing entirely, say what is missing

Return as JSON:
{
  "criteria": [
    {"name": "Correctness", "score": X, "max": 40, "feedback": "..."},
    {"name": "Code Style", "score": X, "max": 25, "feedback": "..."},
    {"name": "Structural Completeness", "score": X, "max": 25, "feedback": "..."},
    {"name": "Clarity", "score": X, "max": 10, "feedback": "..."}
  ],
  "total": X,
  "summary": "One sentence overall assessment",
  "top_improvement": "The single most important thing to fix"
}
```

### Feedback UI

- Score breakdown as a horizontal bar chart per criterion (use a simple CSS bar, not a charting library)
- Each criterion shows: name, score/max, feedback text
- Total score shown prominently at top
- "Top improvement" highlighted in an amber callout box
- "Try Again" button resets the editor (keeps hints visible)

### Build steps

**Step 5.1 — Rubric endpoint**
- FastAPI `/practice/submit` calls LLM with the prompt above
- Parse JSON response
- Store submission + result in DB (for mastery tracking in Module 6)
- Return rubric result to frontend

**Step 5.2 — Feedback view component**
- Slide in from the right (or replace the hint panel below editor)
- Score bars animate in from 0 on load
- Colour coding: 80%+ = green, 60-79% = amber, below 60% = red
- "Try Again" clears code and resets (or student can keep their code and edit)

### Acceptance criteria
- LLM returns valid JSON rubric (add error handling for malformed responses)
- All 4 criteria shown with specific feedback
- Score visually clear at a glance
- Feedback references the student's actual code, not generic advice
- "Try Again" works correctly

---

## MODULE 6 — Skill Map & Competency Tracker

### What it does
After a student completes a practice task and gets rubric feedback, their competency for that skill updates. The dashboard shows a visual skill map. For the prototype this covers only the FSM topic.

### Competency levels

```
Locked        → topic not yet unlocked by instructor
Beginner      → topic unlocked, no practice submitted yet
Intermediate  → submitted at least once, total rubric score 40-69%
Job-Ready     → total rubric score 70%+ on latest submission
```

### Skill map display (prototype: one topic)

- A card showing "FSM Design" with a badge: Locked / Beginner / Intermediate / Job-Ready
- A thin progress bar showing the numeric competency score (0-100)
- Last updated timestamp
- Below the card: "Job Role: [dropdown — RTL Design / Verification / Physical Design]"
- For prototype: whichever role is selected, just show "FSM Design is relevant to this role" — full role mapping comes in Phase 2

### Build steps

**Step 6.1 — Mastery update on submission**
- After rubric result is stored, calculate competency:
  ```python
  def calculate_competency(rubric_score_percent):
      if rubric_score_percent >= 70: return "job-ready", rubric_score_percent
      if rubric_score_percent >= 40: return "intermediate", rubric_score_percent
      return "beginner", rubric_score_percent
  ```
- Update `StudentTopicAccess.mastery_level` and `competency_score`

**Step 6.2 — Skill map component**
- Fetch competency from `/student/dashboard` on load
- Badge colour: grey (locked), blue (beginner), amber (intermediate), green (job-ready)
- Score bar animates to current value on load
- Auto-refreshes after rubric feedback is received (can use a context update, not a polling call)

### Acceptance criteria
- Competency updates immediately after rubric feedback
- Badge and score correct for each level
- Dashboard skill map reflects latest submission without page reload

---

## MODULE 7 — App Shell & Navigation

### What it does
Ties all modules together into a single cohesive web app. This is the last thing to build.

### Pages / routes

```
/login                    → Login page (Module 1)
/dashboard                → Student dashboard + skill map (Modules 1, 6)
/instructor               → Instructor unlock panel (Module 1)
/topic/fsm                → FSM topic page (hub for all learning modes)
/topic/fsm/whiteboard     → Circuit Whiteboard (Module 2)
/topic/fsm/practice       → Verilog Practice + Hints + Rubric (Modules 4, 5)
```

Note: Audio Overview and Text Chat are embedded in the topic page, not separate routes.

### Topic page layout (the hub)

The FSM topic page (`/topic/fsm`) is the central screen. It shows:

**Left panel — Contents**
```
FSM Design
──────────────────
💬 Text Chat with AI
   Ask questions, get instant answers

🎙️ Audio Overview
   Listen to Zoya & Ravi discuss concepts
   [Generate Overview] or [Play] if already generated

──────────────────
[🖐 Open Circuit Whiteboard]

──────────────────
Practice
[→ Verilog Coding Task]
```

**Right panel — active content area**
- When Text Chat is selected: Chat interface loads
- When Audio Overview is clicked: Audio player with "Join Conversation" feature
- When Whiteboard is clicked: opens as full-screen overlay
- When Practice is clicked: navigates to `/topic/fsm/practice`

### Design & UX guidelines

This is a prototype but it must **not look like a prototype**. AMD judges are evaluating the quality of thinking, and a sloppy UI signals sloppy engineering.

**Colour palette**
- Primary background: `#0F1117` (near black)
- Card background: `#1A1D27`
- Accent: `#E8490F` (AMD red — intentional alignment)
- Secondary accent: `#4F9EF8` (blue for info states)
- Success: `#22C55E`
- Text primary: `#F1F5F9`
- Text secondary: `#94A3B8`

**Typography**
- Font: Inter (Google Fonts, free)
- Title: 24px bold
- Section header: 16px semibold
- Body: 14px regular
- Code: JetBrains Mono (monospace)

**Layout**
- Sidebar navigation: 220px fixed left, dark
- Main content: fills remaining width
- Max content width: 1100px centered
- Cards with 1px border `#2D3147`, slight border-radius (8px), no heavy shadows

**State feedback**
- Every button click must have immediate visual feedback (loading spinner or colour change)
- No silent failures — if an LLM call fails, show a clear message with a retry option
- No blank white screens at any point during demo

### Build steps

**Step 7.1 — React Router setup**
```
npm install react-router-dom
```
Set up all routes. Each module component mounts at its route.

**Step 7.2 — App shell**
- Sidebar with: Rycene logo, student name, "Dashboard" link, "FSM Design" topic link (locked/unlocked state shown here)
- Top bar: minimal — just page title and logout button
- Route-based content area

**Step 7.3 — Topic hub page**
- Build the contents list + navigation to each feature as described above

**Step 7.4 — Final integration**
- Ensure auth token flows to all API calls (Axios interceptor or fetch wrapper)
- Ensure competency update from Module 6 propagates back to sidebar badge
- Test the complete demo flow end to end (listed at top of this document)

### Acceptance criteria
- All routes load without errors
- Navigation between modules is seamless
- Auth gate works — unauthenticated users redirect to login
- Locked topics block navigation to their content pages
- The complete demo flow (6 steps listed at document top) runs without any hiccup

---

## Build Order & Daily Schedule

Given today is **Feb 25** and submission is **Mar 1**, here is the realistic daily plan.

### Day 1 — Feb 25 (Today) | Modules 1 + 7 skeleton

**Morning:**
- Set up React project (Vite + React + React Router + Tailwind or plain CSS)
- Set up FastAPI backend with SQLite
- Build login page + JWT auth
- Build instructor unlock endpoint + student dashboard (locked state)
- Seed demo accounts: `instructor@rycene.com / demo123` and `student@rycene.com / demo123`

**Afternoon:**
- Build app shell: sidebar, routing, all pages as empty stubs
- Unlock flow working end-to-end: instructor unlocks → student dashboard updates
- Module 1 complete and testable

**End of day check**: Can you log in, see a locked topic, switch to instructor, unlock it, switch back to student, see it unlocked? If yes, Day 1 is done.

---

### Day 2 — Feb 26 | Module 3 (Concept Conversation)

Start with Module 3 before Module 2 because Module 3 requires pre-generating audio, which takes time, and you need that audio ready.

**Morning:**
- Write the dialogue scripts for all 4 FSM sub-topics (use ChatGPT or Gemini to draft them — 30 mins)
- Generate all audio via ElevenLabs web UI or API (set up two voice profiles first)
- Download and store MP3 files in `/public/audio/fsm/`
- Build JSON manifests for each sub-topic

**Afternoon:**
- Build Conversation Player component (audio queue, speaker indicator, progress bar)
- Build Pause & Ask backend endpoint (LLM call + TTS)
- Integrate into Topic Hub page
- Test all 4 sub-topics play correctly + Pause & Ask works

**End of day check**: Can a student click a sub-topic, hear the two-voice conversation, pause, type a question, and hear a natural continuation? If yes, Day 2 is done.

---

### Day 3 — Feb 27 | Module 2 (MediaPipe Whiteboard)

**Morning:**
- Design or source the FSM circuit SVG (use draw.io — free, exports SVG)
- Label all 6 SVG elements with correct IDs
- Set up MediaPipe in browser: webcam feed, gesture recognizer running in animation loop
- Implement pointing detection + dwell timer

**Afternoon:**
- Connect gesture detection to SVG hotspot hit-testing
- Build explanation side panel
- Integrate ElevenLabs TTS for voice playback of explanations
- Build webcam permission screen + click fallback
- Test all 6 zones trigger correctly via both gesture and click

**End of day check**: Can a student point at the flip-flop symbol and hear the instructor's voice explain it within 2 seconds? If yes, Day 3 is done.

---

### Day 4 — Feb 28 | Modules 4 + 5 + 6 + Polish

**Morning:**
- Build Monaco Editor component with Verilog template
- Build hint endpoint (3 levels, LLM-powered)
- Build rubric endpoint (LLM rubric prompt)
- Connect hint display and rubric feedback view in practice page

**Afternoon:**
- Build skill map / competency tracker component
- Connect rubric submission → competency update → dashboard badge update
- Integration pass: test the entire demo flow from login to competency update
- Bug fixes from integration testing
- UI polish: colours, spacing, loading states, error handling

**End of day check**: Does the complete 6-step demo flow run without errors? Does it look presentable?

---

### Day 5 — Mar 1 | Demo Video + Submission

**Morning:**
- Final bug fixes from overnight testing
- Record demo video (3 minutes max):
  - Show instructor unlocking the topic
  - Show Circuit Whiteboard gesture interaction (use good lighting)
  - Show Concept Conversation with a Pause & Ask
  - Show practice task, hints, and rubric feedback
  - Show competency updating on dashboard
- Write AMD submission description (use the pitch paragraph from your planning)

**Afternoon:**
- Deploy to cloud (Render.com free tier for FastAPI backend, Vercel for React frontend — both free, both fast to set up)
- Submit to AMD Slingshot portal
- Commit all code to GitHub (AMD may ask for this)

---

## Environment & Dependencies

### Frontend
```
React 18 + Vite
React Router DOM
@monaco-editor/react
@mediapipe/tasks-vision
Inter font (Google Fonts)
JetBrains Mono font (Google Fonts)
Axios (API calls)
```

### Backend
```
Python 3.11+
FastAPI
uvicorn
python-jose (JWT)
sqlalchemy (ORM)
aiosqlite (async SQLite)
httpx (async HTTP for LLM/TTS API calls)
python-dotenv (secrets)
```

### External API keys needed (get these on Day 1)
```
OPENAI_API_KEY     or     GOOGLE_GEMINI_API_KEY
ELEVENLABS_API_KEY
```
Store in `.env` file, never commit to Git.

### Deployment
```
Backend: Render.com (free tier, FastAPI Docker deploy)
Frontend: Vercel (free tier, Vite React deploy)
```

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| ElevenLabs TTS latency too high for Pause & Ask | Medium | High | Pre-generate common follow-up questions; show typing indicator to mask wait time |
| MediaPipe gesture detection unreliable on demo laptop | Medium | High | Build and test click fallback on Day 3; always demo with fallback ready |
| LLM returns malformed JSON for rubric | Medium | Medium | Wrap all LLM JSON calls in try/except with a fallback message; test 10 times before demo |
| Cloud deployment has cold start delay | Low | Medium | Keep backend warm with a ping endpoint; or deploy to Railway which has no cold start on free tier |
| Audio files too large for free hosting | Low | Low | Compress MP3s to 64kbps (speech quality is sufficient); 4 topics × 10 segments × ~100KB = ~4MB total |
| Webcam not available at demo venue | Low | High | Always demo click-fallback mode as primary, show gesture as bonus if available |

---

## What is Explicitly NOT in the Prototype

These are Phase 2 items. Do not attempt them before Mar 1 — they will derail your timeline.

- Verilog simulation / waveform output (just tell AMD "simulation engine integrates in Phase 2")
- Originality check on written submissions
- Citation helper
- Hindi language support
- Job role mapping beyond the single dropdown
- Multiple topics beyond FSM Design
- Instructor batch analytics dashboard
- Spaced repetition planner
- Real Coqui XTTS-v2 fine-tuned on instructor voice (uses ElevenLabs for now)
- Mobile / PWA optimization

These are real features with real value — describe them to AMD as your Phase 2 roadmap, not as missing pieces.

---

## AMD Submission Checklist

Before submitting on Mar 1, confirm:

- [ ] Demo URL is live and accessible (test from a different network)
- [ ] Demo accounts work: `instructor@rycene.com` and `student@rycene.com`
- [ ] All 6 demo steps run without errors
- [ ] Demo video is under 3 minutes and shows all key features
- [ ] Submission description mentions: AI skilling coach, VLSI job readiness, MediaPipe gesture whiteboard, two-voice concept conversation, rubric-based feedback, progressive hints, real students (Rycene batch)
- [ ] Every AMD exploration path is mentioned: concept coach ✓, rubric feedback ✓, study planner (mention as tracker) ✓, multilingual (mention as Phase 2 roadmap) ✓, academic integrity ✓
- [ ] GitHub repo is public or shareable (AMD may ask)
- [ ] `.env` secrets are NOT in the repo

---

*Document version: 1.0 | Prepared: Feb 25, 2026 | For: AMD Slingshot 2026 Prototype Submission*
