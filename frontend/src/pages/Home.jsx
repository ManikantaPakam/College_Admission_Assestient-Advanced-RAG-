import { Link } from 'react-router'

function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 px-4">

      <div className="w-full max-w-xl rounded-2xl bg-white p-10 text-center shadow-xl">

        <h1 className="text-3xl font-bold text-blue-600">
          College Admission Assistant
        </h1>

        <p className="mt-4 text-gray-600">
          React + FastAPI + Advanced RAG Application
        </p>

        <Link
          to="/login"
          className="mt-6 inline-block rounded-lg bg-blue-600 px-8 py-3 text-white hover:bg-blue-700"
        >
          Get Started
        </Link>

      </div>

    </div>
  )
}

export default Home