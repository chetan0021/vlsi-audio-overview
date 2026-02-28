import './ErrorDisplay.css'

interface ErrorDisplayProps {
  error: string
  type?: 'api' | 'network' | 'audio' | 'general'
  onRetry?: () => void
  onDismiss?: () => void
}

export function ErrorDisplay({ error, type = 'general', onRetry, onDismiss }: ErrorDisplayProps) {
  const getErrorIcon = () => {
    switch (type) {
      case 'api':
        return '🔌'
      case 'network':
        return '📡'
      case 'audio':
        return '🔊'
      default:
        return '⚠️'
    }
  }

  const getErrorTitle = () => {
    switch (type) {
      case 'api':
        return 'API Error'
      case 'network':
        return 'Connection Error'
      case 'audio':
        return 'Audio Error'
      default:
        return 'Error'
    }
  }

  const getSuggestion = () => {
    switch (type) {
      case 'api':
        return 'The API service encountered an error. Please try again.'
      case 'network':
        return 'Please check your internet connection and try again.'
      case 'audio':
        return 'Audio playback failed. Try refreshing the page.'
      default:
        return 'An unexpected error occurred.'
    }
  }

  return (
    <div className={`error-display error-${type}`}>
      <div className="error-icon">{getErrorIcon()}</div>
      <div className="error-content">
        <h3 className="error-title">{getErrorTitle()}</h3>
        <p className="error-message">{error}</p>
        <p className="error-suggestion">{getSuggestion()}</p>
        <div className="error-actions">
          {onRetry && (
            <button onClick={onRetry} className="retry-btn">
              🔄 Retry
            </button>
          )}
          {onDismiss && (
            <button onClick={onDismiss} className="dismiss-btn">
              ✕ Dismiss
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
