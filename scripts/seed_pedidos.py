"""
Carga los catálogos de pedidos (EP-03): modalidades y estados.

Uso (desde la raíz del proyecto):
    python -m scripts.seed_pedidos
"""

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.domain.enums.pedidos import EstadoPedidoNombre, ModalidadPedidoNombre
from app.infrastructure.database.session import SessionLocal
from app.models.catalogos import Estado_Pedido, modalidadPedido


def sembrar_catalogos() -> None:
    db = SessionLocal()

    try:
        creados = []

        for modalidad in ModalidadPedidoNombre:
            existe = db.scalar(
                select(modalidadPedido).where(
                    modalidadPedido.nombre_modalidad == modalidad.value 
                )
            )
            if existe is None:
                db.add(modalidadPedido(nombre_modalidad=modalidad.value))
                creados.append(f"modalidad: {modalidad.value}")

        for estado in EstadoPedidoNombre:
            existe = db.scalar(
                select(Estado_Pedido).where(
                    Estado_Pedido.nombre_estado == estado.value
                )
            )
            if existe is None:
                db.add(Estado_Pedido(nombre_estado=estado.value))
                creados.append(f"estado: {estado.value}")

        db.commit()

        if creados:
            print("Registros creados:")
            for linea in creados:
                print(f"  - {linea}")
        else:
            print("Los catálogos ya estaban completos.")

    except SQLAlchemyError as error:
        db.rollback()
        print(f"Error al sembrar los catálogos: {error}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    sembrar_catalogos()