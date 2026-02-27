/**
 * AudioPlayer Component
 * Handles audio playback with play/pause controls and progress tracking
 */
import { useState, useEffect, useRef } from 'react'
import './AudioPlayer.css'

interface AudioSegment {
  segment_id: string
  speaker: string
  text: string
  sequence: number
  duration_ms: number
  audio_url: string | null
}

interface AudioPlayerProps {
  segments: AudioSegment[]
  onSegmentChange?: (index: number) => void
  onPlaybackComplete?: () => void
}

export function AudioPlayer({ segments, onSegmentChange, onPlaybackComplete }: AudioPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentSegmentIndex, setCurrentSegmentIndex] = useState(0)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [isLoading, setIsLoading] = useState(false)
  
  const audioRef = useRef<HTMLAudioElement>(null)

  // Load current segment
  useEffect(() => {
    if (segments.length === 0) return
    
    const currentSegment = segments[currentSegmentIndex]
    if (!currentSegment?.audio_url) {
      console.warn('No audio URL for segment', currentSegmentIndex)
      return
    }

    setIsLoading(true)
    
    if (audioRef.current) {
      audioRef.current.src = currentSegment.audio_url
      audioRef.current.load()
    }
  }, [currentSegmentIndex, segments])

  // Handle audio events
  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const handleLoadedMetadata = () => {
      setDuration(audio.duration)
      setIsLoading(false)
    }

    const handleTimeUpdate = () => {
      setCurrentTime(audio.currentTime)
    }

    const handleEnded = () => {
      // Move to next segment
      if (currentSegmentIndex < segments.length - 1) {
        setCurrentSegmentIndex(prev => prev + 1)
        setCurrentTime(0)
      } else {
        // Playback complete
        setIsPlaying(false)
        onPlaybackComplete?.()
      }
    }

    const handleCanPlay = () => {
      if (isPlaying) {
        audio.play().catch(err => console.error('Playback error:', err))
      }
    }

    audio.addEventListener('loadedmetadata', handleLoadedMetadata)
    audio.addEventListener('timeupdate', handleTimeUpdate)
    audio.addEventListener('ended', handleEnded)
    audio.addEventListener('canplay', handleCanPlay)

    return () => {
      audio.removeEventListener('loadedmetadata', handleLoadedMetadata)
      audio.removeEventListener('timeupdate', handleTimeUpdate)
      audio.removeEventListener('ended', handleEnded)
      audio.removeEventListener('canplay', handleCanPlay)
    }
  }, [currentSegmentIndex, segments, isPlaying, onPlaybackComplete])

  // Notify parent of segment changes
  useEffect(() => {
    onSegmentChange?.(currentSegmentIndex)
  }, [currentSegmentIndex, onSegmentChange])

  const togglePlayPause = () => {
    if (!audioRef.current) return

    if (isPlaying) {
      audioRef.current.pause()
    } else {
      audioRef.current.play().catch(err => console.error('Playback error:', err))
    }
    setIsPlaying(!isPlaying)
  }

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTime = parseFloat(e.target.value)
    if (audioRef.current) {
      audioRef.current.currentTime = newTime
      setCurrentTime(newTime)
    }
  }

  const skipToSegment = (index: number) => {
    if (index >= 0 && index < segments.length) {
      setCurrentSegmentIndex(index)
      setCurrentTime(0)
    }
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  if (segments.length === 0) {
    return (
      <div className="audio-player empty">
        <p>No audio segments available</p>
      </div>
    )
  }

  const currentSegment = segments[currentSegmentIndex]
  const hasAudio = segments.some(seg => seg.audio_url)

  if (!hasAudio) {
    return (
      <div className="audio-player no-audio">
        <p>⚠️ Audio synthesis not available (requires Python 3.10 with TTS)</p>
        <p>Dialogue text is available below</p>
      </div>
    )
  }

  return (
    <div className="audio-player">
      <audio ref={audioRef} preload="auto" />
      
      <div className="player-info">
        <div className="current-speaker">
          <span className={`speaker-icon ${currentSegment.speaker}`}>
            {currentSegment.speaker === 'zoya' ? '👩‍🏫' : '👨‍🎓'}
          </span>
          <span className="speaker-name">
            {currentSegment.speaker === 'zoya' ? 'Zoya' : 'Ravi'}
          </span>
        </div>
        <div className="segment-counter">
          Segment {currentSegmentIndex + 1} of {segments.length}
        </div>
      </div>

      <div className="player-controls">
        <button 
          onClick={togglePlayPause}
          disabled={isLoading || !currentSegment.audio_url}
          className="play-pause-btn"
        >
          {isLoading ? '⏳' : isPlaying ? '⏸️' : '▶️'}
        </button>

        <div className="progress-container">
          <input
            type="range"
            min="0"
            max={duration || 0}
            value={currentTime}
            onChange={handleSeek}
            className="progress-bar"
            disabled={isLoading}
          />
          <div className="time-display">
            <span>{formatTime(currentTime)}</span>
            <span>{formatTime(duration)}</span>
          </div>
        </div>

        <div className="segment-nav">
          <button
            onClick={() => skipToSegment(currentSegmentIndex - 1)}
            disabled={currentSegmentIndex === 0}
            className="nav-btn"
          >
            ⏮️
          </button>
          <button
            onClick={() => skipToSegment(currentSegmentIndex + 1)}
            disabled={currentSegmentIndex === segments.length - 1}
            className="nav-btn"
          >
            ⏭️
          </button>
        </div>
      </div>
    </div>
  )
}
