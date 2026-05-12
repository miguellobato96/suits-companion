from fastapi import FastAPI
from app.characters import router as characters_router
from app.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(characters_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}