"""
Acceso a datos de pedidos (EP-03).

Solo consulta y guarda; las reglas de negocio están en
app/services/pedidos.py.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.catalogos import Estado_Pedido, modalidadPedido
from app.models.pedido import Detalle_Pedido, Pedido


# -- RF-CAR-04: precios reales desde la base de datos ------
# (Pendiente de activar cuando exista el modelo Plato)


# ------ RF-CAR-05: modalidad del pedido --

def get_modalidad_por_nombre(
    db: Session, nombre: str
) -> modalidadPedido | None:
    """Busca una modalidad por su nombre (ejemplo: 'Domicilio')."""
    return db.scalar(
        select(modalidadPedido).where(
            modalidadPedido.nombre_modalidad == nombre
        )
    )


# ---- RF-CAR-07: estado inicial y lectura del pedido ----------

def get_estado_por_nombre(db: Session, nombre: str) -> Estado_Pedido | None:
    """Busca un estado por su nombre (ej. 'Pendiente')."""
    return db.scalar(
        select(Estado_Pedido).where(Estado_Pedido.nombre_estado == nombre)
    )


def _cargar_relaciones():
    """Trae el pedido con detalles, estado y modalidad."""
    # Cuando exista el modelo Plato, se puede añadir selectinload(Detalle_Pedido.plato)
    return (
        selectinload(Pedido.detalles),
        selectinload(Pedido.estado),
        selectinload(Pedido.modalidad),
    )


def get_pedido_por_id(db: Session, pedido_id: int) -> Pedido | None:
    """Trae un pedido completo por su id."""
    return db.scalar(
        select(Pedido)
        .where(Pedido.id_pedido == pedido_id)
        .options(*_cargar_relaciones())
        # Fuerza a leer de nuevo los datos que genera la base de datos
        # (fecha_hora, hora_entrega) después de un commit.
        .execution_options(populate_existing=True)
    )


# -- RF-CAR-08: historial del cliente / pedidos -----

def listar_pedidos_por_cliente(db: Session, id_cliente: str) -> list[Pedido]:
    """Historial de un cliente, del más reciente al más antiguo."""
    return list(
        db.scalars(
            select(Pedido)
            .where(Pedido.id_cliente == id_cliente)
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