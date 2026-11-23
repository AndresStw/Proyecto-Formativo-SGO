"""Registro ORM de autenticación que comparte metadata con Alembic."""

from sqlalchemy.orm import registry

from app.infrastructure.database.base import Base


auth_registry = registry(metadata=Base.metadata)
AuthBase = auth_registry.generate_base()
