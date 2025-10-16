import './ProgressBar.css'

function ProgressBar({ current, total, message }) {
  const percentage = total > 0 ? Math.round((current / total) * 100) : 0

  return (
    <div className="progress-container">
      <div className="progress-info">
        <span className="progress-message">{message}</span>
        <span className="progress-stats">{current} / {total}</span>
      </div>
      <div className="progress-bar-wrapper">
        <div 
          className="progress-bar-fill"
          style={{ width: `${percentage}%` }}
        >
          <span className="progress-percentage">{percentage}%</span>
        </div>
      </div>
    </div>
  )
}

export default ProgressBar

