from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.auth_base import AuthBase
from app.models.user import utc_now_naive


class PasswordResetToken(AuthBase):
    """One-time password reset token associated with a user email."""

    __tablename__ = "password_reset_tokens"

    email: Mapped[str] = mapped_column(String(255), primary_key=True)
    token: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        default=utc_now_naive,
    )
