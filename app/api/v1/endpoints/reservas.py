
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.schemas.reservas import ReservaCreate, ReservaResponse
from app.services.reservas import crear_reserva
from app.services.reservas import (
    crear_reserva,
    obtener_historial_reservas,
    obtener_historial_por_cliente,
    actualizar_estado_reserva
)

from app.schemas.reservas import ReservaEstadoUpdate



router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"]
)

    
@router.get("/historial/", response_model=list[ReservaResponse])
def consultar_historial(db: Session = Depends(get_db)):
    return obtener_historial_reservas(db)


@router.get(
    "/historial/cliente/{cliente_id}",
    response_model=list[ReservaResponse]
)
def consultar_historial_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    return obtener_historial_por_cliente(db, cliente_id)


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

@router.patch("/{reserva_id}/estado/", response_model=ReservaResponse)
def cambiar_estado_reserva(
    reserva_id: int,
    datos: ReservaEstadoUpdate,
    db: Session = Depends(get_db)
):
    try:
        reserva_actualizada = actualizar_estado_reserva(
            db,
            reserva_id,
            datos.estado
        )

        return reserva_actualizada

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
