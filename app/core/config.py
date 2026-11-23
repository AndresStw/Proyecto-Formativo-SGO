"""Configuración central leída del entorno y del archivo .env."""
from functools import lru_cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "Sabor Caleño SGO"
    app_env: str = "development"
    debug: bool = True

    database_url: str  # obligatoria — se lee del .env

    jwt_secret_key: str = Field(
        default="dev-only-change-this-secret-before-deploying-32-chars",
        min_length=32,
    )
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = Field(default=1440, gt=0)
    session_inactivity_minutes: int = Field(default=30, gt=0)
    password_reset_expire_minutes: int = Field(default=60, gt=0)
    password_reset_url: str = "http://localhost:5173/reset-password"

    cors_origins: str = (
        "http://localhost:5173,http://localhost:3000,"
        "http://127.0.0.1:5173,http://127.0.0.1:3000"
    )
    cors_allow_methods: str = "GET,POST,PUT,PATCH,DELETE,OPTIONS"
    cors_allow_headers: str = (
        "Authorization,Content-Type,Accept,Origin,X-Requested-With"
    )

    @model_validator(mode="after")
    def reject_development_jwt_secret_in_production(self):
        secret = self.jwt_secret_key.lower()
        if self.app_env.lower() == "production" and (
            secret.startswith("dev-only-") or "cambia-esto" in secret
        ):
            raise ValueError("Configura JWT_SECRET_KEY antes de usar production.")
        return self

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip().rstrip("/")
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]

    @property
    def cors_allow_methods_list(self) -> list[str]:
        return [
            method.strip().upper()
            for method in self.cors_allow_methods.split(",")
            if method.strip()
        ]

    @property
    def cors_allow_headers_list(self) -> list[str]:
        return [
            header.strip()
            for header in self.cors_allow_headers.split(",")
            if header.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
