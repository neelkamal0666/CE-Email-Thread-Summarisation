import { useState, useEffect } from 'react'
import './Modal.css'

function SummaryModal({ summary, onClose, onSave, onApprove, onReject, onViewThread, onExport }) {
  const [editedSummary, setEditedSummary] = useState(summary.edited_summary || summary.original_summary)
  
  useEffect(() => {
    setEditedSummary(summary.edited_summary || summary.original_summary)
  }, [summary])

  const handleSave = (approve = false) => {
    onSave(summary.id, editedSummary, approve)
  }

  const isPending = summary.status === 'pending' || summary.status === 'edited'

  return (
    <div className="modal show" onClick={onClose}>
      <div className="modal-content large" onClick={(e) => e.stopPropagation()}>
        <span className="close" onClick={onClose}>&times;</span>
        
        <h2>Summary Review - {summary.thread_id}</h2>
        
        {summary.crm_context && (
          <div className="crm-context">
            <h4>🔗 CRM Context</h4>
            <div className="crm-grid">
              <div className="crm-item">
                <div className="crm-label">Order ID</div>
                <div className="crm-value">{summary.crm_context.order_id}</div>
              </div>
              <div className="crm-item">
                <div className="crm-label">Product</div>
                <div className="crm-value">{summary.crm_context.product}</div>
              </div>
            </div>
          </div>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', margin: '30px 0' }}>
          <div>
            <h3 style={{ marginBottom: '15px' }}>📊 Summary Details</h3>
            <div className="summary-section">
              <h4>Issue Summary</h4>
              <p>{editedSummary.issue_summary || 'N/A'}</p>
            </div>
            
            {Array.isArray(editedSummary.key_actions) && editedSummary.key_actions.length > 0 && (
              <div className="summary-section">
                <h4>Key Actions</h4>
                <ul>
                  {editedSummary.key_actions.map((action, idx) => (
                    <li key={idx}>{action}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="summary-section">
              <h4>Next Steps</h4>
              <p>{editedSummary.next_steps || 'N/A'}</p>
            </div>
          </div>

          <div>
            <h3 style={{ marginBottom: '15px' }}>📈 Metadata</h3>
            <div className="summary-section">
              <h4>Priority</h4>
              <p><span className={`badge badge-${getPriorityClass(editedSummary.priority)}`}>
                {editedSummary.priority}
              </span></p>
            </div>

            <div className="summary-section">
              <h4>Sentiment</h4>
              <p><span className={`badge badge-${getSentimentClass(editedSummary.sentiment)}`}>
                {editedSummary.sentiment}
              </span></p>
            </div>

            <div className="summary-section">
              <h4>Status</h4>
              <p><span className={`badge badge-${getStatusClass(editedSummary.resolution_status)}`}>
                {editedSummary.resolution_status}
              </span></p>
            </div>
          </div>
        </div>

        {isPending && (
          <div className="edit-section">
            <h3>✏️ Edit Summary</h3>
            <form>
              <div className="form-group">
                <label>Issue Summary</label>
                <textarea
                  value={editedSummary.issue_summary || ''}
                  onChange={(e) => setEditedSummary({...editedSummary, issue_summary: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Next Steps</label>
                <textarea
                  value={editedSummary.next_steps || ''}
                  onChange={(e) => setEditedSummary({...editedSummary, next_steps: e.target.value})}
                />
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '15px' }}>
                <div className="form-group">
                  <label>Priority</label>
                  <select
                    value={editedSummary.priority || 'medium'}
                    onChange={(e) => setEditedSummary({...editedSummary, priority: e.target.value})}
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Status</label>
                  <select
                    value={editedSummary.resolution_status || 'pending'}
                    onChange={(e) => setEditedSummary({...editedSummary, resolution_status: e.target.value})}
                  >
                    <option value="pending">Pending</option>
                    <option value="resolved">Resolved</option>
                    <option value="escalated">Escalated</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Sentiment</label>
                  <select
                    value={editedSummary.sentiment || 'neutral'}
                    onChange={(e) => setEditedSummary({...editedSummary, sentiment: e.target.value})}
                  >
                    <option value="positive">Positive</option>
                    <option value="neutral">Neutral</option>
                    <option value="negative">Negative</option>
                    <option value="frustrated">Frustrated</option>
                  </select>
                </div>
              </div>
              <div className="action-buttons">
                <button type="button" className="btn btn-primary" onClick={() => handleSave(false)}>
                  Save Edits
                </button>
                <button type="button" className="btn btn-success" onClick={() => handleSave(true)}>
                  Save & Approve
                </button>
                <button type="button" className="btn btn-danger" onClick={() => onReject(summary.id)}>
                  Reject
                </button>
              </div>
            </form>
          </div>
        )}

        {summary.status === 'approved' && (
          <div className="action-buttons">
            <button className="btn btn-success" onClick={() => onExport(summary.id)}>
              Export Summary
            </button>
            <button className="btn btn-primary" onClick={() => onViewThread(summary.thread_id)}>
              View Original Thread
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

function getPriorityClass(priority) {
  const classes = { low: 'info', medium: 'primary', high: 'warning', urgent: 'danger' }
  return classes[priority] || 'primary'
}

function getSentimentClass(sentiment) {
  const classes = { positive: 'success', neutral: 'info', negative: 'warning', frustrated: 'danger' }
  return classes[sentiment] || 'info'
}

function getStatusClass(status) {
  const classes = { pending: 'warning', resolved: 'success', escalated: 'danger' }
  return classes[status] || 'warning'
}

export default SummaryModal

