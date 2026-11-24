"""
Esquemas de pedidos (EP-03).

El cliente envía qué platos y cuántos quiere. Mientras no exista el modelo Plato,
se calcula el subtotal y total a partir de cantidad y precio_unitario.
"""

from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.domain.enums.pedidos import (
    EstadoPedidoNombre,
    MetodoPagoPedido,
    ModalidadPedidoNombre,
)


# ----- RF-CAR-04: líneas del carrito --

class DetallePedidoCreate(BaseModel):
    """Una línea del carrito que envía el frontend: plato y cantidad."""

    id_plato: int = Field(gt=0)   # id del plato, mayor que 0
    cantidad: int = Field(ge=1, le=50)   # entre 1 y 50 unidades
    observaciones: str | None = Field(default=None, max_length=255)
    precio_unitario: float | None = Field(default=None, gt=0)


class DetallePedidoResponse(BaseModel):

    id_detalle_pedido: int
    id_plato: int
    nombre_plato: str | None = None
    cantidad: int
    precio_unitario: float
    subtotal: float
    observaciones: str | None = None


# ---- RF-CAR-05, RF-CAR-10 y RF-CAR-11: datos que elige el cliente ---

class PedidoCreate(BaseModel):
    """Datos para confirmar un pedido."""

    modalidad: ModalidadPedidoNombre   # RF-CAR-05: Domicilio / Mesa / Para llevar
    metodo_pago: MetodoPagoPedido | None = None   # RF-CAR-10: Efectivo / Nequi etc
    direccion_entrega: str | None = Field(default=None, max_length=255)  # RF-CAR-11
    id_cliente: str = Field(min_length=1, max_length=45)
    id_mesero: int = Field(gt=0)
    id_mesa: int | None = Field(default=None, gt=0)
    items: list[DetallePedidoCreate] = Field(min_length=1, max_length=50)

    @model_validator(mode="after")
    def validar_pedido(self) -> "PedidoCreate":
        # 1. No se permiten platos repetidos: el carrito debe sumarlos en una línea.
        ids = [item.id_plato for item in self.items]

        if len(ids) != len(set(ids)):
            raise ValueError(
                "Hay platos repetidos. Suma las cantidades en una sola línea."
            )

        direccion = (self.direccion_entrega or "").strip()

        # 2. RF-CAR-11: Domicilio exige dirección.
        if self.modalidad == ModalidadPedidoNombre.DOMICILIO:
            if not direccion:
                raise ValueError(
                    "La dirección de entrega es obligatoria para domicilios."
                )
            self.direccion_entrega = direccion
        else:
            # Mesa y Para llevar no usan dirección: se descarta.
            self.direccion_entrega = None

        return self


# ----- RF-CAR-07 y RF-CAR-08: pedido que se devuelve al frontend ----

class PedidoResponse(BaseModel):
    """Pedido completo tal como se devuelve al frontend."""

    id_pedido: int
    fecha_hora: datetime | None
    estado: str
    modalidad: str
    id_cliente: str
    id_mesero: int
    id_mesa: int | None
    total: float
    hora_entrega: datetime | None
    items: list[DetallePedidoResponse]

    @classmethod
    def desde_modelo(cls, pedido) -> "PedidoResponse":
        """Convierte un Pedido del ORM en la respuesta de la API."""

        items_resp: list[DetallePedidoResponse] = []
        total_calc = 0.0

        for detalle in pedido.detalles:
            precio = float(detalle.precio_unitario)
            # Se calcula al vuelo porque `detalle_pedido` no tiene columna subtotal en MySQL
            subtotal = round(precio * detalle.cantidad, 2)
            total_calc += subtotal
            items_resp.append(
                DetallePedidoResponse(
                    id_detalle_pedido=detalle.id_detalle_pedido,
                    id_plato=detalle.id_plato,
                    nombre_plato=None,
                    cantidad=detalle.cantidad,
                    precio_unitario=precio,
                    subtotal=subtotal,
                    observaciones=detalle.observaciones,
                )
            )

        return cls(
            id_pedido=pedido.id_pedido,
            fecha_hora=pedido.fecha_hora,
            estado=pedido.estado.nombre_estado,
            modalidad=pedido.modalidad.nombre_modalidad,
            id_cliente=pedido.id_cliente,
            id_mesero=pedido.id_mesero,
            id_mesa=pedido.id_mesa,
            total=round(total_calc, 2),     # float para que JS lo sume
            hora_entrega=pedido.hora_entrega,
            items=items_resp,
        )


# ---- Cambio de estado (PATCH) -----

class PedidoStatusUpdate(BaseModel):
    """Cuerpo del PATCH: el nuevo estado."""
    estado: EstadoPedidoNombre