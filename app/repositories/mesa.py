from sqlalchemy.orm import Session
from app.models.mesa import Mesa
from app.models.user import User

def obtener_mesas(db: Session):
    return db.query(Mesa).all()


def obtener_mesa_por_id(db: Session, mesa_id: int):
    return db.query(Mesa).filter(
        Mesa.id_mesa == mesa_id
    ).first()

def actualizar_estado_mesa(db: Session, mesa_id: int, nuevo_estado: str):
    mesa = db.query(Mesa).filter( #! Filtra por id de mesa para consultar 
        Mesa.id_mesa == mesa_id
    ).first()

    if not mesa:
        return None # ! Si la mesa no existe devuelve none

    mesa.estado = nuevo_estado # !Actualiza el estado de la mesa

    db.commit()
    db.refresh(mesa)

    return mesa

def obtener_mesa_por_numero(db: Session, numero_mesa: str):
    return db.query(Mesa).filter(
        Mesa.numero_mesa == numero_mesa
    ).first()


def obtener_mesero(db: Session, mesero_id: int):
    return db.query(User).filter(
        User.id == mesero_id
    ).first()


def crear_mesa(db: Session, datos: dict):
    nueva_mesa = Mesa(**datos)

    db.add(nueva_mesa)
    db.commit()
    db.refresh(nueva_mesa)

    return nueva_mesa


def actualizar_mesa(db: Session, mesa: Mesa, datos: dict):
    for campo, valor in datos.items():
        setattr(mesa, campo, valor)

    db.commit()
    db.refresh(mesa)

    return mesa


def eliminar_mesa(db: Session, mesa: Mesa):
    db.delete(mesa)
    db.commit()