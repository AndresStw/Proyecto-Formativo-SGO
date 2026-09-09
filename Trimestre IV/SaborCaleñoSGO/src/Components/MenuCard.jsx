// src/Components/MenuCard.jsx

/*
     Tarjeta que muestra la informacion de un producto del menu.
    - producto: Objeto con los datos del producto 
    - onAgregar: Función que se ejecuta al hacer clic en /Agregar
    - Muestra imagen, nombre, descripcion y precio del producto
    - calificacion, tiempo de preparacion y calorias
    - Boton /Agregars que añade el producto al carrito
*/

import React from "react";
import { PiStarThin } from "react-icons/pi";
import { CiTimer } from "react-icons/ci";
import { FaFire } from "react-icons/fa";
import "../assets/CSS/menu-card.css";

function MenuCard({ producto, onAgregar }) {
  const imagenDefault = producto.imagen || "/assets/Img/platos/default.jpg";

  return (
    <div className="menu-card">
      <div className="menu-card-image">
        <img src={imagenDefault} alt={producto.nombre} />
        {producto.badge && (
          <span className="menu-card-badge">{producto.badge}</span>
        )}
      </div>

      <div className="menu-card-body">
        <div className="menu-card-header">
          <h4 className="menu-card-title">{producto.nombre}</h4>
          <span className="menu-card-price">${producto.precio}</span>
        </div>

        <p className="menu-card-desc">{producto.descripcion}</p>

        <div className="menu-card-footer">
          <div className="menu-card-meta">
            <span className="badge-cal">
              <PiStarThin /> {producto.rating || "4.5"}
            </span>
            <span className="badge-cal">
              <CiTimer /> {producto.tiempo || "30min"}
            </span>
            <span className="badge-cal">
              <FaFire /> {producto.calorias || "300"} Kcal
            </span>
          </div>

          <button
            className="btn-agregar"
            onClick={() => onAgregar(producto)}
          >
            <i className="fa-solid fa-plus me-1"></i> Agregar
          </button>
        </div>
      </div>
    </div>
  );
}

export default MenuCard;