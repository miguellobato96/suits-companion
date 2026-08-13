import type { CharacterListResponse } from '../types/api'

export async function getCharacters(): Promise<CharacterListResponse> {
  const response = await fetch('/api/characters/')

  if (!response.ok) {
    throw new Error('Failed to fetch characters')
  }

  return response.json()
}
