from datetime import date, time, datetime

from pydantic import BaseModel, ConfigDict, Field

from typing import Literal


# Datos que recibe el Backend para crear una reserva
class ReservaCreate(BaseModel):

    mesa_id_mesa: int = Field(gt=0)

    fecha: date

    hora: time

    cantidad_personas: int = Field(gt=0)


# Datos que devuelve el Backend y guarda
class ReservaResponse(BaseModel):

    id_reserva: int

    cliente_id_cliente: int

    mesa_id_mesa: int

    fecha: date

    hora: time

    fecha_creacion: datetime

    cantidad_personas: int

    estado: str

    model_config = ConfigDict(from_attributes=True)


class ReservaEstadoUpdate(BaseModel):
    estado: Literal[
        "Pendiente",
        "Confirmada",
        "Cancelada",
        "Finalizada",
        "No asistió"
    ]