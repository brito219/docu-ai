import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    app_env: str
    database_url: str
    frontend_origin: str
    storage_type: str
    local_storage_path: Path
    max_upload_size_mb: int

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        app_env=os.getenv("APP_ENV", "development"),
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://docuai:docuai@db:5432/docuai",
        ),
        frontend_origin=os.getenv("FRONTEND_ORIGIN", "http://localhost:5173"),
        storage_type=os.getenv("STORAGE_TYPE", "LOCAL"),
        local_storage_path=Path(os.getenv("LOCAL_STORAGE_PATH", "/app/storage")),
        max_upload_size_mb=int(os.getenv("MAX_UPLOAD_SIZE_MB", "10")),
    )
