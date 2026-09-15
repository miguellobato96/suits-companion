import { useEffect, useState } from 'react'
import { Link, useLocation, useParams } from 'react-router'

import { getReference } from '../../api/references'
import type { Reference } from '../../types/api'

type ReferenceLoadResult = {
  referenceId: number
  reference: Reference | null
  status: 'success' | 'not-found' | 'error'
}

function ReferenceDetails() {
  const { id } = useParams()
  const location = useLocation()
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

  const backToReferences = {
    pathname: '/',
    search: location.search,
  }

  if (isInvalidReferenceId) {
    return (
      <main className="mx-auto max-w-3xl px-4 py-10 sm:px-6 lg:px-8">
        <p className="text-sm font-semibold tracking-[0.14em] text-brand-soft uppercase">
          404
        </p>

        <h1 className="mt-2 font-display text-3xl font-bold text-ink">
          Reference not found
        </h1>

        <p className="mt-3 text-muted">
          The reference you are looking for does not exist.
        </p>

        <Link
          className="mt-6 inline-flex min-h-11 items-center rounded-xl border border-line bg-panel px-4 text-sm font-medium text-ink transition-colors hover:bg-panel-hover focus-visible:ring-2 focus-visible:ring-brand focus-visible:outline-none"
          to={backToReferences}
        >
          Back to references
        </Link>
      </main>
    )
  }

  if (result === null || result.referenceId !== referenceId) {
    return (
      <main className="mx-auto max-w-3xl px-4 py-10 sm:px-6 lg:px-8">
        <p className="text-muted">Loading reference...</p>
      </main>
    )
  }

  if (result.status === 'error') {
    return (
      <main className="mx-auto max-w-3xl px-4 py-10 sm:px-6 lg:px-8">
        <p className="text-red-400">Failed to load reference.</p>
      </main>
    )
  }

  if (result.status === 'not-found' || result.reference === null) {
    return (
      <main className="mx-auto max-w-3xl px-4 py-10 sm:px-6 lg:px-8">
        <p className="text-sm font-semibold tracking-[0.14em] text-brand-soft uppercase">
          404
        </p>

        <h1 className="mt-2 font-display text-3xl font-bold text-ink">
          Reference not found
        </h1>

        <p className="mt-3 text-muted">
          The reference you are looking for does not exist.
        </p>

        <Link
          className="mt-6 inline-flex min-h-11 items-center rounded-xl border border-line bg-panel px-4 text-sm font-medium text-ink transition-colors hover:bg-panel-hover focus-visible:ring-2 focus-visible:ring-brand focus-visible:outline-none"
          to={backToReferences}
        >
          Back to references
        </Link>
      </main>
    )
  }

  const reference = result.reference

  return (
    <main className="mx-auto max-w-3xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
      <Link
        className="inline-flex min-h-11 items-center text-sm font-medium text-muted transition-colors hover:text-ink focus-visible:ring-2 focus-visible:ring-brand focus-visible:outline-none"
        to={backToReferences}
      >
        ← Back to references
      </Link>

      <article className="mt-4 overflow-hidden rounded-2xl border border-line bg-panel">
        <div className="border-b border-line px-5 py-6 sm:px-8 sm:py-8">
          <div className="flex items-start justify-between gap-4">
            <div className="min-w-0">
              <p className="mb-2 text-xs font-semibold tracking-[0.14em] text-brand-soft uppercase">
                {reference.reference_type}
              </p>

              <h1 className="font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
                {reference.title}
              </h1>

              {reference.spoken_by_character && (
                <p className="mt-3 text-sm text-muted">
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
            <blockquote className="mt-7 border-l-2 border-brand pl-4 font-display text-lg leading-8 text-ink italic sm:text-xl">
              “{reference.quote}”
            </blockquote>
          )}
        </div>

        <div className="space-y-8 px-5 py-6 sm:px-8 sm:py-8">
          <section>
            <h2 className="font-display text-xl font-bold text-ink">Context</h2>

            <p className="mt-3 leading-7 text-muted">{reference.context}</p>
          </section>

          {reference.media.length > 0 && (
            <section className="border-t border-line pt-8">
              <h2 className="font-display text-xl font-bold text-ink">
                Referenced media
              </h2>

              <ul className="mt-4 space-y-3">
                {reference.media.map((media) => (
                  <li
                    key={media.id}
                    className="rounded-xl bg-canvas/40 px-4 py-3 text-muted"
                  >
                    <span className="font-medium text-ink">{media.title}</span>

                    {media.release_year && (
                      <span className="ml-2">({media.release_year})</span>
                    )}
                  </li>
                ))}
              </ul>
            </section>
          )}

          {reference.franchises.length > 0 && (
            <section className="border-t border-line pt-8">
              <h2 className="font-display text-xl font-bold text-ink">
                Franchises
              </h2>

              <div className="mt-4 flex flex-wrap gap-2">
                {reference.franchises.map((franchise) => (
                  <span
                    key={franchise.id}
                    className="rounded-full border border-line bg-canvas/40 px-3 py-1.5 text-sm text-muted"
                  >
                    {franchise.name}
                  </span>
                ))}
              </div>
            </section>
          )}
        </div>
      </article>
    </main>
  )
}

export default ReferenceDetails
