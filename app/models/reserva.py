
from sqlalchemy import Integer, String, ForeignKey, Date, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Reserva(Base):
    __tablename__ = "reserva"

    id_reserva: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    cliente_id_cliente: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("cliente.id_cliente"),
        nullable=False
    )

    mesa_id_mesa: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("mesa.id_mesa"),
        nullable=False
    )

    fecha: Mapped[Date] = mapped_column(
        Date,
        nullable=False
    )

    hora: Mapped[Time] = mapped_column(
        Time,
        nullable=False
    )

    cantidad_personas: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        String(45),
        nullable=False,
        default="Pendiente"
    )

    cliente = relationship(
        "Cliente",
        back_populates="reservas"
    )

    mesa = relationship(
        "Mesa",
        back_populates="reservas"
    )
