"""
Acceso a datos de pedidos (EP-03).

Solo consulta y guarda; las reglas de negocio están en
app/services/pedidos.py.
"""

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.domain.enums.pedidos import EstadoPedidoNombre
from app.domain.enums.user_role import UserRole
from app.models.catalogos import Estado_Pedido, MetodoPago, Plato, modalidadPedido
from app.models.mesa import Mesa
from app.models.pedido import Pedido
from app.models.user import User


ESTADOS_ACTIVOS = (
    EstadoPedidoNombre.PENDIENTE.value,
    EstadoPedidoNombre.EN_PREPARACION.value,
    EstadoPedidoNombre.LISTO.value,
)


def get_modalidad_por_nombre(
    db: Session, nombre: str
) -> modalidadPedido | None:
    """Busca una modalidad por su nombre (ejemplo: 'Domicilio')."""
    return db.scalar(
        select(modalidadPedido).where(
            modalidadPedido.nombre_modalidad == nombre
        )
    )


def get_estado_por_nombre(db: Session, nombre: str) -> Estado_Pedido | None:
    """Busca un estado por su nombre (ej. 'Pendiente')."""
    return db.scalar(
        select(Estado_Pedido).where(Estado_Pedido.nombre_estado == nombre)
    )


def get_metodo_pago_por_nombre(db: Session, nombre: str) -> MetodoPago | None:
    """Busca un método de pago por su nombre."""
    return db.scalar(
        select(MetodoPago).where(MetodoPago.metodo == nombre)
    )


def get_plato_por_id(db: Session, id_plato: int) -> Plato | None:
    """Busca un plato por su id."""
    return db.scalar(
        select(Plato).where(Plato.idPlato == id_plato)
    )


def get_mesero_disponible(db: Session) -> User | None:
    """Primer mesero activo sin pedidos en curso."""
    estados_activos = select(Estado_Pedido.id_estado).where(
        Estado_Pedido.nombre_estado.in_(ESTADOS_ACTIVOS)
    )
    meseros_ocupados = select(Pedido.id_mesero).where(
        Pedido.id_estado.in_(estados_activos)
    )

    return db.scalar(
        select(User)
        .where(
            User.role == UserRole.MESERO,
            User.is_active.is_(True),
            User.id.not_in(meseros_ocupados),
        )
        .order_by(User.id)
        .limit(1)
        .with_for_update()
    )


def get_mesa_disponible(db: Session) -> Mesa | None:
    """Primera mesa libre."""
    return db.scalar(
        select(Mesa)
        .where(func.lower(Mesa.estado) == "libre")
        .order_by(Mesa.id_mesa)
        .limit(1)
        .with_for_update()
    )


def _cargar_relaciones():
    """Trae el pedido con detalles, estado, modalidad, método y mesa."""
    return (
        selectinload(Pedido.detalles),
        selectinload(Pedido.estado),
        selectinload(Pedido.modalidad),
        selectinload(Pedido.metodo_pago),
        selectinload(Pedido.mesa),
    )


def get_pedido_por_id(db: Session, pedido_id: int) -> Pedido | None:
    """Trae un pedido completo por su id."""
    return db.scalar(
        select(Pedido)
        .where(Pedido.id_pedido == pedido_id)
        .options(*_cargar_relaciones())
        .execution_options(populate_existing=True)
    )


def listar_pedidos_por_usuario(db: Session, id_usuario: int) -> list[Pedido]:
    """Historial de un usuario, del más reciente al más antiguo."""
    return list(
        db.scalars(
            select(Pedido)
            .where(Pedido.id_usuario == id_usuario)
            .order_by(Pedido.fecha_hora.desc(), Pedido.id_pedido.desc())
            .options(*_cargar_relaciones())
        ).all()
    )


def listar_todos_los_pedidos(db: Session) -> list[Pedido]:
    """Lista todos los pedidos, del más reciente al más antiguo."""
    return list(
        db.scalars(
            select(Pedido)
            .order_by(Pedido.fecha_hora.desc(), Pedido.id_pedido.desc())
            .options(*_cargar_relaciones())
        ).all()
    )

# Consultar pedidos por medio de tarjeta RF-PED-001

def listar_pedidos_pendientes(db: Session) -> list[Pedido]:
    """Lista los pedidos pendientes, del más antiguo al más reciente."""

    return list(
        db.scalars(
            select(Pedido)
            .join(Pedido.estado)
            .where(
                Estado_Pedido.nombre_estado
                == EstadoPedidoNombre.PENDIENTE.value
            )
            .order_by(Pedido.fecha_hora.asc(), Pedido.id_pedido.asc())
            .options(*_cargar_relaciones())
        ).all()
    )