import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router'

import { getReference } from '../../api/references'
import type { Reference } from '../../types/api'

type ReferenceLoadResult = {
  referenceId: number
  reference: Reference | null
  status: 'success' | 'not-found' | 'error'
}

function ReferenceDetails() {
  const { id } = useParams()
  const referenceId = Number(id)

  const isInvalidReferenceId =
    !Number.isInteger(referenceId) || referenceId <= 0

  const [result, setResult] = useState<ReferenceLoadResult | null>(null)

  useEffect(() => {
    if (isInvalidReferenceId) {
      return
    }

    const controller = new AbortController()

    async function loadReference() {
      try {
        const data = await getReference(referenceId, controller.signal)

        if (controller.signal.aborted) {
          return
        }

        if (data === null) {
          setResult({
            referenceId,
            reference: null,
            status: 'not-found',
          })

          return
        }

        setResult({
          referenceId,
          reference: data,
          status: 'success',
        })
      } catch {
        if (!controller.signal.aborted) {
          setResult({
            referenceId,
            reference: null,
            status: 'error',
          })
        }
      }
    }

    loadReference()

    return () => {
      controller.abort()
    }
  }, [isInvalidReferenceId, referenceId])

  if (isInvalidReferenceId) {
    return (
      <main className="mx-auto max-w-3xl px-6 py-8">
        <h1 className="text-2xl font-bold text-slate-100">
          Reference not found
        </h1>

        <p className="mt-2 text-slate-400">
          The reference you are looking for does not exist.
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

  if (result === null || result.referenceId !== referenceId) {
    return (
      <main className="mx-auto max-w-3xl px-6 py-8">
        <p className="text-slate-400">Loading reference...</p>
      </main>
    )
  }

  if (result.status === 'error') {
    return (
      <main className="mx-auto max-w-3xl px-6 py-8">
        <p className="text-red-400">Failed to load reference.</p>
      </main>
    )
  }

  if (result.status === 'not-found' || result.reference === null) {
    return (
      <main className="mx-auto max-w-3xl px-6 py-8">
        <h1 className="text-2xl font-bold text-slate-100">
          Reference not found
        </h1>

        <p className="mt-2 text-slate-400">
          The reference you are looking for does not exist.
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

  const reference = result.reference

  return (
    <main className="mx-auto max-w-3xl px-6 py-8">
      <Link className="text-sm text-slate-400 hover:text-slate-200" to="/">
        ← Back to references
      </Link>

      <article className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-100">
              {reference.title}
            </h1>

            {reference.spoken_by_character && (
              <p className="mt-2 text-sm text-slate-400">
                {reference.spoken_by_character.name}
              </p>
            )}
          </div>

          {reference.season && reference.episode && (
            <span className="shrink-0 rounded-md bg-slate-800 px-2 py-1 text-xs text-slate-300">
              S{reference.season.toString().padStart(2, '0')}E
              {reference.episode.toString().padStart(2, '0')}
            </span>
          )}
        </div>

        {reference.quote && (
          <blockquote className="mt-6 border-l-2 border-slate-700 pl-4 text-slate-300 italic">
            “{reference.quote}”
          </blockquote>
        )}

        <section className="mt-8">
          <h2 className="text-lg font-semibold text-slate-100">Context</h2>

          <p className="mt-2 leading-7 text-slate-400">{reference.context}</p>
        </section>

        {reference.media.length > 0 && (
          <section className="mt-8">
            <h2 className="text-lg font-semibold text-slate-100">
              Referenced media
            </h2>

            <ul className="mt-3 space-y-2">
              {reference.media.map((media) => (
                <li key={media.id} className="text-slate-400">
                  <span className="text-slate-200">{media.title}</span>

                  {media.release_year && (
                    <span className="ml-2">({media.release_year})</span>
                  )}
                </li>
              ))}
            </ul>
          </section>
        )}

        {reference.franchises.length > 0 && (
          <section className="mt-8">
            <h2 className="text-lg font-semibold text-slate-100">Franchises</h2>

            <div className="mt-3 flex flex-wrap gap-2">
              {reference.franchises.map((franchise) => (
                <span
                  key={franchise.id}
                  className="rounded-md bg-slate-800 px-3 py-1 text-sm text-slate-300"
                >
                  {franchise.name}
                </span>
              ))}
            </div>
          </section>
        )}
      </article>
    </main>
  )
}

export default ReferenceDetails
