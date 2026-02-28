import { useEffect, useState } from 'react'
import './LoadingIndicator.css'

interface LoadingIndicatorProps {
  message?: string
  estimatedSeconds?: number
  showProgress?: boolean
}

export function LoadingIndicator({ 
  message = 'Loading...', 
  estimatedSeconds,
  showProgress = false 
}: LoadingIndicatorProps) {
  const [elapsed, setElapsed] = useState(0)

  useEffect(() => {
    if (!showProgress || !estimatedSeconds) return

    const interval = setInterval(() => {
      setElapsed(prev => Math.min(prev + 1, estimatedSeconds))
    }, 1000)

    return () => clearInterval(interval)
  }, [showProgress, estimatedSeconds])

  const progress = estimatedSeconds ? (elapsed / estimatedSeconds) * 100 : 0

  return (
    <div className="loading-indicator">
      <div className="spinner"></div>
      <p className="loading-message">{message}</p>
      {showProgress && estimatedSeconds && (
        <div className="loading-progress">
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <p className="progress-text">
            {elapsed}s / {estimatedSeconds}s
          </p>
        </div>
      )}
    </div>
  )
}
