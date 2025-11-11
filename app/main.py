from fastapi import FastAPI

from .api import documents_router, health_router, pipelines_router, runs_router
from .core.config import get_settings
from .core.init_db import create_all_tables
from .core.logging import configure_logging

configure_logging()
create_all_tables()

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.include_router(health_router.router, prefix="/api/v1")
app.include_router(pipelines_router.router, prefix="/api/v1")
app.include_router(runs_router.router, prefix="/api/v1")
app.include_router(documents_router.router, prefix="/api/v1")


@app.get("/")
async def root() -> dict:
    return {"message": settings.app_name}
