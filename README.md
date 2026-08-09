# Suits Companion

Suits Companion is a companion application for discovering and exploring the cultural references made throughout the TV series *Suits*.

The series is packed with references to movies, TV shows, fictional characters, books, people, music, and pop culture. Some are obvious if you know the source material; others can easily go unnoticed.

The current MVP provides a REST API that turns those references into structured, searchable data.

## Why I Built This

*Suits* is my favorite TV series. I have watched and rewatched it more than ten times, to the point where I know many scenes and lines by heart.

And yet, every time I watch it again, I still notice something new.

Sometimes I recognize a reference immediately. Sometimes I know that a character is referencing something but have never seen the movie or show behind it. Other times, a reference goes completely over my head because I did not even realize there was one.

That is where the idea for Suits Companion came from.

I wanted a way to understand a little more of the show with every rewatch: where its references come from, what they mean, and how they fit into the conversation.

I figured other *Suits* fans might be in the same position — wanting to catch more of those references and revisit the series with a slightly different perspective each time.

Every rewatch can be a slightly different journey.

## Current MVP

The current MVP focuses on the backend and a curated **Season 1** dataset containing:

- 37 cultural references
- 12 *Suits* characters
- 33 referenced media works
- 10 franchises

The backend currently supports:

- browsing cultural references
- free-text search across titles, quotes, and context
- filtering by reference type, character, and franchise
- combined filters and pagination
- structured relationships between references, media, and franchises
- PostgreSQL persistence and database migrations
- idempotent seed scripts
- automated tests
- Docker-based development
- linting and formatting
- Continuous Integration configuration

The dataset is intentionally limited for the MVP and can be expanded progressively as the project develops.

## How References Are Structured

References are modeled separately from the media and franchises they refer to.

For example:

```text
Michael Keaton's Batman
├── Season 1, Episode 1
├── Mike Ross
├── Media
│   ├── Batman (1989)
│   └── Batman Returns (1992)
└── Franchise
    └── Batman
```

This means filtering by the **Batman** franchise can also find references such as `Wayne Manor`, even when the word "Batman" does not appear in the reference itself.

A reference can point to one or more specific works, directly to a franchise, or to both.

## Tech Stack

**Backend**

- Python 3.12
- FastAPI
- SQLAlchemy 2
- Pydantic
- PostgreSQL
- Psycopg 3
- Alembic

**Development & Infrastructure**

- Docker
- Docker Compose
- Pytest
- Ruff
- GitHub Actions

## Getting Started

### Run with Docker

Docker is the recommended way to run the project locally.

From the project root:

```bash
docker compose up --build -d
```

Docker Compose will start PostgreSQL, wait for it to become healthy, apply all Alembic migrations, and start the FastAPI application.

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation is available through Swagger UI at:

```text
http://localhost:8000/docs
```

### Load the Sample Dataset

Database migrations create the schema but do not insert the sample data automatically.

Run:

```bash
docker compose exec backend python -m scripts.seed_characters
docker compose exec backend python -m scripts.seed_media
docker compose exec backend python -m scripts.seed_references
```

The seed scripts are idempotent and can safely be executed multiple times.

### Stop the Application

```bash
docker compose down
```

To also remove the PostgreSQL Docker volume:

```bash
docker compose down -v
```

## Local Development

Create and activate a virtual environment:

```powershell
cd backend

python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the development dependencies:

```powershell
python -m pip install -r requirements-dev.txt
```

Create `backend/.env` based on `backend/.env.example`, then apply the migrations:

```powershell
python -m alembic upgrade head
```

Start the API:

```powershell
python -m uvicorn app.main:app --reload
```

## Development Checks

Run the test suite:

```bash
cd backend
python -m pytest
```

Run linting and formatting checks:

```bash
python -m ruff check .
python -m ruff format --check .
```

To automatically format the code:

```bash
python -m ruff format .
```

A GitHub Actions workflow is also configured to run linting, formatting checks, database migrations against a clean PostgreSQL instance, and the test suite on pushes and pull requests.

## Roadmap

### MVP

- [x] FastAPI REST API
- [x] PostgreSQL persistence and Alembic migrations
- [x] Characters, references, media, and franchises data model
- [x] Search, filtering, and pagination
- [x] Curated Season 1 dataset
- [x] Docker development environment
- [x] Automated backend test suite
- [x] Ruff linting and formatting
- [x] Validate GitHub Actions CI
- [ ] Web frontend

### Future

Possible future development includes:

- references from Seasons 2–9
- community contributions and moderation
- richer media metadata
- automated reference import tools
- tag-based discovery
- user accounts and favorites
- statistics
- quizzes and flashcards
- spaced repetition and learning progression
- AI-assisted explanations

One possible long-term direction is to evolve Suits Companion into an interactive learning experience where users can test how well they recognize the show's references and memorable dialogue.

## Contributing

The initial dataset is deliberately small and curated for the MVP.

As the project grows, contributions could help add missing references, correct existing data, expand the dataset to additional seasons, improve contextual explanations, and develop new backend or frontend features.

More detailed contribution guidelines will be added as the project moves beyond the initial MVP.

## Disclaimer

Suits Companion is an unofficial fan project and is not affiliated with, endorsed by, or associated with the creators, producers, distributors, broadcasters, streaming platforms, or rights holders of *Suits*.

*Suits* and all referenced movies, television series, characters, trademarks, and other intellectual property belong to their respective owners.