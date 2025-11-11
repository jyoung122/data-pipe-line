from functools import lru_cache
from pydantic import BaseSettings, AnyUrl
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Document Pipeline API"
    database_url: str = "sqlite+aiosqlite:///./app.db"
    sync_database_url: str = "sqlite:///./app.db"
    milvus_uri: Optional[AnyUrl] = None
    milvus_collection: str = "pipeline_chunks"
    milvus_embedding_dim: int = 128
    enable_background_workers: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
