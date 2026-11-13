from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base

class TipoPlato(Base):
    __tablename__ = "tipo_plato"

    idTipo_Plato = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tipo = Column(String(45), nullable=False)

    # Relación con Plato
    platos = relationship("Plato", back_populates="tipo_plato")

class modalidadPedido(Base):
    __tablename__ = "modalidad_pedido"

    id_modalidad = Column(Integer, primary_key=True)
    nombre_modalidad = Column(String(50), unique=True, nullable=False)

class Estado_Pedido(Base):
    __tablename__ = "estado_pedido"

    id_estado = Column(Integer, primary_key=True)
    nombre_estado = Column(String(50), unique=True, nullable=False)