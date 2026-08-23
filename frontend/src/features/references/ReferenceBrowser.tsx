import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router'

import { getCharacters } from '../../api/characters'
import { getFranchises } from '../../api/franchises'
import { getReferences } from '../../api/references'
import type { Character, Franchise, Reference } from '../../types/api'
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
  const [characters, setCharacters] = useState<Character[]>([])
  const [franchises, setFranchises] = useState<Franchise[]>([])

  const [total, setTotal] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadFilters() {
      try {
        const [characterData, franchiseData] = await Promise.all([
          getCharacters(),
          getFranchises(),
        ])

        setCharacters(characterData.items)
        setFranchises(franchiseData)
      } catch {
        setError('Failed to load filters.')
      }
    }

    loadFilters()
  }, [])

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
  }, [debouncedSearch, characterId, franchiseId, offset])

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

  return (
    <main className="mx-auto max-w-7xl px-6 py-8">
      <SearchBar value={searchInput} onChange={handleSearchChange} />

      <FilterBar
        characters={characters}
        franchises={franchises}
        characterId={characterId}
        franchiseId={franchiseId}
        onCharacterChange={handleCharacterChange}
        onFranchiseChange={handleFranchiseChange}
      />

      {isLoading && references.length === 0 && (
        <p className="text-slate-400">Loading references...</p>
      )}

      {error && <p className="text-red-400">{error}</p>}

      {!isLoading && !error && references.length === 0 && (
        <p className="text-slate-400">No references found.</p>
      )}

      {!error && references.length > 0 && (
        <>
          {isLoading && (
            <p className="mb-3 text-sm text-slate-500">Updating results...</p>
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
    </main>
  )
}

export default ReferenceBrowser
