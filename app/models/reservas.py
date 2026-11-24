
from datetime import date, time

from sqlalchemy import Integer, String, ForeignKey, Date, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base
 # Estados de reserva son Pendiente, Confirmada
 # Cancelada, Finalizada y No asistió

class Reserva(Base):
    __tablename__ = "reservas"

    id_reserva: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    cliente_id_cliente: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    ) 


    mesa_id_mesa: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("mesa.idMesa"),
        nullable=False
    )

    fecha: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    hora: Mapped[time] = mapped_column(
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

    mesa = relationship(
        "Mesa",
        back_populates="reservas"
    )
