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
    <div className="mt-6 flex items-center justify-between">
      <p className="text-sm text-slate-400">
        Showing {start}–{end} of {total}
      </p>

      <div className="flex gap-2">
        <button
          className="rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-200 disabled:cursor-not-allowed disabled:opacity-40"
          type="button"
          disabled={offset === 0}
          onClick={onPrevious}
        >
          Previous
        </button>

        <button
          className="rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-200 disabled:cursor-not-allowed disabled:opacity-40"
          type="button"
          disabled={offset + limit >= total}
          onClick={onNext}
        >
          Next
        </button>
      </div>
    </div>
  )
}

export default Pagination
