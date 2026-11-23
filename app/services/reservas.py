
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

    # 3. Verificar la capacidad de la mesa
    if datos.cantidad_personas > mesa.capacidad:
        raise ValueError(
            "La cantidad de personas supera la capacidad de la mesa"
        )

    # 4. Verificar que la fecha y hora sean futuras
    fecha_hora_inicio = datetime.combine(
        datos.fecha,
        datos.hora
    )

    if fecha_hora_inicio <= datetime.now():
        raise ValueError(
            "La fecha y hora de la reserva deben ser futuras"
        )

    # 5. Calcular la duración de la reserva (2 horas)
    fecha_hora_fin = fecha_hora_inicio + timedelta(hours=2)

    # 6. Consultar reservas existentes
    reservas = reserva_repository.obtener_reservas_por_mesa_y_fecha(
        db,
        datos.mesa_id_mesa,
        datos.fecha
    )

    # 7. Verificar cruces de horarios
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

    # 8. Preparar los datos
    nuevos_datos = datos.model_dump()

    # 9. Crear la reserva
    nueva_reserva = reserva_repository.crear_reserva(
        db,
        nuevos_datos
    )

    return nueva_reserva
