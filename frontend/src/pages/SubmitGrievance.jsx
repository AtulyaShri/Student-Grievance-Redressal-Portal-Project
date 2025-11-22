import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { grievancesAPI, filesAPI } from '../api'

export default function SubmitGrievance() {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [category, setCategory] = useState('Academic')
  const [deptId, setDeptId] = useState('')
  const [file, setFile] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const grievanceData = {
        title,
        description,
        category,
        dept_id: deptId ? parseInt(deptId) : null,
      }

      const response = await grievancesAPI.create(grievanceData)
      
      // If file is attached, upload it too
      if (file) {
        await filesAPI.upload(file, response.data.id)
      }

      navigate('/dashboard?submitted=true')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit grievance. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow-sm mt-8">
      <h2 className="text-2xl font-semibold mb-6">Submit a Grievance</h2>
      
      {error && (
        <div className="mb-4 p-3 bg-red-50 text-red-600 rounded text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Title *</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500"
            placeholder="Short descriptive title"
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Category *</label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500"
            >
              <option>Academic</option>
              <option>Hostel</option>
              <option>Infrastructure</option>
              <option>Administration</option>
              <option>Fees</option>
              <option>Other</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Department</label>
            <select
              value={deptId}
              onChange={(e) => setDeptId(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500"
            >
              <option value="">Select department</option>
              <option value="1">Computer Science</option>
              <option value="2">Examination</option>
              <option value="3">Hostel</option>
              <option value="4">Finance</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Description *</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500"
            rows={6}
            placeholder="Describe the issue with details, dates, and what actions you've already taken"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Attach file (optional)</label>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files?.[0])}
            className="w-full"
            accept=".pdf,.png,.jpg,.jpeg"
          />
          <p className="text-xs text-slate-500 mt-1">Allowed: PDF, PNG, JPG. Max 5MB</p>
        </div>

        <div className="flex gap-3 pt-4">
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2 bg-sky-600 text-white rounded-lg hover:bg-sky-700 disabled:bg-sky-400 font-medium"
          >
            {loading ? 'Submitting...' : 'Submit Grievance'}
          </button>
          <button
            type="button"
            onClick={() => navigate('/dashboard')}
            className="px-6 py-2 border border-slate-300 rounded-lg hover:bg-slate-50"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  )
}
