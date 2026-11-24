import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.api.health import router as health_router
from app.core.exceptions import AppException

logging.basicConfig(level=logging.INFO)
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
        allow_credentials=True,
        allow_methods=settings.cors_allow_methods_list,
        allow_headers=settings.cors_allow_headers_list,
        max_age=600,
    )

    @application.exception_handler(AppException)
    async def handle_app_exception(_, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    application.include_router(health_router)
    application.include_router(
        api_router,
        prefix="/api/v1",
    )

    return application


app = create_application()
