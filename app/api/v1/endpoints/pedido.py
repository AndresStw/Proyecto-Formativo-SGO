"""
Rutas de pedidos (EP-03).
POST  /pedidos                 -> crear pedido (usuario del token, mesero y mesa automáticos)
GET   /pedidos                 -> historial de todos los pedidos
PATCH /pedidos/{id}/status     -> cambiar el estado de un pedido
"""

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.infrastructure.database.session import get_db
from app.models.user import User
from app.schemas import pedidos as schemas
from app.services import pedidos as pedido_service


router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


# Qué código HTTP devuelve cada error de negocio.
_STATUS_POR_ERROR = {
    pedido_service.PedidoNoEncontradoError: status.HTTP_404_NOT_FOUND,
    pedido_service.PlatoNoEncontradoError: status.HTTP_404_NOT_FOUND,
    pedido_service.PlatoNoDisponibleError: status.HTTP_409_CONFLICT,
    pedido_service.MeseroNoDisponibleError: status.HTTP_409_CONFLICT,
    pedido_service.MesaNoDisponibleError: status.HTTP_409_CONFLICT,
    pedido_service.TransicionInvalidaError: status.HTTP_409_CONFLICT,
    pedido_service.PermisoDenegadoError: status.HTTP_403_FORBIDDEN,
    pedido_service.CatalogoNoConfiguradoError: status.HTTP_503_SERVICE_UNAVAILABLE,
}


def _a_http(error: pedido_service.PedidoError) -> HTTPException:
    """Convierte un error de negocio en una respuesta HTTP con su mensaje."""
    return HTTPException(
        status_code=_STATUS_POR_ERROR.get(
            type(error), status.HTTP_400_BAD_REQUEST
        ),
        detail=str(error),
    )


# ---------- RF-CAR-07: POST /pedidos  ----------

@router.post(
    "",
    response_model=schemas.PedidoResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_pedido(
    data: schemas.PedidoCreate,                          # cuerpo ya validado
    db: Session = Depends(get_db),                       # sesión de base de datos
    current_user: User = Depends(get_current_user),      # usuario del token JWT
):
    """Registra el pedido del usuario autenticado con estado Pendiente."""

    try:
        pedido = pedido_service.crear_pedido(db, current_user, data)
    except pedido_service.PedidoError as error:
        raise _a_http(error)

    return schemas.PedidoResponse.desde_modelo(pedido)

# --- RF-CAR-08: GET /pedidos -----

@router.get("", response_model=list[schemas.PedidoResponse])
def historial_pedidos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Historial de pedidos del usuario autenticado."""

    pedidos = pedido_service.listar_pedidos_usuario(db, current_user)

    return [schemas.PedidoResponse.desde_modelo(pedido) for pedido in pedidos]

#----- Cambio de estado: PATCH /pedidos/{id}/status ----------

@router.patch("/{pedido_id}/status", response_model=schemas.PedidoResponse)
def actualizar_estado_pedido(
    data: schemas.PedidoStatusUpdate,
    pedido_id: int = Path(gt=0),                         # id en la URL, mayor que 0
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Cambia el estado de un pedido.

    - ADMIN, SUPER_ADMIN y COCINERO: cualquier transición válida.
    - CLIENTE: solo puede cancelar sus propios pedidos Pendientes.
    """

    try:
        pedido = pedido_service.cambiar_estado(
            db, current_user, pedido_id, data.estado
        )
    except pedido_service.PedidoError as error:
        raise _a_http(error)

    return schemas.PedidoResponse.desde_modelo(pedido)

# ? RF-PED-01: GET /pedidos/pendientes 

@router.get(
    "/pendientes",
    response_model=list[schemas.PedidoResponse],
)
def pedidos_pendientes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lista los pedidos pendientes para cocina y administradores."""

    try:
        pedidos = pedido_service.listar_pedidos_pendientes(
            db, current_user
        )
    except pedido_service.PedidoError as error:
        raise _a_http(error)

    return [
        schemas.PedidoResponse.desde_modelo(pedido)
        for pedido in pedidos
    ]