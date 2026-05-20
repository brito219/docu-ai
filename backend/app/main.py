from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.documents import router as documents_router
from app.core.config import get_settings
from app.db.database import Base, engine


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="DocuAI Viewer API",
        version="0.2.0",
        description="Day 2 upload and local persistence for the DocuAI Viewer backend.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def startup() -> None:
        settings.local_storage_path.mkdir(parents=True, exist_ok=True)
        Base.metadata.create_all(bind=engine)

    @app.get("/health", tags=["system"])
    def health_check() -> dict[str, str]:
        return {
            "status": "ok",
            "service": "docuai-backend",
            "environment": settings.app_env,
        }

    app.include_router(documents_router)

    return app


app = create_app()
