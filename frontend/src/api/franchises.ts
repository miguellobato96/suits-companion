import type { Franchise } from '../types/api'

export async function getFranchises(): Promise<Franchise[]> {
  const response = await fetch('/api/franchises/')

  if (!response.ok) {
    throw new Error('Failed to fetch franchises')
  }

  return response.json()
}
