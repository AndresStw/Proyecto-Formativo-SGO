"""Valores permitidos para los pedidos (EP-03)."""

from enum import Enum


class ModalidadPedidoNombre(str, Enum):
    DOMICILIO = "Domicilio"
    MESA = "Mesa"
    PARA_LLEVAR = "Para llevar"


class EstadoPedidoNombre(str, Enum):
    PENDIENTE = "Pendiente"
    EN_PREPARACION = "En preparación"
    LISTO = "Listo"
    ENTREGADO = "Entregado"
    CANCELADO = "Cancelado"


class MetodoPagoPedido(str, Enum):
    EFECTIVO = "Efectivo"
    NEQUI = "Nequi"
    DAVIPLATA = "Daviplata"