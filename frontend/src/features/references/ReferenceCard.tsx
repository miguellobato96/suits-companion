import { Link, useLocation } from 'react-router'

import type { Reference } from '../../types/api'

type ReferenceCardProps = {
  reference: Reference
}

function ReferenceCard({ reference }: ReferenceCardProps) {
  const location = useLocation()

  return (
    <Link
      className="group block rounded-2xl focus-visible:ring-2 focus-visible:ring-brand focus-visible:ring-offset-4 focus-visible:ring-offset-canvas focus-visible:outline-none"
      to={{
        pathname: `/references/${reference.id}`,
        search: location.search,
      }}
    >
      <article className="relative overflow-hidden rounded-2xl border border-line bg-panel p-5 transition duration-200 group-hover:-translate-y-0.5 group-hover:border-brand/60 group-hover:bg-panel-hover sm:p-6">
        <span
          className="absolute top-0 left-0 h-full w-1 bg-brand opacity-0 transition-opacity group-hover:opacity-100"
          aria-hidden="true"
        />

        <div className="flex items-start justify-between gap-4">
          <div className="min-w-0">
            <p className="mb-2 text-xs font-semibold tracking-[0.14em] text-brand-soft uppercase">
              {reference.reference_type}
            </p>

            <h2 className="font-display text-xl font-bold tracking-tight text-ink sm:text-2xl">
              {reference.title}
            </h2>

            {reference.spoken_by_character && (
              <p className="mt-1.5 text-sm text-muted">
                {reference.spoken_by_character.name}
              </p>
            )}
          </div>

          {reference.season && reference.episode && (
            <span className="shrink-0 rounded-lg border border-line bg-canvas/40 px-2.5 py-1.5 text-xs font-medium text-muted">
              S{reference.season.toString().padStart(2, '0')}E
              {reference.episode.toString().padStart(2, '0')}
            </span>
          )}
        </div>

        {reference.quote && (
          <blockquote className="mt-5 border-l-2 border-brand/70 pl-4 font-display text-base leading-7 text-ink italic">
            “{reference.quote}”
          </blockquote>
        )}

        <p className="mt-5 line-clamp-3 text-sm leading-6 text-muted">
          {reference.context}
        </p>

        <div className="mt-5 flex items-center justify-between border-t border-line pt-4">
          <div className="flex flex-wrap gap-2">
            {reference.franchises.slice(0, 2).map((franchise) => (
              <span
                key={franchise.id}
                className="rounded-full bg-canvas/50 px-2.5 py-1 text-xs text-muted"
              >
                {franchise.name}
              </span>
            ))}
          </div>

          <span className="ml-4 shrink-0 text-sm font-medium text-brand-soft transition-colors group-hover:text-ink">
            View reference
          </span>
        </div>
      </article>
    </Link>
  )
}

export default ReferenceCard
