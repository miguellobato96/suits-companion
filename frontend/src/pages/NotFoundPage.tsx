import { Link } from 'react-router'

function NotFoundPage() {
  return (
    <main className="mx-auto max-w-3xl px-4 py-10 sm:px-6 lg:px-8">
      <p className="text-sm font-semibold tracking-[0.14em] text-brand-soft uppercase">
        404
      </p>

      <h1 className="mt-2 font-display text-3xl font-bold text-ink">
        Page not found
      </h1>

      <p className="mt-3 text-muted">
        The page you are looking for does not exist.
      </p>

      <Link
        className="mt-6 inline-flex min-h-11 items-center rounded-xl border border-line bg-panel px-4 text-sm font-medium text-ink transition-colors hover:bg-panel-hover focus-visible:ring-2 focus-visible:ring-brand focus-visible:outline-none"
        to="/"
      >
        Back to references
      </Link>
    </main>
  )
}

export default NotFoundPage
