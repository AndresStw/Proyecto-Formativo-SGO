from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base
from app.models.user import utc_now_naive


class UserSession(Base):

    __tablename__ = "user_sessions"

    __table_args__ = (
        Index(
            "ix_user_sessions_user_active",
            "user_id",
            "is_active"
        ),
        Index(
            "ix_user_sessions_expires_at",
            "expires_at"
        ),
    )

    # Identificador de la sesión
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # Usuario propietario de la sesión
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # Identificador único asociado al JWT (claim jti)
    jti: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
        unique=True
    )

    # Fecha de creación
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=utc_now_naive,
        server_default=func.current_timestamp()
    )

    # Última actividad del usuario
    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=utc_now_naive
    )

    # Vencimiento absoluto del token
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    # Fecha de revocación
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    # Estado de la sesión
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    # Información del dispositivo
    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True
    )

    # Relación con el usuario
    user = relationship(
        "User",
        back_populates="sessions"
    )