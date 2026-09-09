// src/Components/CartItem.jsx

/*
  
 Que hace: Muestra un item individual dentro del carrito de compras.
    - item: Objeto con los datos del producto (nombre, descripcion, precio, cantidad)
    - onRemove: Funcion para eliminar el producto del carrito
    - onUpdateCantidad: Funcion para actualizar la cantidad del producto

*/

import React from "react";
import "../assets/CSS/cart-item.css";

function CartItem({ item, onRemove, onUpdateCantidad }) {
  return (
    <div className="cart-item">
      <div className="cart-item-info">
        <h5 className="cart-item-name">{item.nombre}</h5>
        <p className="cart-item-desc">{item.descripcion}</p>
        <span className="cart-item-price">+ ${item.precio}</span>
      </div>

      <div className="cart-item-actions">
        <button
          className="btn btn-outline-secondary btn-sm"
          onClick={() => onUpdateCantidad(item.id, (item.cantidad || 1) - 1)}
          disabled={(item.cantidad || 1) <= 1}
        >
          −
        </button>
        <span className="cart-item-qty">{item.cantidad || 1}</span>
        <button
          className="btn btn-outline-secondary btn-sm"
          onClick={() => onUpdateCantidad(item.id, (item.cantidad || 1) + 1)}
        >
          +
        </button>
        <button
          className="btn btn-danger btn-sm ms-2"
          onClick={() => {
            if (window.confirm(`¿Eliminar "${item.nombre}" del carrito?`)) {
              onRemove(item.id);
            }
          }}
        >
          <i className="fa-solid fa-trash-can"></i>
        </button>
      </div>
    </div>
  );
}

export default CartItem;