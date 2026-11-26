from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.schemas.mesa import (
    MesaCreate,
    MesaUpdate,
    MesaResponse,
    MesaEstadoUpdate
)
from app.services import mesa as mesa_service
from app.api.dependencies import get_current_user, require_admin, require_staff
from app.models.user import User


router = APIRouter(prefix="/mesas", tags=["Mesas"])


@router.get("/", response_model=list[MesaResponse])
def listar_mesas(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return mesa_service.obtener_mesas(db)


@router.get("/{mesa_id}", response_model=MesaResponse)
def consultar_mesa(
    mesa_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return mesa_service.obtener_mesa_por_id(db, mesa_id)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.post("/", response_model=MesaResponse, status_code=status.HTTP_201_CREATED)
def registrar_mesa(
    datos: MesaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    try:
        return mesa_service.registrar_mesa(db, datos)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{mesa_id}", response_model=MesaResponse)
def editar_mesa(
    mesa_id: int,
    datos: MesaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    try:
        return mesa_service.editar_mesa(db, mesa_id, datos)

    except ValueError as error:
        codigo = (
            status.HTTP_404_NOT_FOUND
            if str(error) == "La mesa no existe"
            else status.HTTP_400_BAD_REQUEST
        )

        raise HTTPException(
            status_code=codigo,
            detail=str(error)
        )


@router.patch("/{mesa_id}/estado/", response_model=MesaResponse)
def cambiar_estado_mesa(
    mesa_id: int,
    datos: MesaEstadoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    try:
        return mesa_service.actualizar_estado_mesa(
            db,
            mesa_id,
            datos.estado
        )

    except ValueError as error:
        codigo = (
            status.HTTP_404_NOT_FOUND
            if str(error) == "La mesa no existe"
            else status.HTTP_400_BAD_REQUEST
        )

        raise HTTPException(
            status_code=codigo,
            detail=str(error)
        )


@router.delete("/{mesa_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_mesa(
    mesa_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    try:
        mesa_service.eliminar_mesa(db, mesa_id)
        return None

    except ValueError as error:
        codigo = (
            status.HTTP_404_NOT_FOUND
            if str(error) == "La mesa no existe"
            else status.HTTP_400_BAD_REQUEST
        )

        raise HTTPException(
            status_code=codigo,
            detail=str(error)
        )
