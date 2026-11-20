
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Modelos
from app.models.pedido import Pedido, Detalle_Pedido, Venta
from app.models.catalogos import Estado_Pedido, MetodoPago

# Conexion a la base de datos
from app.infrastructure.database.session import get_db


# ==========================================
# EP-06: OPERACION DE COCINA
# ==========================================

kitchen_router = APIRouter(
    prefix="/kitchen",
    tags=["Kitchen"]
)


# ------------------------------------------
# GET /kitchen/orders
# Consultar pedidos pendientes y en preparacion
# ------------------------------------------

@kitchen_router.get("/orders")
def get_kitchen_orders(db: Session = Depends(get_db)):

    try:

        # 1. Consultar los estados permitidos
        estados = db.query(Estado_Pedido).filter(
            Estado_Pedido.nombre_estado.in_([
                "Pendiente",
                "En preparación"
            ])
        ).all()

        # 2. Obtener los identificadores de los estados
        ids_estados = [estado.id_estado for estado in estados]

        # 3. Consultar los pedidos que tengan esos estados
        pedidos = db.query(Pedido).filter(
            Pedido.id_estado.in_(ids_estados)
        ).order_by(Pedido.fecha_hora.asc()).all()

        # 4. Construir la respuesta de los pedidos
        resultado = []

        for pedido in pedidos:

            # Consultar los detalles de cada pedido
            detalles = db.query(Detalle_Pedido).filter(
                Detalle_Pedido.id_pedido == pedido.id_pedido
            ).all()

            resultado.append({
                "id_pedido": pedido.id_pedido,
                "fecha_hora": (
                    pedido.fecha_hora.isoformat()
                    if pedido.fecha_hora else None
                ),
                "tiempo_preparacion": pedido.tiempo_preparacion,
                "detalles": [
                    {
                        "id_detalle_pedido": detalle.id_detalle_pedido,
                        "cantidad": detalle.cantidad,
                        "observaciones": detalle.observaciones
                    }
                    for detalle in detalles
                ]
            })

        # 5. Retornar respuesta
        return {
            "message": "Pedidos de cocina consultados correctamente",
            "total": len(resultado),
            "orders": resultado
        }

    except SQLAlchemyError:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Error al consultar los pedidos de cocina"
        )


# ------------------------------------------
# PATCH /kitchen/orders/{order_id}/ready
# Cambiar estado del pedido a Listo
# ------------------------------------------

@kitchen_router.patch("/orders/{order_id}/ready")
def mark_order_ready(
    order_id: int,
    db: Session = Depends(get_db)
):

    try:

        # 1. Verificar que el pedido exista
        pedido = db.query(Pedido).filter(
            Pedido.id_pedido == order_id
        ).first()

        if not pedido:
            raise HTTPException(
                status_code=404,
                detail="El pedido no existe"
            )

        # 2. Consultar el estado actual
        estado_actual = db.query(Estado_Pedido).filter(
            Estado_Pedido.id_estado == pedido.id_estado
        ).first()

        if not estado_actual:
            raise HTTPException(
                status_code=404,
                detail="No se encontro el estado actual del pedido"
            )

        # 3. Verificar que el pedido pueda cambiar a Listo
        if estado_actual.nombre_estado not in [
            "Pendiente",
            "En preparación"
        ]:
            raise HTTPException(
                status_code=400,
                detail="El pedido no se encuentra en un estado valido para marcarlo como listo"
            )

        # 4. Buscar el estado Listo
        estado_listo = db.query(Estado_Pedido).filter(
            Estado_Pedido.nombre_estado == "Listo"
        ).first()

        if not estado_listo:
            raise HTTPException(
                status_code=404,
                detail="No existe el estado Listo en los catalogos"
            )

        # 5. Actualizar el estado del pedido
        pedido.id_estado = estado_listo.id_estado

        # 6. Guardar los cambios
        db.commit()
        db.refresh(pedido)

        # 7. Retornar respuesta
        return {
            "message": "El pedido fue marcado como Listo correctamente",
            "order": {
                "id_pedido": pedido.id_pedido,
                "estado": estado_listo.nombre_estado
            }
        }

    except HTTPException:
        raise

    except SQLAlchemyError:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Error al actualizar el estado del pedido"
        )


# ==========================================
# EP-05 / EP-06: REGISTRO DE VENTAS
# ==========================================

cashier_router = APIRouter(
    prefix="/cashier",
    tags=["Cashier"]
)


# ------------------------------------------
# Datos que se reciben para registrar la venta
# ------------------------------------------

class SaleCreate(BaseModel):

    idPedido: int = Field(gt=0)
    idCajero: int = Field(gt=0)
    idMetodoPago: int = Field(gt=0)
    total: Decimal = Field(gt=0)


# ------------------------------------------
# POST /cashier/sales
# Registrar la venta de un pedido
# ------------------------------------------

@cashier_router.post("/sales", status_code=201)
def register_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db)
):

    try:

        # 1. Obtener los datos enviados
        id_pedido = sale.idPedido
        id_cajero = sale.idCajero
        id_metodo_pago = sale.idMetodoPago
        total = sale.total

        # 2. Verificar que el pedido exista
        pedido = db.query(Pedido).filter(
            Pedido.id_pedido == id_pedido
        ).first()

        if not pedido:
            raise HTTPException(
                status_code=404,
                detail="El pedido no existe"
            )

        # 3. Verificar el estado del pedido
        estado_pedido = db.query(Estado_Pedido).filter(
            Estado_Pedido.id_estado == pedido.id_estado
        ).first()

        if not estado_pedido:
            raise HTTPException(
                status_code=404,
                detail="No se encontro el estado del pedido"
            )

        if estado_pedido.nombre_estado not in [
            "Listo",
            "Entregado"
        ]:
            raise HTTPException(
                status_code=400,
                detail="Solo se pueden registrar ventas de pedidos Listos o Entregados"
            )

        # 4. Verificar que el pedido no tenga una venta registrada
        venta_existente = db.query(Venta).filter(
            Venta.idPedido == id_pedido
        ).first()

        if venta_existente:
            raise HTTPException(
                status_code=409,
                detail="Este pedido ya tiene una venta registrada"
            )

        # 5. Verificar que el metodo de pago exista
        metodo_pago = db.query(MetodoPago).filter(
            MetodoPago.idMetodoPago == id_metodo_pago
        ).first()

        if not metodo_pago:
            raise HTTPException(
                status_code=404,
                detail="El metodo de pago no existe"
            )

        # 6. Crear el registro de venta
        nueva_venta = Venta(
            fecha=datetime.now(),
            total=total,
            idPedido=id_pedido,
            idCajero=id_cajero,
            idMetodoPago=id_metodo_pago
        )

        # 7. Guardar la venta
        db.add(nueva_venta)
        db.commit()
        db.refresh(nueva_venta)

        # 8. Retornar respuesta
        return {
            "message": "Venta registrada correctamente",
            "sale": {
                "idVenta": nueva_venta.idVenta,
                "fecha": nueva_venta.fecha.isoformat(),
                "total": float(nueva_venta.total),
                "idPedido": nueva_venta.idPedido,
                "idMetodoPago": nueva_venta.idMetodoPago,
                "idCajero": nueva_venta.idCajero
            }
        }

    except HTTPException:
        raise

    except SQLAlchemyError:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Error al registrar la venta"
        )
