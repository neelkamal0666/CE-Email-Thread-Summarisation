import SummaryCard from './SummaryCard'
import './ReviewSummaries.css'

function ReviewSummaries({ summaries, onViewSummary, onEditSummary, onApproveSummary, onRejectSummary }) {
  if (summaries.length === 0) {
    return (
      <div className="review-summaries">
        <h2>Review & Approve Summaries</h2>
        <div className="empty-state">
          <div className="empty-state-icon">✅</div>
          <div className="empty-state-text">No summaries pending review. All caught up!</div>
        </div>
      </div>
    )
  }

  return (
    <div className="review-summaries">
      <h2>Review & Approve Summaries</h2>
      <div className="summaries-list">
        {summaries.map(summary => (
          <SummaryCard
            key={summary.id}
            summary={summary}
            showActions={true}
            onView={() => onViewSummary(summary.id)}
            onEdit={() => onEditSummary(summary.id)}
            onApprove={() => onApproveSummary(summary.id)}
            onReject={() => onRejectSummary(summary.id)}
          />
        ))}
      </div>
    </div>
  )
}

export default ReviewSummaries

