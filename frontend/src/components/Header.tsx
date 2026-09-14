import { Link } from 'react-router'

function Header() {
  return (
    <header className="border-b border-line bg-canvas">
      <div className="mx-auto max-w-7xl px-4 py-5 sm:px-6 lg:px-8">
        <Link
          className="group inline-flex items-center gap-3 rounded-lg focus-visible:ring-2 focus-visible:ring-brand focus-visible:ring-offset-4 focus-visible:ring-offset-canvas focus-visible:outline-none"
          to="/"
          aria-label="Suits Companion home"
        >
          <span
            className="h-9 w-1 rounded-full bg-brand transition-colors group-hover:bg-brand-hover"
            aria-hidden="true"
          />

          <span>
            <span className="block font-display text-2xl font-bold tracking-tight text-ink sm:text-3xl">
              Suits Companion
            </span>

            <span className="mt-0.5 block text-xs text-muted sm:text-sm">
              Discover the cultural references behind Suits.
            </span>
          </span>
        </Link>
      </div>
    </header>
  )
}

export default Header
