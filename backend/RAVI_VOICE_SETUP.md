# Setting Up Ravi's Male Voice

## Problem
Currently, Ravi's voice sounds female because we're using Zoya's voice sample as a fallback. XTTS-v2 clones whatever voice sample you provide, so we need a male voice sample for Ravi.

## Solution Options

### Option 1: Record Your Own Male Voice (Recommended - Free & Best Quality)
1. Record 6-10 seconds of a male voice saying any text (clear, no background noise)
2. Save as MP3 format
3. Place in: `backend/voice_samples/ravi/sample_01.mp3`
4. The TTS engine will automatically use it

### Option 2: Use Free Male Voice Samples Online
You can download free male voice samples from:
- **LibriVox** (public domain audiobooks): https://librivox.org/
- **Common Voice** (Mozilla): https://commonvoice.mozilla.org/
- **Free Spoken Digit Dataset**: https://github.com/Jakobovski/free-spoken-digit-dataset

Steps:
1. Download a short clip (6-10 seconds) of clear male speech
2. Convert to MP3 if needed
3. Save to: `backend/voice_samples/ravi/sample_01.mp3`

### Option 3: Generate Using Another TTS (Quick Test)
1. Use a free TTS service like https://ttsfree.com/ or https://ttsmaker.com/
2. Generate a male voice saying: "Hello, I'm Ravi. I'm excited to learn about VLSI design."
3. Download as MP3
4. Save to: `backend/voice_samples/ravi/sample_01.mp3`

## Quick Test After Adding Sample
Run this command to test:
```bash
C:\Users\Chetan\Documents\Rycene\backend\venv_tts\Scripts\python.exe C:\Users\Chetan\Documents\Rycene\backend\test_tts_auto.py
```

## File Structure
```
backend/
├── voice_samples/
│   ├── zoya/          # Female instructor voice (already set up)
│   │   ├── sample_01.mp3
│   │   ├── sample_02.mp3
│   │   └── ...
│   └── ravi/          # Male co-host voice (YOU NEED TO ADD THIS)
│       └── sample_01.mp3  # Add your male voice sample here
```

## Requirements for Voice Sample
- **Duration**: 6-10 seconds minimum
- **Format**: MP3 (preferred) or WAV
- **Quality**: Clear speech, minimal background noise
- **Content**: Any natural speech (doesn't matter what is said)
- **Voice**: Male voice for Ravi (co-host character)

## Why This Matters
XTTS-v2 is a voice cloning model - it learns the voice characteristics from your sample and applies them to any text. Without a male sample for Ravi, it will use whatever fallback we provide (currently Zoya's female voice).
