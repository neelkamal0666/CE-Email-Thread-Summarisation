import { useRef, useState } from 'react'
import './Dashboard.css'

function Dashboard({ analytics, statusMessage, onImport, onProcessAll, disableActions }) {
  const fileInputRef = useRef(null)
  const [showFormat, setShowFormat] = useState(false)

  const handleImportClick = () => {
    fileInputRef.current?.click()
  }

  const handleFileChange = (event) => {
    const file = event.target.files?.[0]
    if (file) {
      onImport(file)
      // Reset the input so the same file can be selected again
      event.target.value = ''
    }
  }

  const toggleFormat = () => {
    setShowFormat(!showFormat)
  }

  const exampleFormat = `{
  "version": "v2",
  "threads": [
    {
      "thread_id": "CE-405467-683",
      "topic": "Damaged product on arrival",
      "subject": "Order 405467-683: Damaged item received",
      "initiated_by": "customer",
      "order_id": "405467-683",
      "product": "LED Monitor",
      "messages": [
        {
          "id": "m1",
          "sender": "customer",
          "timestamp": "2025-09-12T06:39:29",
          "body": "Hello, my item arrived damaged..."
        },
        {
          "id": "m2",
          "sender": "company",
          "timestamp": "2025-09-12T06:49:29",
          "body": "We apologize for the inconvenience..."
        }
      ]
    }
  ]
}`

  return (
    <div className="dashboard">
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{analytics.total_threads || 0}</div>
          <div className="stat-label">Total Threads</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{analytics.total_summaries || 0}</div>
          <div className="stat-label">Generated Summaries</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{analytics.pending_summaries || 0}</div>
          <div className="stat-label">Pending Review</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{analytics.approved_summaries || 0}</div>
          <div className="stat-label">Approved</div>
        </div>
      </div>

      <div className="action-section">
        <h2>Quick Actions</h2>
        <div className="button-group">
          <input
            ref={fileInputRef}
            type="file"
            accept=".json,.txt"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
          <button 
            className="btn btn-primary" 
            onClick={handleImportClick}
            disabled={disableActions}
          >
            📁 Import Email Threads
          </button>
          <button 
            className="btn btn-secondary" 
            onClick={onProcessAll}
            disabled={disableActions}
          >
            {disableActions ? '⏳ Processing...' : 'Process All Threads'}
          </button>
        </div>
        <div className="format-section">
          <button className="btn-link" onClick={toggleFormat}>
            📋 {showFormat ? 'Hide' : 'Show'} Expected File Format
          </button>
        </div>
        {showFormat && (
          <div className="format-example">
            <div className="format-header">
              <strong>Expected JSON Format:</strong>
              <button 
                className="btn-copy"
                onClick={() => {
                  navigator.clipboard.writeText(exampleFormat)
                  alert('Format copied to clipboard!')
                }}
              >
                📋 Copy
              </button>
            </div>
            <pre className="format-code">{exampleFormat}</pre>
            <div className="format-note">
              <strong>Required fields:</strong>
              <ul>
                <li><code>threads</code> - Array of thread objects</li>
                <li><code>thread_id</code> - Unique identifier for the thread</li>
                <li><code>order_id</code> - Order/ticket number</li>
                <li><code>product</code> - Product name</li>
                <li><code>messages</code> - Array of message objects with sender, timestamp, and body</li>
              </ul>
            </div>
          </div>
        )}
        <div className="import-hint">
          <small>💡 Upload a JSON file with email thread data to begin processing</small>
        </div>
        {statusMessage.text && (
          <div className={`status-message ${statusMessage.type}`}>
            {statusMessage.text}
          </div>
        )}
      </div>
    </div>
  )
}

export default Dashboard

