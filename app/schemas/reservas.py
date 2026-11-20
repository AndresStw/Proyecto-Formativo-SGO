
from datetime import date, time

from pydantic import BaseModel, ConfigDict, Field


# Datos que recibe el Backend para crear una reserva
class ReservaCreate(BaseModel):

    cliente_id_cliente: str

    mesa_id_mesa: int = Field(gt=0) # Mayor que 0

    fecha: date

    hora: time

    cantidad_personas: int = Field(gt=0) # Mayor que 0


# Datos que devuelve el Backend
class ReservaResponse(BaseModel):

    id_reserva: int

    cliente_id_cliente: str

    mesa_id_mesa: int

    fecha: date

    hora: time

    cantidad_personas: int

    estado: str

    model_config = ConfigDict(from_attributes=True)
