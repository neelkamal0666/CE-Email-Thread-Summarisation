import './Modal.css'

function ThreadModal({ thread, onClose, onSummarize }) {
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="modal show" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <span className="close" onClick={onClose}>&times;</span>
        
        <h2>{thread.subject}</h2>
        <div className="thread-meta" style={{ marginBottom: '20px' }}>
          <span className="meta-item">📧 {thread.thread_id}</span>
          <span className="meta-item">📦 {thread.order_id}</span>
          <span className="meta-item">🛍️ {thread.product}</span>
        </div>
        
        <div style={{ background: '#f5f7fa', padding: '15px', borderRadius: '8px', marginBottom: '20px' }}>
          <strong>Topic:</strong> {thread.topic}
        </div>
        
        <h3 style={{ marginBottom: '15px' }}>Message Thread</h3>
        <div className="message-thread">
          {thread.messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.sender}`}>
              <div className="message-sender">
                {msg.sender === 'customer' ? '👤 Customer' : '👔 Agent'}
              </div>
              <div className="message-time">{formatDate(msg.timestamp)}</div>
              <div className="message-body">{msg.body}</div>
            </div>
          ))}
        </div>
        
        <div className="action-buttons">
          <button 
            className="btn btn-primary" 
            onClick={() => onSummarize(thread.thread_id)}
          >
            Generate Summary
          </button>
        </div>
      </div>
    </div>
  )
}

export default ThreadModal

