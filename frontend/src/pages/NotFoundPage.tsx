import { Link } from 'react-router'

function NotFoundPage() {
  return (
    <main className="mx-auto max-w-7xl px-6 py-16">
      <h1 className="text-3xl font-bold text-slate-100">Page not found</h1>

      <p className="mt-2 text-slate-400">
        The page you are looking for does not exist.
      </p>

      <Link
        className="mt-6 inline-block text-slate-200 underline underline-offset-4"
        to="/"
      >
        Back to references
      </Link>
    </main>
  )
}

export default NotFoundPage
