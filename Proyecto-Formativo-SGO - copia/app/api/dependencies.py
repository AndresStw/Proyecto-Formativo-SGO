"""
Dependencias de autenticación y autorización de Harmony Spa.

Comprueba:
- Firma y vencimiento del JWT.
- Existencia de la sesión en MySQL.
- Revocación de la sesión.
- Estado del usuario.
- Inactividad máxima de 30 minutos.
"""

from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.infrastructure.database.session import get_db
from app.models.user import User
from app.models.user_session import UserSession


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> User:

    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autorizado. Inicia sesión nuevamente.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Comprobar que exista el encabezado Authorization.
    if credentials is None:
        raise unauthorized

    token = credentials.credentials

    try:
        # 2. Verificar la firma y el vencimiento del JWT.
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"require": ["sub", "jti", "iat", "exp"]},
        )

        user_id = int(payload["sub"])
        jti = payload["jti"]

    except (jwt.InvalidTokenError, ValueError, KeyError, TypeError):
        raise unauthorized

    # 3. Buscar la sesión y su usuario.
    result = db.execute(
        select(UserSession, User)
        .join(User, User.id == UserSession.user_id)
        .where(
            UserSession.jti == jti,
            UserSession.user_id == user_id,
        )
    ).first()

    if result is None:
        raise unauthorized

    session_record, user = result

    # 4. Comprobar que la sesión siga activa.
    if not session_record.is_active or session_record.revoked_at:
        raise unauthorized

    # 5. Comprobar que el usuario siga activo.
    if not user.is_active:
        raise unauthorized

    # 6. Trabajar con fechas UTC sin zona horaria,
    # porque nuestras columnas MySQL son DateTime sin timezone.
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # 7. Comprobar vencimiento absoluto.
    if now >= session_record.expires_at:
        session_record.is_active = False
        session_record.revoked_at = now
        db.commit()
        raise unauthorized

    # 8. Comprobar inactividad.
    inactivity_limit = timedelta(
        minutes=settings.SESSION_INACTIVITY_MINUTES
    )

    if now - session_record.last_activity_at >= inactivity_limit:
        session_record.is_active = False
        session_record.revoked_at = now
        db.commit()
        raise unauthorized

    # 9. Actualizar actividad como máximo cada 5 minutos.
    if now - session_record.last_activity_at >= timedelta(minutes=5):
        session_record.last_activity_at = now
        db.commit()

    return user