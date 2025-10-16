import './SummaryCard.css'

function SummaryCard({ summary, showActions, onView, onEdit, onApprove, onReject, onExport }) {
  const editedSummary = summary.edited_summary || summary.original_summary

  const getPriorityBadge = (priority) => {
    const badges = {
      low: { class: 'badge-info', text: 'Low Priority' },
      medium: { class: 'badge-primary', text: 'Medium Priority' },
      high: { class: 'badge-warning', text: 'High Priority' },
      urgent: { class: 'badge-danger', text: 'Urgent' }
    }
    const badge = badges[priority] || badges.medium
    return <span className={`badge ${badge.class}`}>{badge.text}</span>
  }

  const getStatusBadge = (status) => {
    const badges = {
      pending: { class: 'badge-warning', text: 'Pending' },
      resolved: { class: 'badge-success', text: 'Resolved' },
      escalated: { class: 'badge-danger', text: 'Escalated' }
    }
    const badge = badges[status] || badges.pending
    return <span className={`badge ${badge.class}`}>{badge.text}</span>
  }

  const getSentimentBadge = (sentiment) => {
    const badges = {
      positive: { class: 'badge-success', text: 'Positive' },
      neutral: { class: 'badge-info', text: 'Neutral' },
      negative: { class: 'badge-warning', text: 'Negative' },
      frustrated: { class: 'badge-danger', text: 'Frustrated' }
    }
    const badge = badges[sentiment] || badges.neutral
    return <span className={`badge ${badge.class}`}>{badge.text}</span>
  }

  return (
    <div className="summary-card">
      <div className="summary-header">
        <div>
          <div className="thread-title">Thread: {summary.thread_id}</div>
          <div className="summary-meta">
            {getPriorityBadge(editedSummary.priority)}
            {getStatusBadge(editedSummary.resolution_status)}
            {getSentimentBadge(editedSummary.sentiment)}
            <span className="badge badge-info">{summary.summary_type}</span>
          </div>
        </div>
        <div>
          <span className={`badge ${summary.status === 'approved' ? 'badge-success' : 'badge-warning'}`}>
            {summary.status}
          </span>
        </div>
      </div>
      
      <div className="summary-content">
        <div className="summary-section">
          <h4>📝 Issue Summary</h4>
          <p>{editedSummary.issue_summary || 'N/A'}</p>
        </div>
        
        {editedSummary.next_steps && (
          <div className="summary-section">
            <h4>🎯 Next Steps</h4>
            <p>{editedSummary.next_steps}</p>
          </div>
        )}
        
        {editedSummary.tags && editedSummary.tags.length > 0 && (
          <div className="summary-section">
            <h4>🏷️ Tags</h4>
            <div className="tag-list">
              {editedSummary.tags.map((tag, idx) => (
                <span key={idx} className="tag">{tag}</span>
              ))}
            </div>
          </div>
        )}
      </div>
      
      <div className="action-buttons">
        <button className="btn btn-primary btn-small" onClick={onView}>
          View Full Details
        </button>
        {showActions && (
          <>
            <button className="btn btn-secondary btn-small" onClick={onEdit}>
              Edit
            </button>
            <button className="btn btn-success btn-small" onClick={onApprove}>
              Approve
            </button>
            <button className="btn btn-danger btn-small" onClick={onReject}>
              Reject
            </button>
          </>
        )}
        {summary.status === 'approved' && onExport && (
          <button className="btn btn-success btn-small" onClick={onExport}>
            Export
          </button>
        )}
      </div>
    </div>
  )
}

export default SummaryCard

