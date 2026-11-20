"""
Crea el único usuario SUPER_ADMIN de Harmony Spa.

Este script se ejecuta desde la terminal local.
No existe un endpoint público para crear este usuario.
"""

from getpass import getpass

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.security import hash_password
from app.domain.enums.user_role import UserRole
from app.infrastructure.database.session import SessionLocal
from app.models.user import User


def solicitar_datos() -> dict:
    """Solicita los datos iniciales del SUPER_ADMIN."""

    print("\n=== CREACIÓN DEL SUPER_ADMIN ===\n")

    first_name = input("Nombres: ").strip()
    last_name = input("Apellidos: ").strip()
    email = input("Correo electrónico: ").strip().lower()

    if not first_name or not last_name:
        raise ValueError("Los nombres y apellidos son obligatorios.")

    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Debes ingresar un correo electrónico válido.")

    password = getpass("Crea una contraseña (mínimo 12 caracteres): ")
    confirmation = getpass("Confirma la contraseña: ")

    if len(password) < 12:
        raise ValueError("La contraseña debe tener al menos 12 caracteres.")

    if password != confirmation:
        raise ValueError("Las contraseñas no coinciden.")

    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
    }


def crear_super_admin() -> None:
    """Crea el SUPER_ADMIN si todavía no existe."""

    db = SessionLocal()

    try:
        # 1. Comprobar si ya existe un SUPER_ADMIN.
        existing_admin = db.scalar(
            select(User).where(User.role == UserRole.SUPER_ADMIN)
        )

        if existing_admin:
            print(
                "\nNo se puede crear otro SUPER_ADMIN."
                "\nYa existe uno registrado en Harmony Spa."
            )
            return

        # 2. Solicitar los datos.
        datos = solicitar_datos()

        # 3. Comprobar si el correo ya está registrado.
        existing_email = db.scalar(
            select(User).where(User.email == datos["email"])
        )

        if existing_email:
            raise ValueError(
                "Ese correo electrónico ya está registrado."
            )

        # 4. Convertir la contraseña en un hash Argon2id.
        password_hash = hash_password(datos["password"])

        # 5. Crear el usuario con el rol SUPER_ADMIN.
        super_admin = User(
            first_name=datos["first_name"],
            last_name=datos["last_name"],
            email=datos["email"],
            password_hash=password_hash,
            role=UserRole.SUPER_ADMIN,
            is_active=True,
        )

        # 6. Guardar el usuario en MySQL.
        db.add(super_admin)
        db.commit()
        db.refresh(super_admin)

        print("\nSUPER_ADMIN creado correctamente.")
        print(f"Identificador: {super_admin.id}")
        print(f"Correo: {super_admin.email}")
        print("La contraseña se almacenó mediante Argon2id.")

    except IntegrityError:
        db.rollback()
        print(
            "\nNo se pudo crear el SUPER_ADMIN."
            "\nLa base de datos rechazó el registro por una restricción "
            "de unicidad. Es posible que otro proceso haya creado "
            "el administrador o que el correo ya exista."
        )

    except (ValueError, SQLAlchemyError) as error:
        db.rollback()
        print(f"\nNo se pudo completar la operación: {error}")

    finally:
        db.close()


if __name__ == "__main__":
    crear_super_admin()