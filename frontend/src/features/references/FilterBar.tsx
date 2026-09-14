import type { Character, Franchise } from '../../types/api'

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
    <div className="grid gap-4 sm:grid-cols-2">
      <label className="grid gap-2">
        <span className="text-sm font-medium text-muted">Character</span>

        <select
          className="min-h-12 w-full rounded-xl border border-line bg-panel px-4 text-ink transition-colors focus:border-brand focus:ring-4 focus:ring-brand/10 focus:outline-none"
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
      </label>

      <label className="grid gap-2">
        <span className="text-sm font-medium text-muted">Franchise</span>

        <select
          className="min-h-12 w-full rounded-xl border border-line bg-panel px-4 text-ink transition-colors focus:border-brand focus:ring-4 focus:ring-brand/10 focus:outline-none"
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
      </label>
    </div>
  )
}

export default FilterBar
