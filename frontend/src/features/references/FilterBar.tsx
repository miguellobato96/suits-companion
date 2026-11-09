import type { FilterOption } from '../../types/api'

type FilterBarProps = {
  characters: FilterOption[]
  franchises: FilterOption[]
  characterId: number | null
  franchiseId: number | null
  isUnavailable?: boolean
  onCharacterChange: (id: number | null) => void
  onFranchiseChange: (id: number | null) => void
}

function FilterBar({
  characters,
  franchises,
  characterId,
  franchiseId,
  isUnavailable = false,
  onCharacterChange,
  onFranchiseChange,
}: FilterBarProps) {
  const characterUnavailable = isUnavailable || characters.length === 0
  const franchiseUnavailable = isUnavailable || franchises.length === 0

  return (
    <div className="grid gap-4 sm:grid-cols-2">
      <label className="grid gap-2">
        <span className="text-sm font-medium text-muted">Character</span>

        <select
          className="min-h-12 w-full rounded-xl border border-line bg-panel px-4 text-ink transition-colors focus:border-muted focus:ring-2 focus:ring-ink/10 focus:outline-none disabled:cursor-not-allowed disabled:opacity-60"
          value={characterId ?? ''}
          disabled={characterUnavailable}
          onChange={(event) =>
            onCharacterChange(
              event.target.value ? Number(event.target.value) : null,
            )
          }
        >
          <option value="">
            {isUnavailable
              ? 'Characters unavailable'
              : characters.length === 0
                ? 'No characters available'
                : 'All characters'}
          </option>

          {characters.map((character) => (
            <option key={character.id} value={character.id}>
              {character.name} ({character.count})
            </option>
          ))}
        </select>
      </label>

      <label className="grid gap-2">
        <span className="text-sm font-medium text-muted">Franchise</span>

        <select
          className="min-h-12 w-full rounded-xl border border-line bg-panel px-4 text-ink transition-colors focus:border-muted focus:ring-2 focus:ring-ink/10 focus:outline-none disabled:cursor-not-allowed disabled:opacity-60"
          value={franchiseId ?? ''}
          disabled={franchiseUnavailable}
          onChange={(event) =>
            onFranchiseChange(
              event.target.value ? Number(event.target.value) : null,
            )
          }
        >
          <option value="">
            {isUnavailable
              ? 'Franchises unavailable'
              : franchises.length === 0
                ? 'No franchises available'
                : 'All franchises'}
          </option>

          {franchises.map((franchise) => (
            <option key={franchise.id} value={franchise.id}>
              {franchise.name} ({franchise.count})
            </option>
          ))}
        </select>
      </label>
    </div>
  )
}

export default FilterBar
