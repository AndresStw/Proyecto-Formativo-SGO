
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

# Estados de mesa son libre, ocupado, finalizado
# Fuera de servicio
class Mesa(Base):
    __tablename__ = "mesa"

    id_mesa: Mapped[int] = mapped_column(
        "idMesa",
        Integer,
        primary_key=True,
        autoincrement=True
    )

    capacidad: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    numero_mesa: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        unique=True
    )

    
    mesero_id_mesero: Mapped[int] = mapped_column(
    "Mesero_id_mesero",
    Integer,
    ForeignKey("mesero.id_mesero"),
    nullable=False
)

    estado: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="libre"
    )

    mesero = relationship(
        "Mesero",
        back_populates="mesas"
    )

    reservas = relationship(
        "Reserva",
        back_populates="mesa"
    )

