import './Tabs.css'

function Tabs({ activeTab, setActiveTab }) {
  const tabs = [
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'threads', label: 'Email Threads' },
    { id: 'review', label: 'Review & Approve' },
    { id: 'approved', label: 'Approved Summaries' }
  ]

  return (
    <nav className="tabs">
      {tabs.map(tab => (
        <button
          key={tab.id}
          className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
          onClick={() => setActiveTab(tab.id)}
        >
          {tab.label}
        </button>
      ))}
    </nav>
  )
}

export default Tabs

