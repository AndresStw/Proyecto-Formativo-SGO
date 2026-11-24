
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.repositories import reservas as reserva_repository


def crear_reserva(db: Session, datos):

    # 1. Verificar que el cliente exista
    cliente = reserva_repository.obtener_cliente(
        db,
        datos.cliente_id_cliente
    )

    if not cliente:
        raise ValueError("El cliente no existe")

    # 2. Verificar que la mesa exista
    mesa = reserva_repository.obtener_mesa(
        db,
        datos.mesa_id_mesa
    )

    if not mesa:
        raise ValueError("La mesa seleccionada no existe")

    # 3. Verificar que la mesa esté disponible para reservas
    if mesa.estado.capitalize == "fuera de servicio":
        raise ValueError("La mesa está fuera de servicio")

    # 4. Verificar capacidad
    if datos.cantidad_personas > mesa.capacidad:
        raise ValueError(
            "La cantidad de personas supera la capacidad de la mesa"
        )

    # 5. Verificar que la fecha y hora sean futuras
    fecha_hora_inicio = datetime.combine(
        datos.fecha,
        datos.hora
    )

    if fecha_hora_inicio <= datetime.now():
        raise ValueError(
            "La fecha y hora de la reserva deben ser futuras"
        )

    # 6. Calcular duración de la reserva (2 horas)
    fecha_hora_fin = fecha_hora_inicio + timedelta(hours=2)

    # 7. Consultar reservas existentes de esa mesa
    reservas = reserva_repository.obtener_reservas_por_mesa_y_fecha(
        db,
        datos.mesa_id_mesa,
        datos.fecha
    )

    # 8. Verificar que no existan cruces de horarios
    for reserva in reservas:

        reserva_inicio = datetime.combine(
            reserva.fecha,
            reserva.hora
        )

        reserva_fin = reserva_inicio + timedelta(hours=2)

        if (
            fecha_hora_inicio < reserva_fin
            and fecha_hora_fin > reserva_inicio
        ):
            raise ValueError(
                "La mesa ya tiene una reserva en ese horario"
            )

    # 9. Preparar los datos
    nuevos_datos = datos.model_dump()

    # 10. Crear la reserva
    nueva_reserva = reserva_repository.crear_reserva(
        db,
        nuevos_datos
    )

    return nueva_reserva
 # ! Obtener el historial de reservas

def obtener_historial_reservas(db: Session):
    return reserva_repository.obtener_historial_reservas(db)

#! Filtrar por id
def obtener_historial_por_cliente(db: Session, cliente_id: str):
    return reserva_repository.obtener_historial_por_cliente(
        db, cliente_id
    )
# ! Actualizar el estado de reserva

def actualizar_estado_reserva(db: Session, reserva_id: int, nuevo_estado: str):
    estados_permitidos = {
        "Pendiente": ["Confirmada", "Cancelada"],
        "Confirmada": ["Cancelada", "Finalizada", "No asistió"],
        "Cancelada": [],
        "Finalizada": [],
        "No asistió": []
    }

    reserva = reserva_repository.obtener_reserva_por_id(db, reserva_id)

    if not reserva:
        raise ValueError("La reserva no existe")

    if nuevo_estado not in estados_permitidos:
        raise ValueError("El estado seleccionado no es válido")

    if nuevo_estado not in estados_permitidos[reserva.estado]:
        raise ValueError(
            f"No se puede cambiar de {reserva.estado} a {nuevo_estado}"
        )

    return reserva_repository.actualizar_estado_reserva(
        db, reserva_id, nuevo_estado
    )