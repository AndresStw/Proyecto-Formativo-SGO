from sqlalchemy.orm import Session

from app.repositories import mesa as mesa_repository
from app.schemas.mesa import MesaCreate, MesaUpdate
from app.domain.enums.user_role import UserRole


def obtener_mesas(db: Session):
    return mesa_repository.obtener_mesas(db)


def obtener_mesa_por_id(db: Session, mesa_id: int):
    mesa = mesa_repository.obtener_mesa_por_id(db, mesa_id)

    if not mesa:
        raise ValueError("La mesa no existe")

    return mesa


def actualizar_estado_mesa(db: Session, mesa_id: int, nuevo_estado: str):
    mesa = mesa_repository.obtener_mesa_por_id(db, mesa_id)

    if not mesa:
        raise ValueError("La mesa no existe")

    estados_permitidos = [
        "libre",
        "ocupado",
        "fuera de servicio"
    ]

    if nuevo_estado not in estados_permitidos:
        raise ValueError("El estado de la mesa no es válido")

    if mesa.estado == "fuera de servicio" and nuevo_estado == "ocupado":
        raise ValueError("No se puede ocupar una mesa fuera de servicio")

    return mesa_repository.actualizar_estado_mesa(
        db,
        mesa_id,
        nuevo_estado
    )


def registrar_mesa(db: Session, datos: MesaCreate):
    mesa_existente = mesa_repository.obtener_mesa_por_numero(
        db, datos.numero_mesa
    )

    if mesa_existente:
        raise ValueError("Ya existe una mesa con ese número")

    mesero = mesa_repository.obtener_mesero(
        db, datos.mesero_id_mesero
    )

    if (
        not mesero
        or not mesero.is_active
        or mesero.role != UserRole.MESERO
    ):
        raise ValueError(
            "El mesero no existe, está inactivo o no tiene el rol MESERO"
        )

    nuevos_datos = datos.model_dump()
    nuevos_datos["estado"] = "libre"

    return mesa_repository.crear_mesa(db, nuevos_datos)


def editar_mesa(db: Session, mesa_id: int, datos: MesaUpdate):
    mesa = mesa_repository.obtener_mesa_por_id(db, mesa_id)

    if not mesa:
        raise ValueError("La mesa no existe")

    otra_mesa = mesa_repository.obtener_mesa_por_numero(
        db, datos.numero_mesa
    )

    if otra_mesa and otra_mesa.id_mesa != mesa_id:
        raise ValueError("Ya existe otra mesa con ese número")

    mesero = mesa_repository.obtener_mesero(
        db, datos.mesero_id_mesero
    )

    if (
        not mesero
        or not mesero.is_active
        or mesero.role != UserRole.MESERO
    ):
        raise ValueError(
            "El mesero no existe, está inactivo o no tiene el rol MESERO"
        )

    return mesa_repository.actualizar_mesa(
        db,
        mesa,
        datos.model_dump()
    )


def eliminar_mesa(db: Session, mesa_id: int):
    mesa = mesa_repository.obtener_mesa_por_id(db, mesa_id)

    if not mesa:
        raise ValueError("La mesa no existe")

    if mesa.reservas:
        raise ValueError(
            "No se puede eliminar una mesa que tiene reservas asociadas"
        )

    mesa_repository.eliminar_mesa(db, mesa)
