from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

# ! El orden y los datos que recibe y devuelve
class MesaResponse(BaseModel):
    id_mesa: int
    capacidad: int
    numero_mesa: str
    estado: str

    model_config = ConfigDict(from_attributes=True)


class MesaEstadoUpdate(BaseModel):
     estado: Literal[
    "libre",
    "ocupado",
    "fuera de servicio"
    ]

class MesaCreate(BaseModel):
    capacidad: int = Field(gt=0)
    numero_mesa: str = Field(min_length=1, max_length=10)
    mesero_id_mesero: int = Field(gt=0)

class MesaUpdate(BaseModel):
    capacidad: int = Field(gt=0)
    numero_mesa: str = Field(min_length=1, max_length=10)
    mesero_id_mesero: int = Field(gt=0)