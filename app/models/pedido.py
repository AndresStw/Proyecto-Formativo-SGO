from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base


class Pedido(Base):
    __tablename__ = "pedido"

    id_pedido = Column("idPedido", Integer, primary_key=True, autoincrement=True)
    fecha_hora = Column(DateTime, server_default=func.now(), nullable=False)
    tiempo_preparacion = Column(Integer, nullable=True)
    hora_entrega = Column(DateTime, nullable=True)
    direccion_entrega = Column(String(255), nullable=True)

    id_mesero = Column("Mesero_id_mesero", Integer, ForeignKey("users.id"), nullable=False, index=True)
    id_mesa = Column("Mesa_idMesa", Integer, ForeignKey("mesa.idMesa", ondelete="SET NULL"), nullable=True)
    id_usuario = Column("users_id_users", Integer, ForeignKey("users.id"), nullable=False, index=True)
    id_metodo_pago = Column(
        "MetodoPago_idMetodoPago",
        Integer,
        ForeignKey("metodospago.idMetodoPago"),
        nullable=True,
        index=True,
    )
    id_modalidad = Column(
        "modalidadPedido_id_modalidad",
        Integer,
        ForeignKey("modalidad_pedido.id_modalidad"),
        nullable=False,
    )
    id_estado = Column(
        "Estado_Pedido_idEstado_Pedido",
        Integer,
        ForeignKey("estado_pedido.idEstado_Pedido"),
        nullable=False,
    )

    mesa = relationship("Mesa")
    estado = relationship("Estado_Pedido")
    modalidad = relationship("modalidadPedido")
    metodo_pago = relationship("MetodoPago")

    detalles = relationship(
        "Detalle_Pedido",
        back_populates="pedido",
        cascade="all, delete-orphan",
    )

    venta: Mapped["Venta"] = relationship(
        "Venta",
        back_populates="pedido",
        uselist=False
    )


class Detalle_Pedido(Base):
    __tablename__ = "detalle_pedido"

    id_detalle_pedido = Column("idDetalle_Pedido", Integer, primary_key=True, autoincrement=True)
    id_pedido = Column(
        "Pedido_idPedido",
        Integer,
        ForeignKey("pedido.idPedido", ondelete="CASCADE"),
        nullable=False,
    )
    id_plato = Column("Plato_idPlato", Integer, ForeignKey("plato.idPlato"), nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    observaciones = Column("Observaciones", Text, nullable=True)

    pedido = relationship("Pedido", back_populates="detalles")
    # plato = relationship("Plato")


# =========================================================
# MODELO: VENTA
# =========================================================

class Venta(Base):
    __tablename__ = "ventas"

    idVenta: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Identificador único de la venta.",
    )

    fecha: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        comment="Fecha y hora en la que se registra la venta.",
    )

    total: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        comment="Valor total de la venta.",
    )

    idPedido: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("pedido.idPedido"),
        unique=True,
        nullable=False,
        comment="Pedido al que corresponde la venta.",
    )

    idCajero: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        comment="Cajero que registra la venta.",
    )

    idMetodoPago: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("metodospago.idMetodoPago"),
        nullable=False,
        comment="Método utilizado para realizar el pago.",
    )

    pedido: Mapped["Pedido"] = relationship(
        "Pedido",
        back_populates="venta"
    )

    # cajero: Mapped["Cajero"] = relationship(
    #     "Cajero",
    #     back_populates="ventas"
    # )

    # metodoPago: Mapped["MetodoPago"] = relationship(
    #     "MetodoPago",
    #     back_populates="ventas"
    # )

