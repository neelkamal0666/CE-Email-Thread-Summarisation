import './ThreadsList.css'

function ThreadsList({ threads, onRefresh, onViewThread, onSummarizeThread }) {
  if (threads.length === 0) {
    return (
      <div className="threads-list">
        <div className="toolbar">
          <h2>Email Threads</h2>
          <button className="btn btn-secondary btn-small" onClick={onRefresh}>
            Refresh
          </button>
        </div>
        <div className="empty-state">
          <div className="empty-state-icon">📭</div>
          <div className="empty-state-text">
            No threads found. Import threads to get started.
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="threads-list">
      <div className="toolbar">
        <h2>Email Threads</h2>
        <button className="btn btn-secondary btn-small" onClick={onRefresh}>
          Refresh
        </button>
      </div>
      
      <div className="thread-cards">
        {threads.map(thread => (
          <div key={thread.thread_id} className="thread-card">
            <div className="thread-header">
              <div>
                <div className="thread-title">{thread.subject}</div>
                <div className="thread-meta">
                  <span className="meta-item">📧 {thread.thread_id}</span>
                  <span className="meta-item">📦 {thread.order_id}</span>
                  <span className="meta-item">🛍️ {thread.product}</span>
                  <span className="meta-item">💬 {thread.messages.length} messages</span>
                </div>
              </div>
              <div>
                <span className="badge badge-primary">{thread.initiated_by}</span>
              </div>
            </div>
            <div className="message-preview">
              <strong>Topic:</strong> {thread.topic}
            </div>
            <div className="action-buttons">
              <button 
                className="btn btn-primary btn-small"
                onClick={() => onViewThread(thread.thread_id)}
              >
                View Details
              </button>
              <button 
                className="btn btn-secondary btn-small"
                onClick={() => onSummarizeThread(thread.thread_id)}
              >
                Generate Summary
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ThreadsList

