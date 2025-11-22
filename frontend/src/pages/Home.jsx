import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <main className="max-w-6xl mx-auto px-4 py-12">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="col-span-2 bg-white p-6 rounded-lg shadow-sm">
          <h1 className="text-3xl font-bold mb-2">Welcome to the Student Grievance Portal</h1>
          <p className="text-slate-600 mb-4">Submit grievances, track their status, and get transparent updates from the concerned departments.</p>
          <div className="flex gap-3">
            <Link to="/submit" className="px-4 py-2 bg-sky-600 text-white rounded hover:bg-sky-700">
              Submit a Grievance
            </Link>
            <Link to="/dashboard" className="px-4 py-2 border rounded hover:bg-slate-50">
              View your Grievances
            </Link>
          </div>
        </div>

        <aside className="bg-white p-6 rounded-lg shadow-sm">
          <h3 className="font-semibold mb-3">Quick Stats</h3>
          <ul className="text-sm text-slate-600 space-y-3">
            <li>
              <div className="text-xs text-slate-400">Open grievances</div>
              <div className="text-2xl font-bold text-sky-600">12</div>
            </li>
            <li>
              <div className="text-xs text-slate-400">Avg resolution</div>
              <div className="text-2xl font-bold text-sky-600">3.2d</div>
            </li>
            <li>
              <div className="text-xs text-slate-400">Departments</div>
              <div className="text-2xl font-bold text-sky-600">7</div>
            </li>
          </ul>
        </aside>
      </div>

      <section className="mt-8 bg-white p-6 rounded-lg shadow-sm">
        <h2 className="text-2xl font-semibold mb-4">How it works</h2>
        <ol className="list-decimal list-inside text-slate-600 space-y-2 max-w-2xl">
          <li><strong>Register</strong> with your college email and create an account.</li>
          <li><strong>Submit</strong> your grievance with category, description, and optional attachments.</li>
          <li><strong>Track</strong> status in real-time and receive email notifications at each update.</li>
          <li><strong>Resolve</strong> — Get feedback and resolution from the concerned department.</li>
        </ol>
      </section>
    </main>
  )
}
