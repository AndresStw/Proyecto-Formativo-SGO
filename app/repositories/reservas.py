
from sqlalchemy.orm import Session
from datetime import timedelta
from app.models.reservas import Reserva
from app.models.mesa import Mesa
# from app.models.cliente import Cliente


# def obtener_cliente(db: Session, cliente_id: str):
#     return db.query(Cliente).filter( # ! Establece una condición para buscar en este caso por id_cliente
#         Cliente.id_cliente == cliente_id
#     ).first()


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

# ! Cada reserva tiene maximo una duración de 2 horas 

def obtener_reservas_por_mesa_y_fecha(
    db: Session,
    mesa_id: int,
    fecha
):
    fecha_anterior = fecha - timedelta(days=1)

    return db.query(Reserva).filter(
        Reserva.mesa_id_mesa == mesa_id,
        Reserva.fecha >= fecha_anterior,
        Reserva.fecha <= fecha,
        Reserva.estado != "Cancelada"
    ).all()

