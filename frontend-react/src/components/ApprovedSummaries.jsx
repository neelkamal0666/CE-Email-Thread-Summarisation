import SummaryCard from './SummaryCard'
import './ApprovedSummaries.css'

function ApprovedSummaries({ summaries, onViewSummary, onExportSummary, onViewThread }) {
  if (summaries.length === 0) {
    return (
      <div className="approved-summaries">
        <h2>Approved Summaries</h2>
        <div className="empty-state">
          <div className="empty-state-icon">📋</div>
          <div className="empty-state-text">No approved summaries yet.</div>
        </div>
      </div>
    )
  }

  return (
    <div className="approved-summaries">
      <h2>Approved Summaries</h2>
      <div className="summaries-list">
        {summaries.map(summary => (
          <SummaryCard
            key={summary.id}
            summary={summary}
            showActions={false}
            onView={() => onViewSummary(summary.id)}
            onExport={() => onExportSummary(summary.id)}
          />
        ))}
      </div>
    </div>
  )
}

export default ApprovedSummaries

