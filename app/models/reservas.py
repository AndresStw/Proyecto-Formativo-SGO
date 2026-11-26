from datetime import date, time, datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Integer, String, ForeignKey, Date, Time, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

# Estados de reserva: Pendiente, Confirmada,
# Cancelada, Finalizada y No asistió

def obtener_fecha_creacion():
    return datetime.now(
        ZoneInfo("America/Bogota")
    ).replace(tzinfo=None)


class Reserva(Base):
    __tablename__ = "reservas"

    id_reserva: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # Fecha y hora en que se registra la reserva
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=obtener_fecha_creacion
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

    # Fecha para la que se realiza la reserva
    fecha: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    # Hora para la que se realiza la reserva
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