import type { Reference } from '../../types/api'

type ReferenceCardProps = {
  reference: Reference
}

function ReferenceCard({ reference }: ReferenceCardProps) {
  return (
    <article className="rounded-xl border border-slate-800 bg-slate-900 p-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold text-slate-100">
            {reference.title}
          </h2>

          {reference.spoken_by_character && (
            <p className="mt-1 text-sm text-slate-400">
              {reference.spoken_by_character.name}
            </p>
          )}
        </div>

        {reference.season && reference.episode && (
          <span className="rounded-md bg-slate-800 px-2 py-1 text-xs text-slate-300">
            S{reference.season.toString().padStart(2, '0')}E
            {reference.episode.toString().padStart(2, '0')}
          </span>
        )}
      </div>

      {reference.quote && (
        <blockquote className="mt-4 border-l-2 border-slate-700 pl-4 text-sm text-slate-300 italic">
          “{reference.quote}”
        </blockquote>
      )}

      <p className="mt-4 text-sm leading-6 text-slate-400">
        {reference.context}
      </p>
    </article>
  )
}

export default ReferenceCard
