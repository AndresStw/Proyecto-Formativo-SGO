"""
Servicio de pedidos (EP-03).

Reglas de negocio:
- RF-CAR-04: calcular precios, subtotales y total.
- RF-CAR-05: modalidad del pedido.
- RF-CAR-07: registrar el pedido con estado inicial "Pendiente".
- RF-CAR-08: historial del usuario.
- Cambio de estado respetando permisos y transiciones.
"""

from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.domain.enums.pedidos import EstadoPedidoNombre
from app.domain.enums.user_role import UserRole
from app.models.pedido import Detalle_Pedido, Pedido
from app.models.user import User
from app.repositories import pedidos as repo
from app.schemas import pedidos as schemas


# ---------- Errores de negocio ----------

class PedidoError(Exception):
    """Error base de las reglas de negocio de pedidos."""


class CatalogoNoConfiguradoError(PedidoError):
    """Faltan modalidades o estados en la base de datos (RF-CAR-05 y 07)."""


class PlatoNoEncontradoError(PedidoError):
    """Un plato del carrito no existe (RF-CAR-06)."""


class PlatoNoDisponibleError(PedidoError):
    """Un plato del carrito está agotado (RF-CAR-06)."""


class PedidoNoEncontradoError(PedidoError):
    """El pedido no existe o no es del usuario (cambio de estado)."""


class TransicionInvalidaError(PedidoError):
    """Salto de estado no permitido (cambio de estado)."""


class PermisoDenegadoError(PedidoError):
    """El usuario no puede hacer ese cambio (cambio de estado)."""


# ----- RF-CAR-04: subtotales y total -

def calcular_detalles(items) -> tuple[list[Detalle_Pedido], Decimal]:
    """
    Arma las líneas del pedido y calcula el total.
    Devuelve (lista de Detalle_Pedido, total).
    """

    detalles: list[Detalle_Pedido] = []
    total = Decimal("0.00")

    for item in items:
        precio = Decimal(
            str(item.precio_unitario if item.precio_unitario is not None else 0)
        )
        subtotal = (precio * item.cantidad).quantize(Decimal("0.01"))
        total += subtotal

        detalles.append(
            Detalle_Pedido(
                id_plato=item.id_plato,
                cantidad=item.cantidad,
                precio_unitario=precio,    # se guarda el precio unitario
                observaciones=item.observaciones,
            )
        )

    return detalles, total


# - RF-CAR-05: modalidad del pedido -

def obtener_modalidad(db: Session, nombre: str):
    """Busca la modalidad en la base de datos (Domicilio, Mesa, Para llevar)."""

    modalidad = repo.get_modalidad_por_nombre(db, nombre)

    if modalidad is None:
        raise CatalogoNoConfiguradoError(
            f"La modalidad '{nombre}' no existe en la base de datos. "
            "Ejecuta: python -m scripts.seed_pedidos"
        )

    return modalidad


# ------- RF-CAR-07: registrar el pedido como "Pendiente" ---

def crear_pedido(db: Session, user: User, data: schemas.PedidoCreate) -> Pedido:
    """Valida el carrito y registra el pedido en estado Pendiente."""

    # 1. Modalidad elegida (RF-CAR-05) y estado inicial "Pendiente".
    modalidad = obtener_modalidad(db, data.modalidad.value)
    estado_inicial = repo.get_estado_por_nombre(
        db, EstadoPedidoNombre.PENDIENTE.value
    )

    if estado_inicial is None:
        raise CatalogoNoConfiguradoError(
            "El estado 'Pendiente' no existe en la base de datos. "
            "Ejecuta: python -m scripts.seed_pedidos"
        )

    # 2. RF-CAR-04: subtotales y total.
    detalles, _total = calcular_detalles(data.items)

    # 3. Armar el pedido con sus detalles según columnas reales de `pedido`
    pedido = Pedido(
        id_cliente=data.id_cliente,
        id_mesero=data.id_mesero,
        id_mesa=data.id_mesa,
        id_estado=estado_inicial.id_estado,
        id_modalidad=modalidad.id_modalidad,
        detalles=detalles,
    )

    # 4. Guardar. Si algo falla, se deshace todo
    try:
        db.add(pedido)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

    # 5. Releer el pedido completo para devolverlo con todos sus datos.
    return repo.get_pedido_por_id(db, pedido.id_pedido)


# --+-- RF-CAR-08: historial del cliente ---

def listar_pedidos_usuario(db: Session, user: User) -> list[Pedido]:
    """Historial de pedidos del usuario, del más reciente al más antiguo."""

    es_staff = user.role in ROLES_STAFF
    if es_staff:
        return repo.listar_todos_los_pedidos(db)
    return repo.listar_pedidos_por_cliente(db, user.id)


# ---------- Cambio de estado (PATCH /pedidos/{id}/status) ----------

# Roles que pueden cambiar el estado de CUALQUIER pedido.
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


def cambiar_estado(
    db: Session,
    user: User,
    pedido_id: int,
    nuevo_estado: EstadoPedidoNombre,
) -> Pedido:
    """Cambia el estado de un pedido si el usuario puede y la transición es válida."""

    # 1. El pedido debe existir.
    pedido = repo.get_pedido_por_id(db, pedido_id)

    if pedido is None:
        raise PedidoNoEncontradoError("Pedido no encontrado.")

    es_staff = user.role in ROLES_STAFF

    # 2. Un cliente solo puede tocar sus propios pedidos.
    #    Se responde "no encontrado" para no revelar que el pedido existe.
    if not es_staff and pedido.id_cliente != user.id:
        raise PedidoNoEncontradoError("Pedido no encontrado.")

    # 3. Leer el estado actual como enum.
    try:
        estado_actual = EstadoPedidoNombre(pedido.estado.nombre_estado)
    except ValueError:
        raise TransicionInvalidaError(
            f"El estado actual '{pedido.estado.nombre_estado}' no es válido."
        )

    # 4. Reglas extra para el cliente: solo cancelar, y solo si está Pendiente.
    if not es_staff:
        if nuevo_estado != EstadoPedidoNombre.CANCELADO:
            raise PermisoDenegadoError(
                "Solo puedes cancelar tus propios pedidos."
            )
        if estado_actual != EstadoPedidoNombre.PENDIENTE:
            raise TransicionInvalidaError(
                "Solo puedes cancelar un pedido mientras está Pendiente."
            )

    # 5. Verificar que el salto de estado esté permitido en TRANSICIONES.
    if nuevo_estado not in TRANSICIONES[estado_actual]:
        raise TransicionInvalidaError(
            f"No se puede pasar un pedido de '{estado_actual.value}' "
            f"a '{nuevo_estado.value}'."
        )

    # 6. Buscar el nuevo estado en la base de datos.
    estado = repo.get_estado_por_nombre(db, nuevo_estado.value)

    if estado is None:
        raise CatalogoNoConfiguradoError(
            f"El estado '{nuevo_estado.value}' no existe en la base de datos. "
            "Ejecuta: python -m scripts.seed_pedidos"
        )

    # 7. Aplicar el cambio.
    pedido.estado = estado

    if nuevo_estado == EstadoPedidoNombre.ENTREGADO:
        # Hora de la base de datos, igual que fecha_hora.
        pedido.hora_entrega = func.now()

    # 8. Guardar. Si algo falla, se deshace todo
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

    return repo.get_pedido_por_id(db, pedido.id_pedido)
