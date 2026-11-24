from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from app.domain.enums.user_role import UserRole
from app.schemas.email import EmailAddress
from app.schemas.user import UserResponse


class LoginRequest(BaseModel):
    """
    Datos que el usuario envía para iniciar sesión.
    """

    email: EmailAddress
    password: str = Field(min_length=1, max_length=128)


class RegisterRequest(BaseModel):
    """Datos para registrar una cuenta en el backend."""

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    first_name: str = Field(alias="primerNombre", min_length=1, max_length=45)
    second_name: str | None = Field(default=None, alias="segundoNombre", max_length=45)
    last_name: str = Field(alias="primerApellido", min_length=1, max_length=45)
    second_last_name: str | None = Field(default=None, alias="segundoApellido", max_length=45)
    email: EmailAddress = Field(max_length=150)
    phone: str = Field(alias="telefono", min_length=1, max_length=15)
    address: str | None = Field(default=None, alias="direccion", max_length=255)
    password: str = Field(min_length=6, max_length=128)

    @model_validator(mode="before")
    @classmethod
    def strip_registration_strings(cls, values):
        if not isinstance(values, dict):
            return values

        values = dict(values)
        for field_name in (
            "primerNombre", "first_name",
            "segundoNombre", "second_name", "primerApellido", "last_name",
            "segundoApellido", "second_last_name", "telefono", "phone",
        ):
            if isinstance(values.get(field_name), str):
                values[field_name] = values[field_name].strip()

        return values


class StaffUserCreateRequest(BaseModel):
    """Datos para que un administrador cree una cuenta de personal."""

    model_config = ConfigDict(populate_by_name=True)

    first_name: str = Field(alias="primerNombre", min_length=1, max_length=45)
    second_name: str | None = Field(default=None, alias="segundoNombre", max_length=45)
    last_name: str = Field(alias="primerApellido", min_length=1, max_length=45)
    second_last_name: str | None = Field(default=None, alias="segundoApellido", max_length=45)
    email: EmailAddress = Field(max_length=150)
    phone: str = Field(alias="telefono", min_length=1, max_length=15)
    address: str | None = Field(default=None, alias="direccion", max_length=255)
    role: UserRole = Field(alias="rol")
    password: str = Field(min_length=6, max_length=128)

    @model_validator(mode="before")
    @classmethod
    def strip_staff_strings(cls, values):
        if not isinstance(values, dict):
            return values
        values = dict(values)
        for field_name in (
            "primerNombre", "first_name", "segundoNombre", "second_name",
            "primerApellido", "last_name", "segundoApellido", "second_last_name",
            "telefono", "phone", "direccion", "address", "email",
        ):
            if isinstance(values.get(field_name), str):
                values[field_name] = values[field_name].strip()
        return values

    @field_validator("role", mode="before")
    @classmethod
    def allow_only_staff_roles(cls, value):
        if isinstance(value, UserRole):
            role = value
        else:
            try:
                role = UserRole(str(value).strip().upper())
            except ValueError as error:
                raise ValueError(
                    "El rol debe ser mesero, cocinero, cajero o admin."
                ) from error

        if role not in {
            UserRole.MESERO,
            UserRole.COCINERO,
            UserRole.CAJERO,
            UserRole.ADMIN,
        }:
            raise ValueError("El rol debe ser mesero, cocinero, cajero o admin.")
        return role


class ProfileUpdateRequest(BaseModel):
    """Campos editables del perfil; rol y estado no son modificables aquí."""

    model_config = ConfigDict(populate_by_name=True)

    first_name: str | None = Field(default=None, alias="primerNombre", min_length=1, max_length=45)
    second_name: str | None = Field(default=None, alias="segundoNombre", max_length=45)
    last_name: str | None = Field(default=None, alias="primerApellido", min_length=1, max_length=45)
    second_last_name: str | None = Field(default=None, alias="segundoApellido", max_length=45)
    phone: str | None = Field(default=None, alias="telefono", min_length=1, max_length=15)
    address: str | None = Field(default=None, alias="direccion", max_length=255)

    @model_validator(mode="before")
    @classmethod
    def strip_profile_strings(cls, values):
        if not isinstance(values, dict):
            return values
        values = dict(values)
        for field_name in (
            "primerNombre", "first_name", "segundoNombre", "second_name",
            "primerApellido", "last_name", "segundoApellido",
            "second_last_name", "telefono", "phone",
        ):
            if isinstance(values.get(field_name), str):
                values[field_name] = values[field_name].strip()
        return values

    @model_validator(mode="after")
    def required_fields_cannot_be_cleared(self):
        for field_name in ("first_name", "last_name", "phone"):
            if field_name in self.model_fields_set and getattr(self, field_name) is None:
                raise ValueError(f"{field_name} no puede ser null.")
        return self


class ForgotPasswordRequest(BaseModel):
    email: EmailAddress


class ResetPasswordRequest(BaseModel):
    email: EmailAddress
    token: str = Field(min_length=1, max_length=256)
    password: str = Field(min_length=6, max_length=128)
    password_confirmation: str = Field(min_length=6, max_length=128)

    @model_validator(mode="after")
    def passwords_must_match(self):
        if self.password != self.password_confirmation:
            raise ValueError("La confirmación de contraseña no coincide.")
        return self


class AuthResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int
    user: UserResponse
