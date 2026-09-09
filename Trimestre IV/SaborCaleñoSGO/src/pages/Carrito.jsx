// src/pages/Carrito.jsx

/*
  
   Pagina del carrito de compras.
    - Muestra los productos agregados al carrito
    - Permite actualizar cantidades (+, -)
    - Eliminar productos del carrito
    - Calcula subtotal y total automaticamente
    - Botnn para proceder al pago (redirige a placing-order)
  */

import { useState, useEffect } from "react";
import { Link, useNavigate }from "react-router-dom";
import CartItem from "../Components/CartItem";
import "../assets/CSS/carrito.css";

function Carrito() {
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [subtotal, setSubtotal] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    const carritoGuardado = localStorage.getItem("carrito");
    if (carritoGuardado) {
      const carrito = JSON.parse(carritoGuardado);
      setItems(carrito);
      calcularTotales(carrito);
    }
  }, []);

  const calcularTotales = (carrito) => {
    const nuevoSubtotal = carrito.reduce((acc, item) => {
      return acc + (item.precio * (item.cantidad || 1));
    }, 0);
    setSubtotal(nuevoSubtotal);
    setTotal(nuevoSubtotal);
  };

  const guardarCarrito = (nuevoCarrito) => {
    localStorage.setItem("carrito", JSON.stringify(nuevoCarrito));
    setItems(nuevoCarrito);
    calcularTotales(nuevoCarrito);
  };

  const handleUpdateCantidad = (id, nuevaCantidad) => {
    if (nuevaCantidad < 1) {
      handleRemove(id);
      return;
    }
    
    const nuevoCarrito = items.map(item => 
      item.id === id ? { ...item, cantidad: nuevaCantidad } : item
    );
    guardarCarrito(nuevoCarrito);
  };

  const handleRemove = (id) => {
    const nuevoCarrito = items.filter(item => item.id !== id);
    guardarCarrito(nuevoCarrito);
  };

  const handleCheckout = () => {
    if (items.length === 0) {
      alert("Tu carrito está vacío");
      return;
    }
    navigate("/placing-order");
  };

  if (items.length === 0) {
    return (
      <div className="container py-5">
        <div className="carrito-vacio text-center">
          <i className="fa-solid fa-basket-shopping carrito-icon"></i>
          <h3>Tu carrito esta vacío</h3>
          <p className="text-muted">¡Agrega algun producto!</p>
          <Link to="/menu">
            <button className="btn-primary-custom">
              <i className="fa-solid fa-utensils me-2"></i> Ver Menú
            </button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container py-5">
      <h2 className="carrito-titulo">
        <i className="fa-solid fa-basket-shopping me-2"></i>
        Mi Pedido
      </h2>

      <div className="row g-4">
        <div className="col-lg-8">
          <div className="carrito-items">
            {items.map((item) => (
              <CartItem
                key={item.id}
                item={item}
                onRemove={handleRemove}
                onUpdateCantidad={handleUpdateCantidad}
              />
            ))}
          </div>
        </div> <br />

        <div className="col-lg-4">
          <div className="carrito-resumen">
            <h5 className="resumen-titulo">Resumen de Compra</h5>
            <hr />
            
            <div className="resumen-linea">
              <span>Subtotal</span>
              <span>${subtotal.toLocaleString()}</span>
            </div>
            
            <div className="resumen-linea">
              <span>Envío</span>
              <span className="text-success">Gratis</span>
            </div>
            
            <hr />
            
            <div className="resumen-total">
              <span className="fw-bold fs-5">Total</span>
              <span className="fw-bold fs-4" style={{ color: 'var(--secondary)' }}>
                ${total.toLocaleString()}
              </span>
            </div>

            <button 
              className="btn-primary-custom w-100 mt-3"
              onClick={handleCheckout}
            >
              <i className="fa-solid fa-credit-card me-2"></i> Proceder al Pago
            </button>
            
            <Link to="/menu" className="btn-outline-custom w-100 mt-2 text-center">
              <i className="fa-solid fa-arrow-left me-1"></i> Seguir Comprando
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Carrito;