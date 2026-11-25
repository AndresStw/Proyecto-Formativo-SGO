"""
Esquemas de pedidos (EP-03).

El cliente envía modalidad, método de pago, dirección, plato, cantidad y
observaciones. El usuario autenticado se toma del token JWT.
"""

from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.domain.enums.pedidos import (
    EstadoPedidoNombre,
    MetodoPagoPedido,
    ModalidadPedidoNombre,
)


class PedidoCreate(BaseModel):
    """Datos para confirmar un pedido."""

    modalidad: ModalidadPedidoNombre
    metodo_pago: MetodoPagoPedido
    direccion_entrega: str | None = Field(default=None, max_length=255)
    id_plato: int = Field(gt=0)
    cantidad: int = Field(ge=1, le=50)
    observaciones: str | None = Field(default=None, max_length=255)

    @model_validator(mode="after")
    def validar_pedido(self) -> "PedidoCreate":
        direccion = (self.direccion_entrega or "").strip()

        if self.modalidad == ModalidadPedidoNombre.DOMICILIO:
            if not direccion:
                raise ValueError(
                    "La dirección de entrega es obligatoria para domicilios."
                )
            self.direccion_entrega = direccion
        else:
            self.direccion_entrega = None

        return self


class PedidoResponse(BaseModel):
    """Pedido completo con una sola línea de detalle."""

    id_pedido: int
    fecha_hora: datetime | None
    estado: str
    modalidad: str
    id_usuario: int
    id_mesero: int
    id_mesa: int | None
    id_plato: int | None
    cantidad: int
    observaciones: str | None
    direccion_entrega: str | None
    metodo_pago: str | None
    precio_unitario: float
    subtotal: float
    total: float
    hora_entrega: datetime | None

    @classmethod
    def desde_modelo(cls, pedido) -> "PedidoResponse":
        detalle = pedido.detalles[0] if pedido.detalles else None
        precio = float(detalle.precio_unitario) if detalle else 0.0
        cantidad = detalle.cantidad if detalle else 0
        subtotal = round(precio * cantidad, 2)
        total = round(
            sum(
                float(item.precio_unitario) * item.cantidad
                for item in pedido.detalles
            ),
            2,
        )

        return cls(
            id_pedido=pedido.id_pedido,
            fecha_hora=pedido.fecha_hora,
            estado=pedido.estado.nombre_estado,
            modalidad=pedido.modalidad.nombre_modalidad,
            id_usuario=pedido.id_usuario,
            id_mesero=pedido.id_mesero,
            id_mesa=pedido.id_mesa,
            id_plato=detalle.id_plato if detalle else None,
            cantidad=cantidad,
            observaciones=detalle.observaciones if detalle else None,
            direccion_entrega=pedido.direccion_entrega,
            metodo_pago=pedido.metodo_pago.metodo if pedido.metodo_pago else None,
            precio_unitario=precio,
            subtotal=subtotal,
            total=total,
            hora_entrega=pedido.hora_entrega,
        )


class PedidoStatusUpdate(BaseModel):
    """Cuerpo del PATCH: el nuevo estado."""

    estado: EstadoPedidoNombre
