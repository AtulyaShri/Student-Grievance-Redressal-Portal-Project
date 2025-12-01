import { Link, useNavigate } from 'react-router-dom'
import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'

export default function Header() {
  const { user, logout } = useContext(AuthContext)
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <header className="bg-white shadow-sm sticky top-0 z-20">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-full bg-sky-600 flex items-center justify-center text-white font-bold">
            
          </div>
          <div>
            <div className="text-lg font-bold">Student Grievance Portal</div>
            <div className="text-xs text-slate-500">Transparent • Fast • Accountable</div>
          </div>
        </div>

        <nav className="flex items-center gap-4">
          <Link to="/" className="text-slate-700 hover:text-slate-900 text-sm">Home</Link>
          {user && (
            <>
              <Link to="/submit" className="text-slate-700 hover:text-slate-900 text-sm">Submit</Link>
              <Link to="/dashboard" className="text-slate-700 hover:text-slate-900 text-sm">My Grievances</Link>
              {user.is_admin && (
                <Link to="/admin" className="text-slate-700 hover:text-slate-900 text-sm font-semibold">Admin</Link>
              )}
            </>
          )}

          {user ? (
            <div className="flex items-center gap-3">
              <span className="text-sm text-slate-600">{user.email}</span>
              <button
                onClick={handleLogout}
                className="px-3 py-1 bg-red-50 text-red-600 rounded text-sm hover:bg-red-100"
              >
                Logout
              </button>
            </div>
          ) : (
            <Link to="/login" className="px-3 py-1 bg-sky-600 text-white rounded text-sm hover:bg-sky-700">
              Login
            </Link>
          )}
        </nav>
      </div>
    </header>
  )
}
