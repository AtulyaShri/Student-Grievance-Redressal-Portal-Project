import { useState, useEffect } from 'react'
import { useSearchParams, Link } from 'react-router-dom'
import { grievancesAPI } from '../api'

export default function Dashboard() {
  const [grievances, setGrievances] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [searchParams] = useSearchParams()
  const [filter, setFilter] = useState('All')

  useEffect(() => {
    fetchGrievances()
  }, [filter])

  const fetchGrievances = async () => {
    try {
      setLoading(true)
      setError('')
      // TODO: Use filter parameter in API call once backend supports it
      const data = await grievancesAPI.list()
      setGrievances(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load grievances')
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'Open':
        return 'bg-yellow-100 text-yellow-800'
      case 'In Progress':
        return 'bg-blue-100 text-blue-800'
      case 'Resolved':
        return 'bg-green-100 text-green-800'
      case 'Closed':
        return 'bg-slate-100 text-slate-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getCategoryColor = (category) => {
    const colors = {
      Academic: 'text-purple-600',
      Hostel: 'text-orange-600',
      Infrastructure: 'text-red-600',
      Administration: 'text-blue-600',
      Fees: 'text-green-600',
      Other: 'text-slate-600',
    }
    return colors[category] || 'text-slate-600'
  }

  const submitted = searchParams.get('submitted')

  return (
    <div className="max-w-6xl mx-auto mt-8 pb-8">
      {submitted && (
        <div className="mb-6 p-4 bg-green-50 text-green-700 rounded-lg border border-green-200">
          ✓ Your grievance has been submitted successfully. You can track its status below.
        </div>
      )}

      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
        <h2 className="text-2xl font-semibold">My Grievances</h2>
        <Link
          to="/submit"
          className="mt-4 md:mt-0 px-4 py-2 bg-sky-600 text-white rounded-lg hover:bg-sky-700 font-medium inline-block"
        >
          + Submit New Grievance
        </Link>
      </div>

      {/* Filters */}
      <div className="mb-6 flex gap-2 flex-wrap">
        {['All', 'Open', 'In Progress', 'Resolved', 'Closed'].map((status) => (
          <button
            key={status}
            onClick={() => setFilter(status)}
            className={`px-3 py-1 rounded-full text-sm font-medium transition ${
              filter === status
                ? 'bg-sky-600 text-white'
                : 'bg-slate-200 text-slate-700 hover:bg-slate-300'
            }`}
          >
            {status}
          </button>
        ))}
      </div>

      {error && (
        <div className="p-4 bg-red-50 text-red-600 rounded-lg mb-6">
          {error}
        </div>
      )}

      {loading && (
        <div className="text-center py-12">
          <p className="text-slate-600">Loading grievances...</p>
        </div>
      )}

      {!loading && grievances.length === 0 && (
        <div className="bg-slate-50 rounded-lg p-12 text-center">
          <p className="text-slate-600 mb-4">No grievances found</p>
          <Link
            to="/submit"
            className="inline-block px-4 py-2 bg-sky-600 text-white rounded-lg hover:bg-sky-700"
          >
            Submit your first grievance
          </Link>
        </div>
      )}

      {!loading && grievances.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-300 bg-slate-50">
                <th className="text-left py-3 px-4 font-semibold">ID</th>
                <th className="text-left py-3 px-4 font-semibold">Title</th>
                <th className="text-left py-3 px-4 font-semibold">Category</th>
                <th className="text-left py-3 px-4 font-semibold">Status</th>
                <th className="text-left py-3 px-4 font-semibold">Created</th>
                <th className="text-left py-3 px-4 font-semibold">Action</th>
              </tr>
            </thead>
            <tbody>
              {grievances.map((grievance) => (
                <tr key={grievance.id} className="border-b border-slate-200 hover:bg-slate-50">
                  <td className="py-3 px-4 text-slate-600">#{grievance.id}</td>
                  <td className="py-3 px-4 font-medium">{grievance.title}</td>
                  <td className={`py-3 px-4 font-medium ${getCategoryColor(grievance.category)}`}>
                    {grievance.category}
                  </td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded text-xs font-semibold ${getStatusColor(grievance.status)}`}>
                      {grievance.status}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-slate-600">
                    {new Date(grievance.created_at).toLocaleDateString()}
                  </td>
                  <td className="py-3 px-4">
                    <Link
                      to={`/grievance/${grievance.id}`}
                      className="text-sky-600 hover:text-sky-800 font-medium"
                    >
                      View
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
        <div className="bg-white p-4 rounded-lg border border-slate-200">
          <p className="text-sm text-slate-600 mb-1">Open Grievances</p>
          <p className="text-2xl font-bold">
            {grievances.filter((g) => g.status === 'Open').length}
          </p>
        </div>
        <div className="bg-white p-4 rounded-lg border border-slate-200">
          <p className="text-sm text-slate-600 mb-1">In Progress</p>
          <p className="text-2xl font-bold">
            {grievances.filter((g) => g.status === 'In Progress').length}
          </p>
        </div>
        <div className="bg-white p-4 rounded-lg border border-slate-200">
          <p className="text-sm text-slate-600 mb-1">Resolved</p>
          <p className="text-2xl font-bold">
            {grievances.filter((g) => g.status === 'Resolved').length}
          </p>
        </div>
      </div>
    </div>
  )
}
