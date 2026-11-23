
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.api.health import router as health_router

settings = get_settings()


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        debug=settings.debug,
        description="API REST del sistema Sabor Caleño.",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    application.include_router(health_router)
    application.include_router(
        api_router,
        prefix="/api/v1",
    )

    return application


app = create_application()
