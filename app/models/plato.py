from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.database.base import Base


class Plato(Base):
    __tablename__ = "plato"

    idPlato = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(45), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(DECIMAL(10, 2), nullable=False)
    disponible = Column(Boolean, nullable=True, default=True)

    Tipo_Plato_idTipo_Plato = Column(
        Integer, ForeignKey("tipo_plato.idTipo_Plato"), nullable=False
    )

    tipo_plato = relationship("TipoPlato", back_populates="platos")
    receta: Mapped["Receta"] = relationship(
    "Receta",
    back_populates="plato",
    uselist=False
)