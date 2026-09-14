import { ChevronLeft, ChevronRight } from 'lucide-react'

type PaginationProps = {
  total: number
  offset: number
  limit: number
  onPrevious: () => void
  onNext: () => void
}

function Pagination({
  total,
  offset,
  limit,
  onPrevious,
  onNext,
}: PaginationProps) {
  if (total === 0) {
    return null
  }

  const start = offset + 1
  const end = Math.min(offset + limit, total)

  return (
    <div className="mt-8 flex flex-col gap-4 border-t border-line pt-5 sm:flex-row sm:items-center sm:justify-between">
      <p className="text-sm text-muted">
        Showing {start}–{end} of {total}
      </p>

      <div className="grid grid-cols-2 gap-2 sm:flex">
        <button
          className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl border border-line bg-panel px-4 text-sm font-medium text-ink transition-colors hover:bg-panel-hover disabled:cursor-not-allowed disabled:opacity-40"
          type="button"
          disabled={offset === 0}
          onClick={onPrevious}
        >
          <ChevronLeft size={16} aria-hidden="true" />
          Previous
        </button>

        <button
          className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl border border-line bg-panel px-4 text-sm font-medium text-ink transition-colors hover:bg-panel-hover disabled:cursor-not-allowed disabled:opacity-40"
          type="button"
          disabled={offset + limit >= total}
          onClick={onNext}
        >
          Next
          <ChevronRight size={16} aria-hidden="true" />
        </button>
      </div>
    </div>
  )
}

export default Pagination
