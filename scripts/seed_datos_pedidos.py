"""
Carga datos de prueba para pedidos: meseros, mesas, platos y un cliente.

Uso (desde la raíz del proyecto):
    python -m scripts.seed_datos_pedidos
"""

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.security import hash_password
from app.domain.enums.user_role import UserRole
from app.infrastructure.database.session import SessionLocal
from app.models.catalogos import Plato, TipoPlato
from app.models.mesa import Mesa
from app.models.user import User


MESEROS = [
    {
        "first_name": "Mesero",
        "last_name": "Uno",
        "email": "mesero1@test.com",
        "phone": "3000000101",
        "password": "Mesero123456",
    },
    {
        "first_name": "Mesero",
        "last_name": "Dos",
        "email": "mesero2@test.com",
        "phone": "3000000102",
        "password": "Mesero123456",
    },
]

CLIENTE = {
    "first_name": "Cliente",
    "last_name": "Prueba",
    "email": "cliente.pedidos@test.com",
    "phone": "3000000201",
    "password": "Cliente123456",
    "address": "Cali",
}

TIPOS_PLATO = ["Plato fuerte", "Bebida", "Postre"]

PLATOS = [
    {
        "nombre": "Bandeja Paisa",
        "descripcion": "Frijoles, carne, chorizo, arroz, huevo y plátano.",
        "precio": Decimal("28000.00"),
        "tipo": "Plato fuerte",
    },
    {
        "nombre": "Sancocho de Gallina",
        "descripcion": "Sopa tradicional con gallina, papa y yuca.",
        "precio": Decimal("22000.00"),
        "tipo": "Plato fuerte",
    },
    {
        "nombre": "Arroz con Pollo",
        "descripcion": "Arroz con pollo desmechado y ensalada.",
        "precio": Decimal("20000.00"),
        "tipo": "Plato fuerte",
    },
    {
        "nombre": "Limonada Natural",
        "descripcion": "Limonada fría preparada en el momento.",
        "precio": Decimal("5000.00"),
        "tipo": "Bebida",
    },
    {
        "nombre": "Tres Leches",
        "descripcion": "Porción de torta tres leches.",
        "precio": Decimal("9000.00"),
        "tipo": "Postre",
    },
]

TOTAL_MESAS = 10


def _get_or_create_user(db, data, role: UserRole):
    user = db.scalar(select(User).where(User.email == data["email"]))

    if user is not None:
        return user, False

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        phone=data["phone"],
        address=data.get("address"),
        password_hash=hash_password(data["password"], minimum_length=6),
        role=role,
        is_active=True,
    )
    db.add(user)
    db.flush()
    return user, True


def _get_or_create_tipo(db, nombre: str):
    tipo = db.scalar(
        select(TipoPlato).where(TipoPlato.nombre_tipo == nombre)
    )

    if tipo is not None:
        return tipo, False

    tipo = TipoPlato(nombre_tipo=nombre)
    db.add(tipo)
    db.flush()
    return tipo, True


def _get_or_create_plato(db, data, tipos):
    plato = db.scalar(select(Plato).where(Plato.nombre == data["nombre"]))

    if plato is not None:
        return plato, False

    plato = Plato(
        nombre=data["nombre"],
        descripcion=data["descripcion"],
        precio=data["precio"],
        disponible=True,
        Tipo_Plato_idTipo_Plato=tipos[data["tipo"]].idTipo_Plato,
    )
    db.add(plato)
    return plato, True


def sembrar_datos() -> None:
    db = SessionLocal()

    try:
        creados = []

        meseros = []

        for data in MESEROS:
            mesero, creado = _get_or_create_user(db, data, UserRole.MESERO)
            meseros.append(mesero)

            if creado:
                creados.append(f"mesero: {data['email']}")

        _cliente, creado = _get_or_create_user(db, CLIENTE, UserRole.CLIENTE)

        if creado:
            creados.append(f"cliente: {CLIENTE['email']}")

        tipos = {}

        for nombre in TIPOS_PLATO:
            tipo, creado = _get_or_create_tipo(db, nombre)
            tipos[nombre] = tipo

            if creado:
                creados.append(f"tipo de plato: {nombre}")

        for data in PLATOS:
            plato, creado = _get_or_create_plato(db, data, tipos)

            if creado:
                creados.append(f"plato: {data['nombre']}")

        for numero in range(1, TOTAL_MESAS + 1):
            numero_mesa = str(numero)
            existe = db.scalar(
                select(Mesa).where(Mesa.numero_mesa == numero_mesa)
            )

            if existe is not None:
                continue

            db.add(
                Mesa(
                    capacidad=4,
                    numero_mesa=numero_mesa,
                    mesero_id_mesero=meseros[(numero - 1) % len(meseros)].id,
                    estado="libre",
                )
            )
            creados.append(f"mesa: {numero_mesa}")

        db.commit()

        if creados:
            print("Registros creados:")
            for linea in creados:
                print(f"  - {linea}")
        else:
            print("Los datos de prueba ya estaban completos.")

        print("\nCredenciales de prueba:")
        print("  - Cliente: cliente.pedidos@test.com / Cliente123456")
        print("  - Mesero 1: mesero1@test.com / Mesero123456")
        print("  - Mesero 2: mesero2@test.com / Mesero123456")

    except SQLAlchemyError as error:
        db.rollback()
        print(f"Error al sembrar los datos de prueba: {error}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    sembrar_datos()
