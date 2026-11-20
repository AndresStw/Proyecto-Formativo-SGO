"""
Rutas de autenticación de Harmony Spa.
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, bearer_scheme
from app.infrastructure.database.session import get_db
from app.models.user import User
from app.models.user_session import UserSession
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services.auth_service import (
    AuthenticationError,
    authenticate_user,
)


router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """Autentica al usuario y devuelve su token."""

    try:
        access_token, expires_in = authenticate_user(
            db=db,
            email=str(data.email),
            password=data.password,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )

        return TokenResponse(
            access_token=access_token,
            expires_in=expires_in,
        )

    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos.",
        )


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    """Devuelve el perfil del usuario autenticado."""

    return current_user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    credentials=Depends(bearer_scheme),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Revoca únicamente la sesión del token actual."""

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autorizado.",
        )

    import jwt
    from app.core.config import settings

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
        )

    session_record = db.scalar(
        select(UserSession).where(
            UserSession.jti == payload["jti"],
            UserSession.user_id == current_user.id,
        )
    )

    if session_record is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión no encontrada.",
        )

    session_record.is_active = False
    session_record.revoked_at = (
        datetime.now(timezone.utc).replace(tzinfo=None)
    )

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)