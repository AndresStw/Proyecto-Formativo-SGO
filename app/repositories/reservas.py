
from sqlalchemy.orm import Session

from app.models.reservas import Reserva
from app.models.mesas import Mesa
from app.models.cliente import Cliente


def obtener_cliente(db: Session, cliente_id: str):
    return db.query(Cliente).filter( # ! Establece una condición para buscar en este caso por id_cliente
        Cliente.id_cliente == cliente_id
    ).first()


def obtener_mesa(db: Session, mesa_id: int):
    return db.query(Mesa).filter( # ! Consula la informacion de la BD 
        Mesa.id_mesa == mesa_id
    ).first()  # ! Devuelve el primer resultado encontrado


def crear_reserva(db: Session, datos: dict):

    nueva_reserva = Reserva(**datos)

    db.add(nueva_reserva) # ! Prepara la agregación del registro
    db.commit() # ! Confirma la operación en la BD
    db.refresh(nueva_reserva) # ! Refresca / Actualiza la tabla con el nuevo registro

    return nueva_reserva # ! Devuelve 
