
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
#! ORM TABLA MESERO - ESTRUCTURA

class Mesa(Base):
    __tablename__ = "mesa"

    id_mesa: Mapped[int] = mapped_column(
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
        Integer,
        ForeignKey("mesero.id_mesero"),
        nullable=False
    )

    mesero = relationship(
        "Mesero",
        back_populates="mesas"
    )
