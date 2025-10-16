import { useState, useEffect } from 'react'
import axios from 'axios'
import Header from './components/Header'
import Tabs from './components/Tabs'
import Dashboard from './components/Dashboard'
import ThreadsList from './components/ThreadsList'
import ReviewSummaries from './components/ReviewSummaries'
import ApprovedSummaries from './components/ApprovedSummaries'
import ThreadModal from './components/ThreadModal'
import SummaryModal from './components/SummaryModal'
import ProgressBar from './components/ProgressBar'
import './App.css'

const API_BASE_URL = '/api'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [analytics, setAnalytics] = useState({})
  const [threads, setThreads] = useState([])
  const [summaries, setSummaries] = useState([])
  const [currentThread, setCurrentThread] = useState(null)
  const [currentSummary, setCurrentSummary] = useState(null)
  const [showThreadModal, setShowThreadModal] = useState(false)
  const [showSummaryModal, setShowSummaryModal] = useState(false)
  const [statusMessage, setStatusMessage] = useState({ type: '', text: '' })
  const [processing, setProcessing] = useState({ active: false, current: 0, total: 0, message: '' })

  useEffect(() => {
    loadAnalytics()
    loadThreads()
    loadSummaries()
  }, [])

  useEffect(() => {
    if (activeTab === 'review') {
      loadPendingSummaries()
    } else if (activeTab === 'approved') {
      loadApprovedSummaries()
    }
  }, [activeTab])

  const api = axios.create({
    baseURL: API_BASE_URL,
  })

  const showSuccess = (message) => {
    setStatusMessage({ type: 'success', text: message })
    setTimeout(() => setStatusMessage({ type: '', text: '' }), 5000)
  }

  const showError = (message) => {
    setStatusMessage({ type: 'error', text: message })
    setTimeout(() => setStatusMessage({ type: '', text: '' }), 5000)
  }

  const loadAnalytics = async () => {
    try {
      const response = await api.get('/analytics')
      setAnalytics(response.data)
    } catch (error) {
      console.error('Failed to load analytics:', error)
    }
  }

  const loadThreads = async () => {
    try {
      const response = await api.get('/threads')
      setThreads(response.data)
    } catch (error) {
      console.error('Failed to load threads:', error)
    }
  }

  const loadSummaries = async () => {
    try {
      const response = await api.get('/summaries')
      setSummaries(response.data)
    } catch (error) {
      console.error('Failed to load summaries:', error)
    }
  }

  const loadPendingSummaries = async () => {
    try {
      const [pendingRes, editedRes] = await Promise.all([
        api.get('/summaries?status=pending'),
        api.get('/summaries?status=edited')
      ])
      setSummaries([...pendingRes.data, ...editedRes.data])
    } catch (error) {
      console.error('Failed to load pending summaries:', error)
    }
  }

  const loadApprovedSummaries = async () => {
    try {
      const response = await api.get('/summaries?status=approved')
      setSummaries(response.data)
    } catch (error) {
      console.error('Failed to load approved summaries:', error)
    }
  }

  const importThreads = async (file) => {
    try {
      if (!file) {
        showError('Please select a file to import')
        return
      }

      // Read the file
      const fileText = await file.text()
      const data = JSON.parse(fileText)
      
      // Validate the data structure
      if (!data.threads || !Array.isArray(data.threads)) {
        throw new Error('Invalid file format. Expected JSON with "threads" array.')
      }
      
      const result = await api.post('/threads/import', data)
      showSuccess(`Successfully imported ${result.data.imported} of ${result.data.total} threads`)
      loadAnalytics()
      loadThreads()
    } catch (error) {
      if (error instanceof SyntaxError) {
        showError('Invalid JSON file. Please check the file format.')
      } else {
        showError('Failed to import threads: ' + error.message)
      }
    }
  }

  const processAllThreads = async () => {
    try {
      const threadsToProcess = threads
      if (threadsToProcess.length === 0) {
        showError('No threads to process. Import threads first.')
        return
      }

      // Initialize progress
      setProcessing({
        active: true,
        current: 0,
        total: threadsToProcess.length,
        message: 'Processing threads...'
      })

      let processed = 0
      for (const thread of threadsToProcess) {
        try {
          await api.post(`/threads/${thread.thread_id}/summarize`)
          processed++
          
          // Update progress
          setProcessing({
            active: true,
            current: processed,
            total: threadsToProcess.length,
            message: `Processing thread ${processed} of ${threadsToProcess.length}...`
          })
        } catch (error) {
          console.error(`Failed to process thread ${thread.thread_id}:`, error)
        }
      }

      // Complete
      setProcessing({ active: false, current: 0, total: 0, message: '' })
      showSuccess(`Successfully processed ${processed} threads!`)
      loadAnalytics()
      loadSummaries()
      setActiveTab('review')
    } catch (error) {
      setProcessing({ active: false, current: 0, total: 0, message: '' })
      showError('Failed to process threads: ' + error.message)
    }
  }

  const viewThread = async (threadId) => {
    try {
      const response = await api.get(`/threads/${threadId}`)
      setCurrentThread(response.data)
      setShowThreadModal(true)
    } catch (error) {
      showError('Failed to load thread details')
    }
  }

  const summarizeThread = async (threadId) => {
    try {
      setProcessing({
        active: true,
        current: 0,
        total: 1,
        message: 'Generating summary...'
      })
      
      await api.post(`/threads/${threadId}/summarize`)
      
      setProcessing({
        active: true,
        current: 1,
        total: 1,
        message: 'Summary complete!'
      })
      
      setTimeout(() => {
        setProcessing({ active: false, current: 0, total: 0, message: '' })
        showSuccess('Summary generated successfully!')
        loadAnalytics()
        loadSummaries()
        setActiveTab('review')
      }, 500)
    } catch (error) {
      setProcessing({ active: false, current: 0, total: 0, message: '' })
      showError('Failed to generate summary: ' + error.message)
    }
  }

  const viewSummary = async (summaryId) => {
    try {
      const response = await api.get(`/summaries/${summaryId}`)
      setCurrentSummary(response.data)
      setShowSummaryModal(true)
    } catch (error) {
      showError('Failed to load summary details')
    }
  }

  const editSummary = async (summaryId) => {
    await viewSummary(summaryId)
  }

  const saveSummaryEdits = async (summaryId, editedSummary, approve = false) => {
    try {
      await api.put(`/summaries/${summaryId}/edit`, {
        edited_summary: editedSummary,
        user: 'CE Associate'
      })

      if (approve) {
        await api.post(`/summaries/${summaryId}/approve`, {
          user: 'CE Associate'
        })
        showSuccess('Summary approved successfully!')
      } else {
        showSuccess('Summary updated successfully!')
      }

      setShowSummaryModal(false)
      loadAnalytics()
      loadPendingSummaries()
    } catch (error) {
      showError('Failed to save edits: ' + error.message)
    }
  }

  const approveSummary = async (summaryId) => {
    try {
      await api.post(`/summaries/${summaryId}/approve`, {
        user: 'CE Associate'
      })
      showSuccess('Summary approved successfully!')
      loadAnalytics()
      loadPendingSummaries()
    } catch (error) {
      showError('Failed to approve summary: ' + error.message)
    }
  }

  const rejectSummary = async (summaryId) => {
    const reason = prompt('Please provide a reason for rejection:')
    if (!reason) return

    try {
      await api.post(`/summaries/${summaryId}/reject`, {
        user: 'CE Associate',
        reason: reason
      })
      showSuccess('Summary rejected')
      setShowSummaryModal(false)
      loadAnalytics()
      loadPendingSummaries()
    } catch (error) {
      showError('Failed to reject summary: ' + error.message)
    }
  }

  const exportSummary = async (summaryId) => {
    try {
      const response = await api.get(`/export/${summaryId}`)
      const exportData = response.data
      
      const dataStr = JSON.stringify(exportData, null, 2)
      const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr)
      const exportFileDefaultName = `summary_${exportData.thread_id}_${Date.now()}.json`
      
      const linkElement = document.createElement('a')
      linkElement.setAttribute('href', dataUri)
      linkElement.setAttribute('download', exportFileDefaultName)
      linkElement.click()
      
      showSuccess('Summary exported successfully!')
    } catch (error) {
      showError('Failed to export summary: ' + error.message)
    }
  }

  return (
    <div className="app">
      <Header />
      
      <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />

      <div className="tab-content-container">
        {processing.active && (
          <ProgressBar 
            current={processing.current}
            total={processing.total}
            message={processing.message}
          />
        )}
        {activeTab === 'dashboard' && (
          <Dashboard
            analytics={analytics}
            statusMessage={statusMessage}
            onImport={importThreads}
            onProcessAll={processAllThreads}
            disableActions={processing.active}
          />
        )}

        {activeTab === 'threads' && (
          <ThreadsList
            threads={threads}
            onRefresh={loadThreads}
            onViewThread={viewThread}
            onSummarizeThread={summarizeThread}
          />
        )}

        {activeTab === 'review' && (
          <ReviewSummaries
            summaries={summaries}
            onViewSummary={viewSummary}
            onEditSummary={editSummary}
            onApproveSummary={approveSummary}
            onRejectSummary={rejectSummary}
          />
        )}

        {activeTab === 'approved' && (
          <ApprovedSummaries
            summaries={summaries}
            onViewSummary={viewSummary}
            onExportSummary={exportSummary}
            onViewThread={viewThread}
          />
        )}
      </div>

      {showThreadModal && currentThread && (
        <ThreadModal
          thread={currentThread}
          onClose={() => setShowThreadModal(false)}
          onSummarize={(threadId) => {
            summarizeThread(threadId)
            setShowThreadModal(false)
          }}
        />
      )}

      {showSummaryModal && currentSummary && (
        <SummaryModal
          summary={currentSummary}
          onClose={() => setShowSummaryModal(false)}
          onSave={saveSummaryEdits}
          onApprove={approveSummary}
          onReject={rejectSummary}
          onViewThread={viewThread}
          onExport={exportSummary}
        />
      )}
    </div>
  )
}

export default App

