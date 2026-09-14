import { Search, X } from 'lucide-react'

type SearchBarProps = {
  value: string
  onChange: (value: string) => void
}

function SearchBar({ value, onChange }: SearchBarProps) {
  return (
    <div className="relative">
      <label className="sr-only" htmlFor="reference-search">
        Search references
      </label>

      <Search
        className="pointer-events-none absolute top-1/2 left-4 -translate-y-1/2 text-muted"
        size={18}
        aria-hidden="true"
      />

      <input
        id="reference-search"
        className="min-h-12 w-full appearance-none rounded-xl border border-line bg-panel px-11 pr-12 text-ink transition-colors placeholder:text-muted focus:border-brand focus:ring-4 focus:ring-brand/10 focus:outline-none"
        type="search"
        placeholder="Search references..."
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />

      {value && (
        <button
          className="absolute top-1/2 right-2 flex min-h-10 min-w-10 -translate-y-1/2 items-center justify-center rounded-lg text-muted transition-colors hover:bg-panel-hover hover:text-ink focus-visible:ring-2 focus-visible:ring-brand focus-visible:outline-none"
          type="button"
          aria-label="Clear search"
          onClick={() => onChange('')}
        >
          <X size={18} aria-hidden="true" />
        </button>
      )}
    </div>
  )
}

export default SearchBar
