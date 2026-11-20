from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Verificar que la API está activa")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "harmony-spa-api"}


@router.get(
    "/health/ready",
    summary="Verificar que la API puede comunicarse con MySQL",
)
def readiness_check(db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:
        # No exponer detalles internos de conexión al consumidor de la API.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Base de datos no disponible",
        ) from exc

    return {"status": "ready", "database": "connected"}