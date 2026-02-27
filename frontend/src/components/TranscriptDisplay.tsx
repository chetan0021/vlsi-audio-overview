/**
 * TranscriptDisplay Component
 * Shows current dialogue text synchronized with audio playback
 */
import { useEffect, useRef } from 'react'
import './TranscriptDisplay.css'

interface AudioSegment {
  segment_id: string
  speaker: string
  text: string
  sequence: number
  duration_ms: number
  audio_url: string | null
}

interface TranscriptDisplayProps {
  segments: AudioSegment[]
  currentSegmentIndex: number
  autoScroll?: boolean
}

export function TranscriptDisplay({ 
  segments, 
  currentSegmentIndex,
  autoScroll = true 
}: TranscriptDisplayProps) {
  const currentSegmentRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to current segment
  useEffect(() => {
    if (autoScroll && currentSegmentRef.current) {
      currentSegmentRef.current.scrollIntoView({
        behavior: 'smooth',
        block: 'center'
      })
    }
  }, [currentSegmentIndex, autoScroll])

  if (segments.length === 0) {
    return (
      <div className="transcript-display empty">
        <p>No transcript available</p>
      </div>
    )
  }

  return (
    <div className="transcript-display">
      <div className="transcript-header">
        <h3>📝 Transcript</h3>
        <div className="segment-indicator">
          Segment {currentSegmentIndex + 1} of {segments.length}
        </div>
      </div>

      <div className="transcript-content">
        {segments.map((segment, index) => {
          const isCurrent = index === currentSegmentIndex
          const isPast = index < currentSegmentIndex
          
          return (
            <div
              key={segment.segment_id}
              ref={isCurrent ? currentSegmentRef : null}
              className={`transcript-segment ${segment.speaker} ${
                isCurrent ? 'current' : isPast ? 'past' : 'future'
              }`}
            >
              <div className="segment-header">
                <div className="speaker-info">
                  <span className={`speaker-icon ${segment.speaker}`}>
                    {segment.speaker === 'zoya' ? '👩‍🏫' : '👨‍🎓'}
                  </span>
                  <span className="speaker-name">
                    {segment.speaker === 'zoya' ? 'Zoya' : 'Ravi'}
                  </span>
                </div>
                {isCurrent && (
                  <span className="current-badge">▶ Playing</span>
                )}
              </div>
              
              <div className="segment-text">
                {segment.text}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
