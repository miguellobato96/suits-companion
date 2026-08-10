from fastapi import FastAPI

from app.characters.router import router as characters_router
from app.core.config import settings
from app.franchises.router import router as franchises_router
from app.media.router import router as media_router
from app.references.router import router as references_router

app = FastAPI(title=settings.app_name)

app.include_router(characters_router)
app.include_router(franchises_router)
app.include_router(media_router)
app.include_router(references_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
