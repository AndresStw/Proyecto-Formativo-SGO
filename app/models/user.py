from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Computed,
    DateTime,
    Enum as SAEnum,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums.user_role import UserRole
from app.infrastructure.database.auth_base import AuthBase


def utc_now_naive() -> datetime:
    """
    Obtiene la fecha y hora UTC sin información de zona horaria,
    para almacenarla de forma consistente en MySQL DATETIME.
    """

    return datetime.now(timezone.utc).replace(tzinfo=None)


class User(AuthBase):

    __tablename__ = "users"

    __table_args__ = (
        UniqueConstraint(
            "super_admin_slot",
            name="uq_users_single_super_admin"
        ),
        Index(
            "uq_users_phone",
            "phone",
            unique=True,
        ),
        Index(
            "ix_users_role_active",
            "role",
            "is_active"
        ),
    )

    # Identificador principal
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # Información personal
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    second_name: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    second_last_name: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True
    )

    email: Mapped[str] = mapped_column(
        String(254),
        nullable=False,
        unique=True
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    address: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    # Seguridad
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # Rol del usuario
    role: Mapped[UserRole] = mapped_column(
        SAEnum(
            UserRole,
            values_callable=lambda cls: [
                role.value for role in cls
            ],
            native_enum=False,
            create_constraint=True,
            length=20,
            name="user_role",
        ),
        nullable=False
    )

    # Estado de la cuenta
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    # Fechas de auditoría
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    # Restricción para permitir un solo SUPER_ADMIN.
    # MySQL asignará 1 a ese rol y NULL a los demás.
    super_admin_slot: Mapped[int | None] = mapped_column(
        Integer,
        Computed(
            "CASE WHEN role = 'SUPER_ADMIN' THEN 1 ELSE NULL END",
            persisted=True
        ),
        nullable=True
    )

    # Relación con las sesiones del usuario
    sessions = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
