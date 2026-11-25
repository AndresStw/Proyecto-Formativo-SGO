"""
Servicio de pedidos (EP-03).

Reglas de negocio:
- Asignación automática de mesero y mesa disponibles.
- Validación del plato y del método de pago.
- Registro del pedido con estado inicial "Pendiente".
- Historial del usuario.
- Cambio de estado respetando permisos y transiciones.
"""

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.domain.enums.pedidos import EstadoPedidoNombre, ModalidadPedidoNombre
from app.domain.enums.user_role import UserRole
from app.models.pedido import Detalle_Pedido, Pedido
from app.models.user import User
from app.repositories import pedidos as repo
from app.schemas import pedidos as schemas


class PedidoError(Exception):
    """Error base de las reglas de negocio de pedidos."""


class CatalogoNoConfiguradoError(PedidoError):
    """Faltan modalidades, estados o métodos de pago en la base de datos."""


class PlatoNoEncontradoError(PedidoError):
    """El plato enviado no existe."""


class PlatoNoDisponibleError(PedidoError):
    """El plato enviado está agotado."""


class MeseroNoDisponibleError(PedidoError):
    """No hay meseros activos sin pedidos en curso."""


class MesaNoDisponibleError(PedidoError):
    """No hay mesas libres."""


class PedidoNoEncontradoError(PedidoError):
    """El pedido no existe o no es del usuario."""


class TransicionInvalidaError(PedidoError):
    """Salto de estado no permitido."""


class PermisoDenegadoError(PedidoError):
    """El usuario no puede hacer ese cambio."""


ROLES_STAFF = {UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.COCINERO}

TRANSICIONES: dict[EstadoPedidoNombre, set[EstadoPedidoNombre]] = {
    EstadoPedidoNombre.PENDIENTE: {
        EstadoPedidoNombre.EN_PREPARACION,
        EstadoPedidoNombre.CANCELADO,
    },
    EstadoPedidoNombre.EN_PREPARACION: {
        EstadoPedidoNombre.LISTO,
        EstadoPedidoNombre.CANCELADO,
    },
    EstadoPedidoNombre.LISTO: {EstadoPedidoNombre.ENTREGADO},
    EstadoPedidoNombre.ENTREGADO: set(),
    EstadoPedidoNombre.CANCELADO: set(),
}

ESTADOS_QUE_LIBERAN_MESA = {
    EstadoPedidoNombre.ENTREGADO,
    EstadoPedidoNombre.CANCELADO,
}


def obtener_modalidad(db: Session, nombre: str):
    """Busca la modalidad en la base de datos (Domicilio, Mesa, Para llevar)."""

    modalidad = repo.get_modalidad_por_nombre(db, nombre)

    if modalidad is None:
        raise CatalogoNoConfiguradoError(
            f"La modalidad '{nombre}' no existe en la base de datos. "
            "Ejecuta: python -m scripts.seed_pedidos"
        )

    return modalidad


def crear_pedido(db: Session, user: User, data: schemas.PedidoCreate) -> Pedido:
    """Valida el pedido, asigna recursos y lo registra en estado Pendiente."""

    modalidad = obtener_modalidad(db, data.modalidad.value)
    estado_inicial = repo.get_estado_por_nombre(
        db, EstadoPedidoNombre.PENDIENTE.value
    )

    if estado_inicial is None:
        raise CatalogoNoConfiguradoError(
            "El estado 'Pendiente' no existe en la base de datos. "
            "Ejecuta: python -m scripts.seed_pedidos"
        )

    metodo_pago = repo.get_metodo_pago_por_nombre(
        db, data.metodo_pago.value
    )

    if metodo_pago is None:
        raise CatalogoNoConfiguradoError(
            f"El método de pago '{data.metodo_pago.value}' no existe. "
            "Ejecuta: python -m scripts.seed_pedidos"
        )

    plato = repo.get_plato_por_id(db, data.id_plato)

    if plato is None:
        raise PlatoNoEncontradoError("El plato no existe.")

    if not plato.disponible:
        raise PlatoNoDisponibleError("El plato no está disponible.")

    mesero = repo.get_mesero_disponible(db)

    if mesero is None:
        raise MeseroNoDisponibleError(
            "No hay meseros disponibles en este momento."
        )

    mesa = None

    if data.modalidad == ModalidadPedidoNombre.MESA:
        mesa = repo.get_mesa_disponible(db)

        if mesa is None:
            raise MesaNoDisponibleError(
                "No hay mesas disponibles en este momento."
            )

        mesa.estado = "ocupado"

    detalle = Detalle_Pedido(
        id_plato=plato.idPlato,
        cantidad=data.cantidad,
        precio_unitario=plato.precio,
        observaciones=data.observaciones,
    )

    pedido = Pedido(
        id_usuario=user.id,
        id_mesero=mesero.id,
        id_mesa=mesa.id_mesa if mesa else None,
        id_metodo_pago=metodo_pago.idMetodoPago,
        direccion_entrega=data.direccion_entrega,
        id_estado=estado_inicial.id_estado,
        id_modalidad=modalidad.id_modalidad,
        detalles=[detalle],
    )

    try:
        db.add(pedido)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

    return repo.get_pedido_por_id(db, pedido.id_pedido)


def listar_pedidos_usuario(db: Session, user: User) -> list[Pedido]:
    """Historial de pedidos del usuario, del más reciente al más antiguo."""

    if user.role in ROLES_STAFF:
        return repo.listar_todos_los_pedidos(db)

    return repo.listar_pedidos_por_usuario(db, user.id)


def cambiar_estado(
    db: Session,
    user: User,
    pedido_id: int,
    nuevo_estado: EstadoPedidoNombre,
) -> Pedido:
    """Cambia el estado de un pedido si el usuario puede y la transición es válida."""

    pedido = repo.get_pedido_por_id(db, pedido_id)

    if pedido is None:
        raise PedidoNoEncontradoError("Pedido no encontrado.")

    es_staff = user.role in ROLES_STAFF

    if not es_staff and pedido.id_usuario != user.id:
        raise PedidoNoEncontradoError("Pedido no encontrado.")

    try:
        estado_actual = EstadoPedidoNombre(pedido.estado.nombre_estado)
    except ValueError:
        raise TransicionInvalidaError(
            f"El estado actual '{pedido.estado.nombre_estado}' no es válido."
        )

    if not es_staff:
        if nuevo_estado != EstadoPedidoNombre.CANCELADO:
            raise PermisoDenegadoError(
                "Solo puedes cancelar tus propios pedidos."
            )
        if estado_actual != EstadoPedidoNombre.PENDIENTE:
            raise TransicionInvalidaError(
                "Solo puedes cancelar un pedido mientras está Pendiente."
            )

    if nuevo_estado not in TRANSICIONES[estado_actual]:
        raise TransicionInvalidaError(
            f"No se puede pasar un pedido de '{estado_actual.value}' "
            f"a '{nuevo_estado.value}'."
        )

    estado = repo.get_estado_por_nombre(db, nuevo_estado.value)

    if estado is None:
        raise CatalogoNoConfiguradoError(
            f"El estado '{nuevo_estado.value}' no existe en la base de datos. "
            "Ejecuta: python -m scripts.seed_pedidos"
        )

    pedido.estado = estado

    if nuevo_estado == EstadoPedidoNombre.ENTREGADO:
        pedido.hora_entrega = func.now()

    if nuevo_estado in ESTADOS_QUE_LIBERAN_MESA and pedido.mesa is not None:
        pedido.mesa.estado = "libre"

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

    return repo.get_pedido_por_id(db, pedido.id_pedido)
