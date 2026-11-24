"""
Esquemas de usuarios de Harmony Spa.

Definen la información que el backend puede devolver
sin exponer datos privados.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domain.enums.user_role import UserRole
from app.schemas.email import EmailAddress


class UserResponse(BaseModel):
    """
    Información pública de un usuario.

    No incluye password_hash ni otros datos privados.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    second_name: str | None
    last_name: str
    second_last_name: str | None
    email: EmailAddress
    phone: str | None
    address: str | None
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
