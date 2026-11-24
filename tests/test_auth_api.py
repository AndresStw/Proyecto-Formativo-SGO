import logging
from urllib.parse import parse_qs, urlsplit

import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.core.security import hash_password, password_needs_rehash
from app.domain.enums.user_role import UserRole
from app.models.user import User


def test_registration_requires_separate_name_fields(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "nombre": "Nombre Completo",
            "email": "nombre-completo@example.com",
            "telefono": "3000000030",
            "password": "Clave123",
        },
    )
    assert response.status_code == 422


def test_ep01_authentication_flow(client, caplog):
    registration = client.post(
        "/api/v1/auth/register",
        json={
            "primerNombre": "Ana",
            "segundoNombre": "María",
            "primerApellido": "Torres",
            "email": "ana@example.com",
            "telefono": "+573001234567",
            "direccion": "Cali",
            "password": "Clave123",
        },
    )
    assert registration.status_code == 201
    registered = registration.json()
    assert registered["access_token"]
    assert registered["user"]["first_name"] == "Ana"
    assert registered["user"]["last_name"] == "Torres"
    assert registered["user"]["role"] == "CLIENTE"
    access_token = registered["access_token"]

    profile = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert profile.status_code == 200
    assert profile.json()["id"] == registered["user"]["id"]

    update = client.put(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"primerNombre": "Ana María", "direccion": "Palmira"},
    )
    assert update.status_code == 200
    assert update.json()["first_name"] == "Ana María"
    assert update.json()["address"] == "Palmira"

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "ana@example.com", "password": "Clave123"},
    )
    assert login.status_code == 200
    assert login.json()["user"]["id"] == registered["user"]["id"]

    with caplog.at_level(logging.INFO, logger="app.api.v1.auth"):
        forgot = client.post(
            "/api/v1/auth/forgot-password",
            json={"email": "ana@example.com"},
        )
    assert forgot.status_code == 200
    log_entry = next(
        record.getMessage()
        for record in caplog.records
        if "Enlace de recuperación de contraseña:" in record.getMessage()
    )
    reset_url = log_entry.split(": ", 1)[1]
    reset_query = parse_qs(urlsplit(reset_url).query)

    reset = client.post(
        "/api/v1/auth/reset-password",
        json={
            "email": "ana@example.com",
            "token": reset_query["token"][0],
            "password": "NuevaClave123",
            "password_confirmation": "NuevaClave123",
        },
    )
    assert reset.status_code == 200

    reused_reset_token = client.post(
        "/api/v1/auth/reset-password",
        json={
            "email": "ana@example.com",
            "token": reset_query["token"][0],
            "password": "OtraClave123",
            "password_confirmation": "OtraClave123",
        },
    )
    assert reused_reset_token.status_code == 400

    new_login = client.post(
        "/api/v1/auth/login",
        json={"email": "ana@example.com", "password": "NuevaClave123"},
    )
    assert new_login.status_code == 200

    logout = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {new_login.json()['access_token']}"},
    )
    assert logout.status_code == 204

    revoked_profile = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {new_login.json()['access_token']}"},
    )
    assert revoked_profile.status_code == 401


def test_ep01_cors_preflight(client):
    response = client.options(
        "/api/v1/auth/login",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "authorization,content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert response.headers["access-control-allow-credentials"] == "true"


def test_bcrypt_2y_hash_upgrades_on_login(client, test_engine):
    password = "ClaveBcrypt123"
    bcrypt_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("ascii")
    legacy_hash = "$2y$" + bcrypt_hash[4:]
    assert password_needs_rehash(legacy_hash)

    testing_session = sessionmaker(bind=test_engine, expire_on_commit=False)
    with testing_session() as db:
        db.add(
            User(
                first_name="Luis",
                last_name="Pérez",
                email="luis@example.com",
                password_hash=legacy_hash,
                role=UserRole.CLIENTE,
                is_active=True,
            )
        )
        db.commit()

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "luis@example.com", "password": password},
    )
    assert login.status_code == 200
    assert login.json()["access_token"]

    with testing_session() as db:
        user = db.scalar(select(User).where(User.email == "luis@example.com"))
        assert user is not None
        assert user.password_hash.startswith("$argon2id$")


def test_admin_can_create_staff_roles_and_list_users(client, test_engine):
    admin_email = "admin-rf07@example.com"
    admin_password = "AdminClave123"
    testing_session = sessionmaker(bind=test_engine, expire_on_commit=False)
    with testing_session() as db:
        db.add(
            User(
                first_name="Admin",
                last_name="Prueba",
                email=admin_email,
                phone="3000000002",
                password_hash=hash_password(admin_password),
                role=UserRole.ADMIN,
                is_active=True,
            )
        )
        db.commit()

    login = client.post(
        "/api/v1/auth/login",
        json={"email": admin_email, "password": admin_password},
    )
    assert login.status_code == 200
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    for index, role in enumerate(("MESERO", "COCINERO", "CAJERO", "ADMIN"), 1):
        response = client.post(
            "/api/v1/auth/users",
            headers=headers,
            json={
                "primerNombre": "Personal",
                "primerApellido": f"Prueba{index}",
                "email": f"personal{index}@example.com",
                "telefono": f"300000001{index}",
                "rol": role,
                "password": "Clave123",
            },
        )
        assert response.status_code == 201
        assert response.json()["role"] == role
        assert "password_hash" not in response.json()

    listed = client.get("/api/v1/auth/users", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 5


def test_client_cannot_create_staff_account(client):
    registration = client.post(
        "/api/v1/auth/register",
        json={
            "primerNombre": "Cliente",
            "primerApellido": "Prueba",
            "email": "cliente-rf07@example.com",
            "telefono": "3000000020",
            "password": "Clave123",
        },
    )
    assert registration.status_code == 201
    headers = {
        "Authorization": f"Bearer {registration.json()['access_token']}"
    }

    response = client.post(
        "/api/v1/auth/users",
        headers=headers,
        json={
            "primerNombre": "Personal",
            "primerApellido": "NoAutorizado",
            "email": "no-autorizado@example.com",
            "telefono": "3000000021",
            "rol": "MESERO",
            "password": "Clave123",
        },
    )
    assert response.status_code == 403


def test_local_test_email_can_login_and_request_password_reset(client, test_engine, caplog):
    email = "admin@local.test"
    password = "AdminClave123"
    testing_session = sessionmaker(bind=test_engine, expire_on_commit=False)
    with testing_session() as db:
        db.add(
            User(
                first_name="Admin",
                last_name="Local",
                email=email,
                password_hash=hash_password(password),
                role=UserRole.ADMIN,
                is_active=True,
            )
        )
        db.commit()

    login = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert login.status_code == 200
    assert login.json()["user"]["email"] == email

    with caplog.at_level(logging.INFO, logger="app.api.v1.auth"):
        forgot = client.post("/api/v1/auth/forgot-password", json={"email": email})
    assert forgot.status_code == 200
    assert "Enlace de recuperación" in caplog.text
