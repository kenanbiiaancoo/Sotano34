"""FastAPI application factory."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.demo import router as demo_router
from app.api.health import router as health_router
from app.core.config import Settings, get_settings


_INDEX_PATH = Path(__file__).resolve().parent / "static" / "index.html"


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create the FastAPI application with validated settings."""

    application = FastAPI(title="Legal Intake AI")
    application.state.settings = (
        settings if settings is not None else get_settings()
    )
    application.include_router(health_router)
    application.include_router(demo_router)

    @application.get("/", response_class=FileResponse)
    def demo_page() -> FileResponse:
        """Serve the static local demo interface."""

        return FileResponse(_INDEX_PATH)

    return application


app = create_app()
