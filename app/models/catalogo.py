
from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.database import Base


class TipoPlato(Base):
    __tablename__ = "tipo_plato"

    idTipo_Plato = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tipo = Column(String(45), nullable=False)

    # !Relación con Plato
    platos = relationship(
        "Plato",
        back_populates="tipo_plato"
    )


class Plato(Base):
    __tablename__ = "plato"

    idPlato = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(45), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(DECIMAL(10, 2), nullable=False)
    disponible = Column(Boolean, nullable=True, default=True)

    Tipo_Plato_idTipo_Plato = Column(
        Integer,
        ForeignKey("tipo_plato.idTipo_Plato"),
        nullable=False
    )

    # ! Relación con TipoPlato
    tipo_plato = relationship(
        "TipoPlato",
        back_populates="platos"
    )
