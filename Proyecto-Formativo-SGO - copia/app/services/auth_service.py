"""
Servicio de autenticación de Harmony Spa.

Responsabilidades:
- Buscar al usuario por correo.
- Verificar su contraseña.
- Comprobar que esté activo.
- Generar un JWT.
- Registrar la sesión en MySQL.
"""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password
from app.models.user import User
from app.models.user_session import UserSession


class AuthenticationError(Exception):
    """Error cuando las credenciales no son válidas."""


def authenticate_user(
    db: Session,
    email: str,
    password: str,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> tuple[str, int]:
    """
    Autentica al usuario y registra una sesión.

    Retorna:
        (access_token, expires_in)
    """

    # 1. Buscar al usuario por correo.
    user = db.scalar(
        select(User).where(User.email == email.lower())
    )

    # 2. Comprobar credenciales.
    # El mismo mensaje evita revelar si el correo existe.
    if user is None or not verify_password(
        password,
        user.password_hash
    ):
        raise AuthenticationError(
            "Correo electrónico o contraseña incorrectos."
        )

    # 3. Comprobar que el usuario esté activo.
    if not user.is_active:
        raise AuthenticationError(
            "Correo electrónico o contraseña incorrectos."
        )

    # 4. Crear las fechas de expiración en UTC.
    now = datetime.now(timezone.utc)

    expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

    expires_at = now + timedelta(seconds=expires_in)

    # 5. Crear un identificador único para esta sesión.
    jti = str(uuid4())

    # 6. Construir el contenido del JWT.
    payload = {
        "sub": str(user.id),
        "jti": jti,
        "iat": now,
        "exp": expires_at,
    }

    # 7. Firmar el token.
    access_token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    # 8. Registrar la sesión en MySQL.
    session_record = UserSession(
        user_id=user.id,
        jti=jti,
        last_activity_at=now.replace(tzinfo=None),
        expires_at=expires_at.replace(tzinfo=None),
        is_active=True,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    try:
        db.add(session_record)
        db.commit()

    except SQLAlchemyError:
        db.rollback()
        raise

    # 9. Entregar el token y su duración.
    return access_token, expires_in