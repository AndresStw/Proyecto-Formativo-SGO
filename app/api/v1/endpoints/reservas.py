
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.schemas.reservas import (
    ReservaCreate,
    ReservaResponse,
    ReservaEstadoUpdate
)
from app.services.reservas import (
    crear_reserva,
    obtener_historial_reservas,
    obtener_historial_por_cliente,
    actualizar_estado_reserva
)
from app.api.dependencies import (
    get_current_user,
    require_staff
)
from app.models.user import User
from app.domain.enums.user_role import UserRole

router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"]
)


# Consultar historial general: solo personal autorizado
@router.get(
    "/historial/",
    response_model=list[ReservaResponse]
)
def consultar_historial(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    return obtener_historial_reservas(db)


# Consultar historial propio: solo clientes
@router.get(
    "/historial/cliente/",
    response_model=list[ReservaResponse]
)
def consultar_historial_cliente(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.CLIENTE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los clientes pueden consultar su propio historial."
        )

    return obtener_historial_por_cliente(db, current_user.id)


# Registrar reserva
@router.post(
    "/",
    response_model=ReservaResponse,
    status_code=status.HTTP_201_CREATED
)
def registrar_reserva(
    datos: ReservaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return crear_reserva(db, datos, current_user)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


# Actualizar estado de reserva: solo personal autorizado
@router.patch(
    "/{reserva_id}/estado/",
    response_model=ReservaResponse
)
def cambiar_estado_reserva(
    reserva_id: int,
    datos: ReservaEstadoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    try:
        reserva_actualizada = actualizar_estado_reserva(
            db,
            reserva_id,
            datos.estado
        )

        if not reserva_actualizada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La reserva no existe"
            )

        return reserva_actualizada

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
