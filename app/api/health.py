# ! Se actualizo el archivo debido a que estaba utilizando FLASK en vez de fastAPI
# ! Debido a que el resto esta utilizando FAST

"""Health checks: servidor vivo + conexión a DB."""

from fastapi import APIRouter
from sqlalchemy import text

from app.infrastructure.database.connection import get_session

router = APIRouter(tags=["Health"])


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "Sabor Caleño SGO"
    }


@router.get("/health/db")
def health_db():
    try:
        with get_session() as db:
            db.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected"
        }

    except Exception:
        return {
            "status": "error",
            "database": "disconnected"
        }