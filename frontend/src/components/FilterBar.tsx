import type { Character, Franchise } from '../types/api'

type FilterBarProps = {
  characters: Character[]
  franchises: Franchise[]
  characterId: number | null
  franchiseId: number | null
  onCharacterChange: (id: number | null) => void
  onFranchiseChange: (id: number | null) => void
}

function FilterBar({
  characters,
  franchises,
  characterId,
  franchiseId,
  onCharacterChange,
  onFranchiseChange,
}: FilterBarProps) {
  return (
    <div className="mb-6 grid gap-3 sm:grid-cols-2">
      <select
        className="rounded-lg border border-slate-700 bg-slate-900 px-4 py-2 text-slate-200"
        value={characterId ?? ''}
        onChange={(event) =>
          onCharacterChange(
            event.target.value ? Number(event.target.value) : null,
          )
        }
      >
        <option value="">All characters</option>

        {characters.map((character) => (
          <option key={character.id} value={character.id}>
            {character.name}
          </option>
        ))}
      </select>

      <select
        className="rounded-lg border border-slate-700 bg-slate-900 px-4 py-2 text-slate-200"
        value={franchiseId ?? ''}
        onChange={(event) =>
          onFranchiseChange(
            event.target.value ? Number(event.target.value) : null,
          )
        }
      >
        <option value="">All franchises</option>

        {franchises.map((franchise) => (
          <option key={franchise.id} value={franchise.id}>
            {franchise.name}
          </option>
        ))}
      </select>
    </div>
  )
}

export default FilterBar
