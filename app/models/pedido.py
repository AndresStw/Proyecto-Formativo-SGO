from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from app.infrastructure.database.base import Base

class Pedido(Base):
    __tablename__ = "pedido"

    id_pedido = Column(Integer, primary_key=True)
    fecha_hora = Column(DateTime, server_default=func.now(), nullable=False)
    tiempo_preparacion = Column(Integer, nullable=True)
    hora_entrega = Column(DateTime, nullable=True)

    id_estado = Column(Integer, ForeignKey("estado_pedido.id_estado"), nullable=False)
    id_modalidad = Column(Integer, ForeignKey("modalidad_pedido.id_modalidad"), nullable=False)

class Detalle_Pedido(Base):
    __tablename__ = "detalle_pedido"

    id_detalle_pedido = Column(Integer, primary_key=True)
    observaciones = Column(String(255), nullable=True)
    cantidad = Column(Integer, default=1, nullable=False)

    id_pedido = Column(Integer, ForeignKey("pedido.id_pedido"), nullable=False)