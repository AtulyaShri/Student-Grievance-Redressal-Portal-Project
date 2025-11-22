import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { grievancesAPI } from '../api'

export default function GrievanceDetail() {
  const { id } = useParams()
  const [grievance, setGrievance] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchGrievance()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id])

  const fetchGrievance = async () => {
    try {
      setLoading(true)
      setError('')
      const data = await grievancesAPI.get(id)
      setGrievance(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load grievance')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="py-12 text-center text-slate-600">Loading grievance...</div>
    )
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 text-red-700 rounded">{error}</div>
    )
  }

  if (!grievance) {
    return (
      <div className="p-8 text-center text-slate-600">Grievance not found.</div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-sm mt-6">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-semibold mb-1">{grievance.title}</h1>
          <p className="text-sm text-slate-500">#{grievance.id} • {grievance.category} • {grievance.department_name || 'N/A'}</p>
        </div>
        <div className="text-right">
          <div className={`inline-block px-3 py-1 rounded text-sm font-semibold ${
            grievance.status === 'Resolved' ? 'bg-green-100 text-green-800' : grievance.status === 'In Progress' ? 'bg-blue-100 text-blue-800' : 'bg-yellow-100 text-yellow-800'
          }`}>
            {grievance.status}
          </div>
          <div className="text-xs text-slate-500 mt-1">Created: {new Date(grievance.created_at).toLocaleString()}</div>
        </div>
      </div>

      <section className="mt-6">
        <h2 className="text-sm font-medium text-slate-700 mb-2">Description</h2>
        <div className="prose max-w-none text-slate-700">{grievance.description}</div>
      </section>

      {grievance.attachment && (
        <section className="mt-6">
          <h3 className="text-sm font-medium text-slate-700 mb-2">Attachment</h3>
          <a href={grievance.attachment_url || '#'} className="text-sky-600 hover:text-sky-800">Download file</a>
        </section>
      )}

      {/* Timeline / Audit log if available */}
      {grievance.audits && grievance.audits.length > 0 && (
        <section className="mt-6">
          <h3 className="text-sm font-medium text-slate-700 mb-2">History</h3>
          <ul className="space-y-2">
            {grievance.audits.map((a) => (
              <li key={a.id} className="p-3 bg-slate-50 rounded">
                <div className="text-sm text-slate-700">{a.note}</div>
                <div className="text-xs text-slate-500 mt-1">{new Date(a.created_at).toLocaleString()}</div>
              </li>
            ))}
          </ul>
        </section>
      )}

      <div className="mt-6 flex gap-3">
        <Link to="/dashboard" className="px-4 py-2 border rounded">Back to dashboard</Link>
      </div>
    </div>
  )
}
