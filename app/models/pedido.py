
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.infrastructure.database.base import Base


class Pedido(Base):
    __tablename__ = "pedido"

    id_pedido = Column(Integer, primary_key=True)
    fecha_hora = Column(DateTime, server_default=func.now(), nullable=False)
    tiempo_preparacion = Column(Integer, nullable=True)
    hora_entrega = Column(DateTime, nullable=True)

    id_estado = Column(Integer, ForeignKey("estado_pedido.id_estado"), nullable=False)
    id_modalidad = Column(Integer, ForeignKey("modalidad_pedido.id_modalidad"), nullable=False)

    venta: Mapped["Venta"] = relationship(
        "Venta",
        back_populates="pedido",
        uselist=False
    )


class Detalle_Pedido(Base):
    __tablename__ = "detalle_pedido"

    id_detalle_pedido = Column(Integer, primary_key=True)
    observaciones = Column(String(255), nullable=True)
    cantidad = Column(Integer, default=1, nullable=False)

    id_pedido = Column(Integer, ForeignKey("pedido.id_pedido"), nullable=False)


# =========================================================
# MODELO: VENTA
# =========================================================

class Venta(Base):
    __tablename__ = "ventas"

    idVenta: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Identificador único de la venta."
    )

    fecha: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        comment="Fecha y hora en la que se registra la venta."
    )

    total: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        comment="Valor total de la venta."
    )

    idPedido: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("pedido.id_pedido"),
        unique=True,
        nullable=False,
        comment="Pedido al que corresponde la venta."
    )

    idCajero: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("TABLA_CAJERO.ID_CAJERO"),
        nullable=False,
        comment="Cajero que registra la venta."
    )

    idMetodoPago: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("metodosPago.idMetodoPago"),
        nullable=False,
        comment="Método utilizado para realizar el pago."
    )

    pedido: Mapped["Pedido"] = relationship(
        "Pedido",
        back_populates="venta"
    )

    cajero: Mapped["Cajero"] = relationship(
        "Cajero",
        back_populates="ventas"
    )

    metodoPago: Mapped["MetodoPago"] = relationship(
        "MetodoPago",
        back_populates="ventas"
    )
