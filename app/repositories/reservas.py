
from sqlalchemy.orm import Session
from datetime import timedelta
from app.domain.enums.user_role import UserRole
from app.models.reservas import Reserva
from app.models.mesa import Mesa
from app.models.user import User


def obtener_cliente(db: Session, cliente_id: int):
    return db.query(User).filter(
        User.id == cliente_id,
        User.role == UserRole.CLIENTE,
        User.is_active.is_(True),
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

# ! Cada reserva tiene maximo una duración de 2 horas 

def obtener_reservas_por_mesa_y_fecha(
    db: Session,
    mesa_id: int,
    fecha
):
    fecha_anterior = fecha - timedelta(days=1)
    fecha_siguiente = fecha + timedelta(days=1)

    return db.query(Reserva).filter(
        Reserva.mesa_id_mesa == mesa_id,
        Reserva.fecha >= fecha_anterior,
        Reserva.fecha <= fecha_siguiente,
        Reserva.estado != "Cancelada"
    ).all()

def obtener_historial_reservas(db: Session):
    return db.query(Reserva).order_by(
        Reserva.fecha.desc(),
        Reserva.hora.desc()
    ).all()


def obtener_historial_por_cliente(db: Session, cliente_id: int):
    return db.query(Reserva).filter(
        Reserva.cliente_id_cliente == cliente_id
    ).order_by(
        Reserva.fecha.desc(),
        Reserva.hora.desc()
    ).all()

def actualizar_estado_reserva(db: Session, reserva_id: int, nuevo_estado: str):
    reserva = db.query(Reserva).filter(
        Reserva.id_reserva == reserva_id
    ).first()

    if not reserva:
        return None

    reserva.estado = nuevo_estado

    db.commit()
    db.refresh(reserva)

    return reserva

def obtener_reserva_por_id(db: Session, reserva_id: int):
    return db.query(Reserva).filter(
        Reserva.id_reserva == reserva_id
    ).first()
