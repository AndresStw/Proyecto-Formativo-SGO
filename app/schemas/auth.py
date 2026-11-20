from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """
    Datos que el usuario envía para iniciar sesión.
    """

    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    """
    Respuesta que entrega el backend cuando
    la autenticación es exitosa.
    """

    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int