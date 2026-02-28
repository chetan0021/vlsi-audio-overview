import { useState, useEffect } from 'react'
import './App.css'
import { AudioPlayer } from './components/AudioPlayer'
import { TranscriptDisplay } from './components/TranscriptDisplay'
import { LoadingIndicator } from './components/LoadingIndicator'
import { ErrorDisplay } from './components/ErrorDisplay'

interface DialogueSegment {
  segment_id: string
  speaker: string
  text: string
  sequence: number
  duration_ms: number
  audio_url: string | null
}

interface QuestionResponse {
  success: boolean
  response_id: string
  question: string
  segments_count: number
  segments: DialogueSegment[]
  tts_enabled: boolean
}

function App() {
  const [apiStatus, setApiStatus] = useState<string>('checking...')
  const [isGenerating, setIsGenerating] = useState(false)
  const [dialogue, setDialogue] = useState<DialogueSegment[]>([])
  const [error, setError] = useState<string>('')
  const [errorType, setErrorType] = useState<'api' | 'network' | 'audio' | 'general'>('general')
  const [currentSegmentIndex, setCurrentSegmentIndex] = useState(0)
  
  // Question state
  const [question, setQuestion] = useState<string>('')
  const [isAskingQuestion, setIsAskingQuestion] = useState(false)
  const [questionResponse, setQuestionResponse] = useState<DialogueSegment[]>([])

  useEffect(() => {
    // Check backend API connection
    fetch('/api/')
      .then(res => res.json())
      .then(data => setApiStatus(data.message))
      .catch(() => setApiStatus('Backend not connected'))
  }, [])

  const generateDialogue = async () => {
    setIsGenerating(true)
    setError('')
    setDialogue([])
    setQuestionResponse([])
    setCurrentSegmentIndex(0)
    
    try {
      const response = await fetch('/api/overview/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          topic: 'FSM Design Basics',
          duration_minutes: 2,
          context: 'Brief introduction to FSM fundamentals and one simple example'
        })
      })
      
      const data = await response.json()
      
      if (data.success) {
        setDialogue(data.segments)
        setError('')
      } else {
        setError(data.error || 'Failed to generate dialogue')
        setErrorType('api')
      }
    } catch (err) {
      setError('Network error: ' + (err as Error).message)
      setErrorType('network')
    } finally {
      setIsGenerating(false)
    }
  }

  const askQuestion = async () => {
    if (!question.trim()) return
    
    setIsAskingQuestion(true)
    setError('')
    setQuestionResponse([])
    
    try {
      const response = await fetch('/api/question/text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question,
          topic: 'FSM Design',
          context: 'We are discussing Finite State Machines and their applications.'
        })
      })
      
      const data: QuestionResponse = await response.json()
      
      if (data.success) {
        setQuestionResponse(data.segments)
        setQuestion('')
        setError('')
      } else {
        setError(data.error || 'Failed to get response')
        setErrorType('api')
      }
    } catch (err) {
      setError('Network error: ' + (err as Error).message)
      setErrorType('network')
    } finally {
      setIsAskingQuestion(false)
    }
  }

  const handleSegmentChange = (index: number) => {
    setCurrentSegmentIndex(index)
  }

  const handlePlaybackComplete = () => {
    console.log('Playback completed!')
  }

  return (
    <div className="App">
      <header>
        <h1>🎓 VLSI Audio Overview</h1>
        <p>NotebookLM-style learning for VLSI education</p>
      </header>
      
      <main>
        <div className="status-card">
          <h2>System Status</h2>
          <p>Backend API: <strong>{apiStatus}</strong></p>
        </div>
        
        <div className="test-card">
          <h2>🎬 Generate Audio Overview</h2>
          <p>Generate a 2-minute dialogue between Zoya and Ravi about FSM Design (5-7 segments)</p>
          
          <button 
            onClick={generateDialogue} 
            disabled={isGenerating}
            className="generate-btn"
          >
            {isGenerating ? '⏳ Generating...' : '🎬 Generate Dialogue'}
          </button>
          
          {error && (
            <ErrorDisplay 
              error={error}
              type={errorType}
              onRetry={generateDialogue}
              onDismiss={() => setError('')}
            />
          )}
          
          {isGenerating && (
            <LoadingIndicator 
              message="Generating dialogue and synthesizing audio..."
              estimatedSeconds={300}
              showProgress={true}
            />
          )}
          
          {dialogue.length > 0 && !isGenerating && (
            <div className="audio-overview-container">
              <AudioPlayer 
                segments={dialogue}
                onSegmentChange={handleSegmentChange}
                onPlaybackComplete={handlePlaybackComplete}
              />
              
              <TranscriptDisplay 
                segments={dialogue}
                currentSegmentIndex={currentSegmentIndex}
              />
            </div>
          )}
        </div>

        <div className="test-card">
          <h2>💬 Ask a Question</h2>
          <p>Test the "Join Conversation" feature by asking Zoya and Ravi a question</p>
          
          <div className="question-input-container">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && askQuestion()}
              placeholder="e.g., What's the difference between Moore and Mealy machines?"
              className="question-input"
              disabled={isAskingQuestion}
            />
            <button 
              onClick={askQuestion}
              disabled={isAskingQuestion || !question.trim()}
              className="ask-btn"
            >
              {isAskingQuestion ? '⏳ Asking...' : '🎤 Ask'}
            </button>
          </div>

          {questionResponse.length > 0 && (
            <div className="dialogue-container">
              <h3>💡 Response ({questionResponse.length} segments)</h3>
              <div className="dialogue-list">
                {questionResponse.map((segment) => (
                  <div 
                    key={segment.segment_id} 
                    className={`dialogue-segment ${segment.speaker}`}
                  >
                    <div className="speaker-badge">
                      {segment.speaker === 'zoya' ? '👩‍🏫 Zoya' : '👨‍🎓 Ravi'}
                    </div>
                    <div className="dialogue-text">
                      {segment.text}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {isAskingQuestion && (
            <LoadingIndicator 
              message="Processing your question..."
              estimatedSeconds={30}
              showProgress={true}
            />
          )}
        </div>
        
        <div className="info-card">
          <h3>🎙️ Features Status</h3>
          <p>✅ Dialogue generation with Gemini AI</p>
          <p>✅ Audio player with playback controls</p>
          <p>✅ Synchronized transcript display</p>
          <p>✅ Question answering (text input)</p>
          <p>✅ Contextual responses from Zoya & Ravi</p>
          <p>⏳ Audio synthesis with voice cloning (requires Python 3.10)</p>
          <p>⏳ Voice input for questions (microphone)</p>
        </div>
      </main>
    </div>
  )
}

export default App
