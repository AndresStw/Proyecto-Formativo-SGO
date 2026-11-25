from decimal import Decimal

from sqlalchemy import select

from app.core.security import hash_password
from app.domain.enums.pedidos import (
    EstadoPedidoNombre,
    MetodoPagoPedido,
    ModalidadPedidoNombre,
)
from app.domain.enums.user_role import UserRole
from app.models.catalogos import (
    Estado_Pedido,
    MetodoPago,
    Plato,
    TipoPlato,
    modalidadPedido,
)
from app.models.mesa import Mesa
from app.models.user import User


def _registrar_cliente(client) -> tuple[str, int]:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "primerNombre": "Cliente",
            "primerApellido": "Pedidos",
            "email": "cliente.tests@example.com",
            "telefono": "+573001112233",
            "direccion": "Cali",
            "password": "Cliente123",
        },
    )
    assert response.status_code == 201, response.text
    data = response.json()
    return data["access_token"], data["user"]["id"]


def _sembrar_catalogos(db) -> dict:
    for estado in EstadoPedidoNombre:
        db.add(Estado_Pedido(nombre_estado=estado.value))

    for modalidad in ModalidadPedidoNombre:
        db.add(modalidadPedido(nombre_modalidad=modalidad.value))

    for metodo in MetodoPagoPedido:
        db.add(MetodoPago(metodo=metodo.value))

    tipo = TipoPlato(nombre_tipo="Plato fuerte")
    db.add(tipo)
    db.flush()

    plato_disponible = Plato(
        nombre="Bandeja Paisa",
        descripcion="Plato de prueba",
        precio=Decimal("28000.00"),
        disponible=True,
        Tipo_Plato_idTipo_Plato=tipo.idTipo_Plato,
    )
    plato_agotado = Plato(
        nombre="Plato agotado",
        descripcion="Plato de prueba",
        precio=Decimal("10000.00"),
        disponible=False,
        Tipo_Plato_idTipo_Plato=tipo.idTipo_Plato,
    )
    db.add_all([plato_disponible, plato_agotado])

    meseros = []

    for numero in (1, 2):
        mesero = User(
            first_name="Mesero",
            last_name=str(numero),
            email=f"mesero{numero}@example.com",
            phone=f"300000010{numero}",
            password_hash=hash_password("Mesero123456", minimum_length=6),
            role=UserRole.MESERO,
            is_active=True,
        )
        db.add(mesero)
        meseros.append(mesero)

    db.flush()

    mesa_libre = Mesa(
        capacidad=4,
        numero_mesa="1",
        mesero_id_mesero=meseros[0].id,
        estado="libre",
    )
    mesa_ocupada = Mesa(
        capacidad=4,
        numero_mesa="2",
        mesero_id_mesero=meseros[1].id,
        estado="ocupado",
    )
    db.add_all([mesa_libre, mesa_ocupada])
    db.commit()

    return {
        "plato_disponible": plato_disponible,
        "plato_agotado": plato_agotado,
        "meseros": meseros,
        "mesa_libre": mesa_libre,
    }


def _payload(id_plato: int, modalidad: str = "Mesa") -> dict:
    return {
        "modalidad": modalidad,
        "metodo_pago": "Efectivo",
        "direccion_entrega": None,
        "id_plato": id_plato,
        "cantidad": 2,
        "observaciones": "Sin cebolla",
    }


def test_crear_pedido_asigna_recursos_disponibles(client, db_session):
    token, user_id = _registrar_cliente(client)
    datos = _sembrar_catalogos(db_session)

    response = client.post(
        "/api/v1/pedidos",
        headers={"Authorization": f"Bearer {token}"},
        json=_payload(datos["plato_disponible"].idPlato),
    )

    assert response.status_code == 201, response.text
    pedido = response.json()

    assert pedido["id_usuario"] == user_id
    assert pedido["id_mesero"] == datos["meseros"][0].id
    assert pedido["id_mesa"] == datos["mesa_libre"].id_mesa
    assert pedido["id_plato"] == datos["plato_disponible"].idPlato
    assert pedido["cantidad"] == 2
    assert pedido["metodo_pago"] == "Efectivo"
    assert pedido["precio_unitario"] == 28000.0
    assert pedido["subtotal"] == 56000.0
    assert pedido["total"] == 56000.0

    db_session.expire_all()
    mesa = db_session.get(Mesa, datos["mesa_libre"].id_mesa)
    assert mesa.estado == "ocupado"


def test_crear_pedido_requiere_token(client, db_session):
    datos = _sembrar_catalogos(db_session)

    response = client.post(
        "/api/v1/pedidos",
        json=_payload(datos["plato_disponible"].idPlato),
    )

    assert response.status_code == 401


def test_crear_pedido_con_plato_agotado(client, db_session):
    token, _ = _registrar_cliente(client)
    datos = _sembrar_catalogos(db_session)

    response = client.post(
        "/api/v1/pedidos",
        headers={"Authorization": f"Bearer {token}"},
        json=_payload(datos["plato_agotado"].idPlato),
    )

    assert response.status_code == 409


def test_crear_pedido_sin_mesa_disponible(client, db_session):
    token, _ = _registrar_cliente(client)
    datos = _sembrar_catalogos(db_session)

    for mesa in db_session.scalars(select(Mesa)).all():
        mesa.estado = "ocupado"

    db_session.commit()

    response = client.post(
        "/api/v1/pedidos",
        headers={"Authorization": f"Bearer {token}"},
        json=_payload(datos["plato_disponible"].idPlato),
    )

    assert response.status_code == 409


def test_crear_pedido_sin_mesero_disponible(client, db_session):
    token, _ = _registrar_cliente(client)
    datos = _sembrar_catalogos(db_session)

    for mesero in db_session.scalars(
        select(User).where(User.role == UserRole.MESERO)
    ).all():
        mesero.is_active = False

    db_session.commit()

    response = client.post(
        "/api/v1/pedidos",
        headers={"Authorization": f"Bearer {token}"},
        json=_payload(datos["plato_disponible"].idPlato),
    )

    assert response.status_code == 409
