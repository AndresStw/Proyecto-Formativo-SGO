"""Factory de la aplicación FastAPI."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Construye la misma aplicación usada por Uvicorn y Vercel."""
    from app.main import create_application

    return create_application()
