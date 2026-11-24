"""Servicios para registro, autenticación y recuperación de cuentas."""

from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import secrets
from urllib.parse import urlencode
from uuid import uuid4

import jwt
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import hash_password, password_needs_rehash, verify_password
from app.domain.enums.user_role import UserRole
from app.models.password_reset_token import PasswordResetToken
from app.models.user import User
from app.models.user_session import UserSession


class AuthenticationError(Exception):
    """Error cuando las credenciales no son válidas."""


class RegistrationError(Exception):
    """Error cuando el correo o el teléfono ya están registrados."""


class PasswordResetError(Exception):
    """Error cuando el enlace de recuperación no es válido o expiró."""


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _as_naive_utc(value: datetime) -> datetime:
    return value.astimezone(timezone.utc).replace(tzinfo=None)


def _create_access_token(
    db: Session,
    user: User,
    ip_address: str | None,
    user_agent: str | None,
) -> tuple[str, int]:
    settings = get_settings()
    now = _now_utc()
    expires_in = settings.jwt_expire_minutes * 60
    expires_at = now + timedelta(seconds=expires_in)
    jti = str(uuid4())

    access_token = jwt.encode(
        {
            "sub": str(user.id),
            "jti": jti,
            "iat": now,
            "exp": expires_at,
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    db.add(
        UserSession(
            user_id=user.id,
            jti=jti,
            last_activity_at=_as_naive_utc(now),
            expires_at=_as_naive_utc(expires_at),
            is_active=True,
            ip_address=ip_address,
            user_agent=user_agent,
        )
    )
    return access_token, expires_in


def register_user(
    db: Session,
    *,
    first_name: str,
    second_name: str | None,
    last_name: str,
    second_last_name: str | None,
    email: str,
    phone: str,
    address: str | None,
    password: str,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> tuple[User, str, int]:
    normalized_email = email.strip().lower()
    normalized_phone = phone.strip()

    existing_email = db.scalar(select(User).where(User.email == normalized_email))
    existing_phone = db.scalar(select(User).where(User.phone == normalized_phone))
    if existing_email or existing_phone:
        raise RegistrationError("El correo o teléfono ya está registrado.")

    user = User(
        first_name=first_name.strip(),
        second_name=second_name.strip() if second_name else None,
        last_name=last_name.strip(),
        second_last_name=(second_last_name.strip() if second_last_name else None),
        email=normalized_email,
        phone=normalized_phone,
        address=address.strip() if address else None,
        password_hash=hash_password(password, minimum_length=6),
        role=UserRole.CLIENTE,
        is_active=True,
    )

    try:
        db.add(user)
        db.flush()
        access_token, expires_in = _create_access_token(
            db, user, ip_address, user_agent
        )
        db.commit()
        db.refresh(user)
    except IntegrityError as error:
        db.rollback()
        raise RegistrationError(
            "El correo o teléfono ya está registrado."
        ) from error
    except SQLAlchemyError:
        db.rollback()
        raise

    return user, access_token, expires_in


def create_staff_user(
    db: Session,
    *,
    first_name: str,
    second_name: str | None,
    last_name: str,
    second_last_name: str | None,
    email: str,
    phone: str,
    address: str | None,
    password: str,
    role: UserRole,
) -> User:
    """Create a staff account; callers must enforce administrator access."""
    allowed_roles = {
        UserRole.MESERO,
        UserRole.COCINERO,
        UserRole.CAJERO,
        UserRole.ADMIN,
    }
    if role not in allowed_roles:
        raise ValueError("The requested role is not a staff role.")

    normalized_email = email.strip().lower()
    normalized_phone = phone.strip()
    existing_email = db.scalar(select(User).where(User.email == normalized_email))
    existing_phone = db.scalar(select(User).where(User.phone == normalized_phone))
    if existing_email or existing_phone:
        raise RegistrationError("El correo o teléfono ya está registrado.")

    user = User(
        first_name=first_name.strip(),
        second_name=second_name.strip() if second_name else None,
        last_name=last_name.strip(),
        second_last_name=second_last_name.strip() if second_last_name else None,
        email=normalized_email,
        phone=normalized_phone,
        address=address.strip() if address else None,
        password_hash=hash_password(password, minimum_length=6),
        role=role,
        is_active=True,
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError as error:
        db.rollback()
        raise RegistrationError(
            "El correo o teléfono ya está registrado."
        ) from error
    except SQLAlchemyError:
        db.rollback()
        raise

    return user


def authenticate_user_with_user(
    db: Session,
    email: str,
    password: str,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> tuple[User, str, int]:
    user = db.scalar(select(User).where(User.email == email.strip().lower()))

    if user is None or not verify_password(password, user.password_hash):
        raise AuthenticationError("Correo electrónico o contraseña incorrectos.")

    if not user.is_active:
        raise AuthenticationError("Correo electrónico o contraseña incorrectos.")

    if password_needs_rehash(user.password_hash):
        user.password_hash = hash_password(password, minimum_length=6)

    try:
        access_token, expires_in = _create_access_token(
            db, user, ip_address, user_agent
        )
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

    return user, access_token, expires_in


def create_password_reset_link(db: Session, email: str) -> str | None:
    normalized_email = email.strip().lower()
    user = db.scalar(select(User).where(User.email == normalized_email))
    if user is None:
        return None

    now = _as_naive_utc(_now_utc())
    settings = get_settings()
    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    reset_record = db.get(PasswordResetToken, normalized_email)
    if reset_record is None:
        reset_record = PasswordResetToken(
            email=normalized_email,
            token=token_hash,
            created_at=now,
        )
        db.add(reset_record)
    else:
        # Keep one active reset token per email.
        reset_record.token = token_hash
        reset_record.created_at = now

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

    separator = "&" if "?" in settings.password_reset_url else "?"
    query = urlencode({"token": raw_token, "email": user.email})
    return f"{settings.password_reset_url}{separator}{query}"


def reset_user_password(
    db: Session,
    *,
    email: str,
    token: str,
    password: str,
) -> None:
    user = db.scalar(select(User).where(User.email == email.strip().lower()))
    if user is None:
        raise PasswordResetError("El token es inválido o ha expirado.")

    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    reset_record = db.get(PasswordResetToken, user.email)
    now = _as_naive_utc(_now_utc())
    created_at = reset_record.created_at if reset_record is not None else None
    if created_at is not None and created_at.tzinfo is not None:
        created_at = created_at.astimezone(timezone.utc).replace(tzinfo=None)
    expires_at = (
        created_at + timedelta(minutes=get_settings().password_reset_expire_minutes)
        if created_at is not None
        else None
    )
    if (
        reset_record is None
        or expires_at is None
        or now >= expires_at
        or not hmac.compare_digest(reset_record.token, token_hash)
    ):
        raise PasswordResetError("El token es inválido o ha expirado.")

    user.password_hash = hash_password(password, minimum_length=6)
    db.delete(reset_record)

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
