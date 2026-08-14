import { Link } from 'react-router'

function Header() {
  return (
    <header className="border-b border-slate-800 bg-slate-950">
      <div className="mx-auto max-w-7xl px-6 py-6">
        <Link to="/">
          <h1 className="text-2xl font-bold text-slate-100">Suits Companion</h1>
        </Link>

        <p className="mt-1 text-sm text-slate-400">
          Discover the cultural references behind Suits.
        </p>
      </div>
    </header>
  )
}

export default Header
