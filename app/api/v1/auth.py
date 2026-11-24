"""Rutas de autenticación Python y rutas compatibles con EP-01 de Laravel."""

import logging
from datetime import datetime, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.dependencies import bearer_scheme, get_current_user, require_admin
from app.core.config import get_settings
from app.infrastructure.database.session import get_db
from app.models.user import User
from app.models.user_session import UserSession
from app.schemas.auth import (
    ForgotPasswordRequest,
    LaravelAuthResponse,
    LaravelProfileUpdateResponse,
    LaravelUserResponse,
    LoginRequest,
    ProfileUpdateRequest,
    RegisterRequest,
    ResetPasswordRequest,
    StaffUserCreateRequest,
    TokenResponse,
)
from app.schemas.user import UserResponse
from app.services.auth_service import (
    AuthenticationError,
    PasswordResetError,
    RegistrationError,
    authenticate_user,
    authenticate_user_with_user,
    create_password_reset_link,
    create_staff_user,
    register_user,
    reset_user_password,
)


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Autenticación"])
laravel_router = APIRouter(tags=["Autenticación EP-01"])


def _request_ip(request: Request) -> str | None:
    return request.client.host if request.client else None


def _register(
    data: RegisterRequest,
    request: Request,
    db: Session,
) -> LaravelAuthResponse | JSONResponse:
    try:
        user, access_token, _ = register_user(
            db=db,
            first_name=data.first_name,
            second_name=data.second_name,
            last_name=data.last_name,
            second_last_name=data.second_last_name,
            email=str(data.email),
            phone=data.phone,
            address=data.address,
            password=data.password,
            ip_address=_request_ip(request),
            user_agent=request.headers.get("user-agent"),
        )
    except RegistrationError as error:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": "Los datos enviados no son válidos.",
                "errors": {
                    "email": [str(error)],
                    "telefono": [str(error)],
                },
            },
        )

    return LaravelAuthResponse(
        access_token=access_token,
        user=LaravelUserResponse.model_validate(user),
    )


@router.post(
    "/register",
    response_model=LaravelAuthResponse,
    status_code=status.HTTP_201_CREATED,
)
@laravel_router.post(
    "/register",
    response_model=LaravelAuthResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """Registra un cliente y devuelve el token y su perfil."""
    return _register(data, request, db)


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """Conserva la respuesta del endpoint Python que ya existía."""
    try:
        access_token, expires_in = authenticate_user(
            db=db,
            email=str(data.email),
            password=data.password,
            ip_address=_request_ip(request),
            user_agent=request.headers.get("user-agent"),
        )
    except AuthenticationError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error

    return TokenResponse(access_token=access_token, expires_in=expires_in)


@laravel_router.post("/login", response_model=LaravelAuthResponse)
def laravel_login(
    data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """Devuelve el contrato accessToken + user esperado por Laravel/Postman."""
    try:
        user, access_token, _ = authenticate_user_with_user(
            db=db,
            email=str(data.email),
            password=data.password,
            ip_address=_request_ip(request),
            user_agent=request.headers.get("user-agent"),
        )
    except AuthenticationError as error:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": "Las credenciales son incorrectas.",
                "errors": {"email": ["Las credenciales son incorrectas."]},
                #Falta agregar eñ error o mensaje si el usuario esta inactivo.
            },
        )

    return LaravelAuthResponse(
        access_token=access_token,
        user=LaravelUserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    """Devuelve el perfil autenticado con el contrato Python existente."""
    return current_user


@laravel_router.get("/me", response_model=LaravelUserResponse)
def get_laravel_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/users", response_model=list[UserResponse])
def list_python_users(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Lista cuentas para administradores, sin exponer hashes de contraseña."""
    return db.scalars(select(User).order_by(User.id)).all()


@laravel_router.get("/users", response_model=list[LaravelUserResponse])
def list_laravel_users(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Lista usuarios con los nombres de campo del contrato Laravel EP-01."""
    return db.scalars(select(User).order_by(User.id)).all()


def _create_staff_account(data: StaffUserCreateRequest, db: Session):
    try:
        return create_staff_user(
            db=db,
            first_name=data.first_name,
            second_name=data.second_name,
            last_name=data.last_name,
            second_last_name=data.second_last_name,
            email=str(data.email),
            phone=data.phone,
            address=data.address,
            password=data.password,
            role=data.role,
        )
    except RegistrationError as error:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": "Los datos enviados no son válidos.",
                "errors": {
                    "email": [str(error)],
                    "telefono": [str(error)],
                },
            },
        )


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_python_staff_account(
    data: StaffUserCreateRequest,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Crea una cuenta de personal desde la API Python."""
    return _create_staff_account(data, db)


@laravel_router.post(
    "/users",
    response_model=LaravelUserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_laravel_staff_account(
    data: StaffUserCreateRequest,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Permite a un administrador crear personal con el contrato Laravel."""
    return _create_staff_account(data, db)


def _update_profile(
    data: ProfileUpdateRequest,
    current_user: User,
    db: Session,
) -> User:
    updates = data.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Debes enviar al menos un campo para actualizar.",
        )

    if "phone" in updates and updates["phone"] is not None:
        updates["phone"] = updates["phone"].strip()
        duplicate_phone = db.scalar(
            select(User).where(
                User.phone == updates["phone"],
                User.id != current_user.id,
            )
        )
        if duplicate_phone:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El teléfono ya está registrado.",
            )

    for field, value in updates.items():
        setattr(current_user, field, value.strip() if isinstance(value, str) else value)

    try:
        db.commit()
        db.refresh(current_user)
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El teléfono ya está registrado.",
        ) from error
    except Exception:
        db.rollback()
        raise
    return current_user


@router.put("/me", response_model=UserResponse)
def update_python_profile(
    data: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _update_profile(data, current_user, db)


@laravel_router.put("/me", response_model=LaravelProfileUpdateResponse)
def update_laravel_profile(
    data: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        updated_user = _update_profile(data, current_user, db)
    except HTTPException as error:
        detail = str(error.detail)
        errors = {"telefono": [detail]} if "teléfono" in detail.lower() else {}
        return JSONResponse(
            status_code=error.status_code,
            content={"message": detail, "errors": errors},
        )
    return LaravelProfileUpdateResponse(
        message="Perfil actualizado correctamente",
        user=LaravelUserResponse.model_validate(updated_user),
    )


def _revoke_current_session(
    credentials: HTTPAuthorizationCredentials | None,
    current_user: User,
    db: Session,
) -> None:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autorizado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    settings = get_settings()
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
            options={"require": ["jti"]},
        )
    except jwt.InvalidTokenError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error

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
    session_record.revoked_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.commit()


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _revoke_current_session(credentials, current_user, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@laravel_router.post("/logout")
def laravel_logout(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _revoke_current_session(credentials, current_user, db)
    return {"message": "Sesión cerrada exitosamente"}


@router.post("/forgot-password")
@laravel_router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    reset_link = create_password_reset_link(db, str(data.email))
    if reset_link is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "No se pudo enviar el enlace. Verifica el correo."},
        )

    logger.info("Enlace de recuperación de contraseña: %s", reset_link)
    return {
        "message": "Enlace de recuperación enviado (Revisa los logs del backend)"
    }


@router.post("/reset-password")
@laravel_router.post("/reset-password")
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    try:
        reset_user_password(
            db,
            email=str(data.email),
            token=data.token,
            password=data.password,
        )
    except PasswordResetError as error:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(error)},
        )

    return {"message": "¡Contraseña restablecida con éxito!"}
