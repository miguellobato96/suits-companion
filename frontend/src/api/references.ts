import type { Reference, ReferenceListResponse } from '../types/api'

type GetReferencesParams = {
  search?: string
  characterId?: number
  franchiseId?: number
  offset?: number
  limit?: number
  signal?: AbortSignal
}

export async function getReferences({
  search,
  characterId,
  franchiseId,
  offset = 0,
  limit = 20,
  signal,
}: GetReferencesParams = {}): Promise<ReferenceListResponse> {
  const params = new URLSearchParams()

  if (search) {
    params.set('search', search)
  }

  if (characterId) {
    params.set('character_id', characterId.toString())
  }

  if (franchiseId) {
    params.set('franchise_id', franchiseId.toString())
  }

  params.set('offset', offset.toString())
  params.set('limit', limit.toString())

  const response = await fetch(`/api/references/?${params.toString()}`, {
    signal,
  })

  if (!response.ok) {
    throw new Error('Failed to fetch references')
  }

  return response.json()
}

export async function getReference(
  id: number,
  signal?: AbortSignal,
): Promise<Reference | null> {
  const response = await fetch(`/api/references/${id}`, {
    signal,
  })

  if (response.status === 404) {
    return null
  }

  if (!response.ok) {
    throw new Error('Failed to fetch reference')
  }

  return response.json()
}
