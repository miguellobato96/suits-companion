export type Character = {
  id: number
  name: string
  role: string | null
}

export type CharacterListResponse = {
  items: Character[]
  total: number
  offset: number
  limit: number
}

export type Franchise = {
  id: number
  name: string
}

export type Media = {
  id: number
  title: string
  media_type: string
  release_year: number | null
  franchises: Franchise[]
}

export type Reference = {
  id: number
  title: string
  reference_type: string
  season: number | null
  episode: number | null
  quote: string | null
  context: string
  spoken_by_character: Character | null
  media: Media[]
  franchises: Franchise[]
}

export type ReferenceListResponse = {
  items: Reference[]
  total: number
  offset: number
  limit: number
}
