import { RefreshCw } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router'

import { getReferenceFilterOptions, getReferences } from '../../api/references'
import type { Reference, ReferenceFilterOptionsResponse } from '../../types/api'
import FilterBar from './FilterBar'
import Pagination from './Pagination'
import ReferenceCard from './ReferenceCard'
import SearchBar from './SearchBar'

const PAGE_SIZE = 20
const SEARCH_DEBOUNCE_MS = 300

function parsePositiveInteger(value: string | null): number | null {
  if (value === null) {
    return null
  }

  const number = Number(value)

  return Number.isInteger(number) && number > 0 ? number : null
}

function parseOffset(value: string | null): number {
  if (value === null) {
    return 0
  }

  const number = Number(value)

  return Number.isInteger(number) && number >= 0 ? number : 0
}

function ReferenceBrowser() {
  const [searchParams, setSearchParams] = useSearchParams()

  const searchInput = searchParams.get('search') ?? ''
  const characterId = parsePositiveInteger(searchParams.get('character_id'))
  const franchiseId = parsePositiveInteger(searchParams.get('franchise_id'))
  const offset = parseOffset(searchParams.get('offset'))

  const [debouncedSearch, setDebouncedSearch] = useState(searchInput)

  const [references, setReferences] = useState<Reference[]>([])

  const [filterOptions, setFilterOptions] =
    useState<ReferenceFilterOptionsResponse>({
      characters: [],
      franchises: [],
    })

  const [filterError, setFilterError] = useState<string | null>(null)

  const [total, setTotal] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [retryKey, setRetryKey] = useState(0)

  useEffect(() => {
    const controller = new AbortController()

    async function loadFilterOptions() {
      setFilterError(null)

      try {
        const data = await getReferenceFilterOptions({
          search: debouncedSearch,
          characterId: characterId ?? undefined,
          franchiseId: franchiseId ?? undefined,
          signal: controller.signal,
        })

        setFilterOptions(data)
      } catch {
        if (!controller.signal.aborted) {
          setFilterError('Failed to load filter options.')
        }
      }
    }

    loadFilterOptions()

    return () => {
      controller.abort()
    }
  }, [debouncedSearch, characterId, franchiseId, retryKey])

  // Keep URL state immediate while debouncing only the API search request.
  useEffect(() => {
    const timeoutId = window.setTimeout(() => {
      setDebouncedSearch(searchInput.trim())
    }, SEARCH_DEBOUNCE_MS)

    return () => {
      window.clearTimeout(timeoutId)
    }
  }, [searchInput])

  useEffect(() => {
    const controller = new AbortController()

    async function loadReferences() {
      setIsLoading(true)
      setError(null)

      try {
        const data = await getReferences({
          search: debouncedSearch,
          characterId: characterId ?? undefined,
          franchiseId: franchiseId ?? undefined,
          offset,
          limit: PAGE_SIZE,
          signal: controller.signal,
        })

        setReferences(data.items)
        setTotal(data.total)
      } catch {
        if (!controller.signal.aborted) {
          setError('Failed to load references.')
        }
      } finally {
        if (!controller.signal.aborted) {
          setIsLoading(false)
        }
      }
    }

    loadReferences()

    return () => {
      controller.abort()
    }
  }, [debouncedSearch, characterId, franchiseId, offset, retryKey])

  function handleSearchChange(value: string) {
    setSearchParams(
      (currentParams) => {
        const nextParams = new URLSearchParams(currentParams)

        if (value) {
          nextParams.set('search', value)
        } else {
          nextParams.delete('search')
        }

        nextParams.delete('offset')

        return nextParams
      },
      { replace: true },
    )
  }

  function handleCharacterChange(id: number | null) {
    setSearchParams((currentParams) => {
      const nextParams = new URLSearchParams(currentParams)

      if (id !== null) {
        nextParams.set('character_id', id.toString())
      } else {
        nextParams.delete('character_id')
      }

      nextParams.delete('offset')

      return nextParams
    })
  }

  function handleFranchiseChange(id: number | null) {
    setSearchParams((currentParams) => {
      const nextParams = new URLSearchParams(currentParams)

      if (id !== null) {
        nextParams.set('franchise_id', id.toString())
      } else {
        nextParams.delete('franchise_id')
      }

      nextParams.delete('offset')

      return nextParams
    })
  }

  function handlePrevious() {
    const previousOffset = Math.max(0, offset - PAGE_SIZE)

    setSearchParams((currentParams) => {
      const nextParams = new URLSearchParams(currentParams)

      if (previousOffset === 0) {
        nextParams.delete('offset')
      } else {
        nextParams.set('offset', previousOffset.toString())
      }

      return nextParams
    })
  }

  function handleNext() {
    setSearchParams((currentParams) => {
      const nextParams = new URLSearchParams(currentParams)

      nextParams.set('offset', (offset + PAGE_SIZE).toString())

      return nextParams
    })
  }

  function handleRetry() {
    setRetryKey((current) => current + 1)
  }

  const hasReferenceError = error !== null

  return (
    <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
      <section
        className="mb-8 grid gap-4"
        aria-label="Search and filter references"
      >
        <SearchBar value={searchInput} onChange={handleSearchChange} />

        <FilterBar
          characters={filterOptions.characters}
          franchises={filterOptions.franchises}
          characterId={characterId}
          franchiseId={franchiseId}
          isUnavailable={
            filterError !== null && filterOptions.characters.length === 0
          }
          onCharacterChange={handleCharacterChange}
          onFranchiseChange={handleFranchiseChange}
        />
      </section>

      {hasReferenceError ? (
        <section
          className="rounded-2xl border border-line bg-panel px-5 py-8 sm:px-8"
          role="alert"
        >
          <p className="text-xs font-semibold tracking-[0.14em] text-brand-soft uppercase">
            Connection error
          </p>

          <h1 className="mt-2 font-display text-2xl font-bold text-ink">
            Unable to load references
          </h1>

          <p className="mt-3 max-w-xl leading-7 text-muted">
            Something went wrong while loading the references. Check your
            connection and try again.
          </p>

          <button
            className="mt-6 inline-flex min-h-11 items-center gap-2 rounded-xl border border-line bg-canvas/40 px-4 text-sm font-medium text-ink transition-colors hover:bg-panel-hover focus-visible:ring-2 focus-visible:ring-brand focus-visible:outline-none"
            type="button"
            onClick={handleRetry}
          >
            <RefreshCw size={16} aria-hidden="true" />
            Try again
          </button>
        </section>
      ) : (
        <>
          {filterError && (
            <p className="mb-6 text-sm text-red-400" role="alert">
              Filter options are temporarily unavailable.
            </p>
          )}

          {isLoading && references.length === 0 && (
            <p className="text-muted" role="status">
              Loading references...
            </p>
          )}

          {!isLoading && references.length === 0 && (
            <section className="rounded-2xl border border-line bg-panel px-5 py-8 sm:px-8">
              <p className="text-xs font-semibold tracking-[0.14em] text-brand-soft uppercase">
                No results
              </p>

              <h2 className="mt-2 font-display text-2xl font-bold text-ink">
                No references found
              </h2>

              <p className="mt-3 text-muted">
                Try changing your search or removing one of the filters.
              </p>
            </section>
          )}

          {references.length > 0 && (
            <>
              {isLoading && (
                <p className="mb-3 text-sm text-muted" role="status">
                  Updating results...
                </p>
              )}

              <div className="grid gap-4">
                {references.map((reference) => (
                  <ReferenceCard key={reference.id} reference={reference} />
                ))}
              </div>

              <Pagination
                total={total}
                offset={offset}
                limit={PAGE_SIZE}
                onPrevious={handlePrevious}
                onNext={handleNext}
              />
            </>
          )}
        </>
      )}
    </main>
  )
}

export default ReferenceBrowser
