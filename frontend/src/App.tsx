import { useEffect, useState } from 'react'

import { getCharacters } from './api/characters'
import { getFranchises } from './api/franchises'
import { getReferences } from './api/references'
import FilterBar from './components/FilterBar'
import Header from './components/Header'
import Pagination from './components/Pagination'
import ReferenceCard from './components/ReferenceCard'
import SearchBar from './components/SearchBar'
import type { Character, Franchise, Reference } from './types/api'

const PAGE_SIZE = 20
const SEARCH_DEBOUNCE_MS = 300

function App() {
  const [references, setReferences] = useState<Reference[]>([])
  const [characters, setCharacters] = useState<Character[]>([])
  const [franchises, setFranchises] = useState<Franchise[]>([])

  const [searchInput, setSearchInput] = useState('')
  const [searchQuery, setSearchQuery] = useState('')
  const [characterId, setCharacterId] = useState<number | null>(null)
  const [franchiseId, setFranchiseId] = useState<number | null>(null)

  const [total, setTotal] = useState(0)
  const [offset, setOffset] = useState(0)

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
      setSearchQuery(searchInput.trim())
      setOffset(0)
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
          search: searchQuery,
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
  }, [searchQuery, characterId, franchiseId, offset])

  function handleCharacterChange(id: number | null) {
    setCharacterId(id)
    setOffset(0)
  }

  function handleFranchiseChange(id: number | null) {
    setFranchiseId(id)
    setOffset(0)
  }

  function handlePrevious() {
    setOffset((currentOffset) => Math.max(0, currentOffset - PAGE_SIZE))
  }

  function handleNext() {
    setOffset((currentOffset) => currentOffset + PAGE_SIZE)
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <Header />

      <main className="mx-auto max-w-7xl px-6 py-8">
        <SearchBar value={searchInput} onChange={setSearchInput} />

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
    </div>
  )
}

export default App
