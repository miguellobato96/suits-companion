from fastapi import FastAPI
from app.characters import router as characters_router

app = FastAPI(title="Suits Companion API")
app.include_router(characters_router)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}