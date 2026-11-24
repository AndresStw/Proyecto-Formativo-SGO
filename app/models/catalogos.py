from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.database.base import Base


class TipoPlato(Base):
    __tablename__ = "tipo_plato"

    idTipo_Plato = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tipo = Column(String(45), nullable=False)

    # !Relación con Plato
    # platos = relationship(
    #     "Plato",
    #     back_populates="tipo_plato"
    # )


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

    # # ! Relación con TipoPlato
    # tipo_plato = relationship(
    #     "TipoPlato",
    #     back_populates="platos"
    # )

# CATÁLOGOS DE PEDIDOS (EP-03)

class modalidadPedido(Base):
    __tablename__ = "modalidad_pedido"

    id_modalidad = Column(Integer, primary_key=True, autoincrement=True)
    nombre_modalidad = Column("nombreModalidad", String(45), nullable=False)
    descripcion = Column(Text, nullable=True)

class Estado_Pedido(Base):
    __tablename__ = "estado_pedido"

    id_estado = Column("idEstado_Pedido", Integer, primary_key=True, autoincrement=True)
    nombre_estado = Column(String(45), unique=True, nullable=False)


class MetodoPago(Base):
    __tablename__ = "metodospago"

    idMetodoPago = Column(Integer, primary_key=True, autoincrement=True)
    metodo = Column(String(45), nullable=False)
