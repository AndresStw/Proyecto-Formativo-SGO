
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.schemas.reservas import ReservaCreate, ReservaResponse
from app.services.reservas import crear_reserva


router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"]
)


@router.post(
    "/",
    response_model=ReservaResponse,
    status_code=status.HTTP_201_CREATED
)
def registrar_reserva(
    datos: ReservaCreate,
    db: Session = Depends(get_db)
):

    try:
        nueva_reserva = crear_reserva(db, datos)

        return nueva_reserva

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
