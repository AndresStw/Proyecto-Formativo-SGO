// src/components/CarruselPedidos.jsx

/*
 ARchivo: CarruselPedidos
  Que hace: Muestra los pedidos del usuario en un carrusel .
    - pedidos: Array de objetos con los datos de los pedidos desde la db.son
    - onSelect: Funcionn que se ejecuta al seleccionar un pedido
 
*/

import { useState, useEffect } from "react";
import "../assets/CSS/carrusel-pedidos.css";

function CarruselPedidos({ pedidos, onSelect }) {
  const [indiceActual, setIndiceActual] = useState(0);
  const [itemsPorPagina, setItemsPorPagina] = useState(3);

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 576) {
        setItemsPorPagina(1);
      } else if (window.innerWidth < 768) {
        setItemsPorPagina(2);
      } else {
        setItemsPorPagina(3);
      }
    };

    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const totalPaginas = Math.ceil(pedidos.length / itemsPorPagina);
  const inicio = indiceActual * itemsPorPagina;
  const fin = inicio + itemsPorPagina;
  const itemsVisibles = pedidos.slice(inicio, fin);

  const irAPagina = (pagina) => {
    if (pagina < 0 || pagina >= totalPaginas) return;
    setIndiceActual(pagina);
  };

  if (pedidos.length === 0) {
    return <p className="text-center text-muted">No hay pedidos disponibles</p>;
  }

  return (
    <div className="carrusel-container">
      <div className="carrusel-track">
        {itemsVisibles.map((pedido) => (
          <div
            key={pedido.id}
            className="carrusel-item"
            onClick={() => onSelect(pedido)}
          >
            <div className="carrusel-card">
              <div className="carrusel-card-image">
                <img
                  src={pedido.imagen || "/assets/Img/platos/default.jpg"}
                  alt={pedido.cliente}
                />
                <span className={`carrusel-badge bg-${pedido.estadoBadge || 'secondary'}`}>
                  {pedido.estado}
                </span>
              </div>
              <div className="carrusel-card-body">
                <div className="carrusel-card-header">
                  <span className="carrusel-id">#{pedido.id}</span>
                  <span className="carrusel-fecha">{pedido.fecha}</span>
                </div>
                <h5 className="carrusel-cliente">{pedido.cliente}</h5>
                <div className="carrusel-items">
                  {pedido.items.slice(0, 2).map((item, idx) => (
                    <span key={idx} className="carrusel-item-tag">
                      {item.nombre} x{item.cantidad}
                    </span>
                  ))}
                  {pedido.items.length > 2 && (
                    <span className="carrusel-more">+{pedido.items.length - 2} más</span>
                  )}
                </div>
                <div className="carrusel-footer">
                  <span className="carrusel-total">
                    <strong>${pedido.total.toLocaleString()}</strong>
                  </span>
                  <span className="carrusel-metodo">
                    <i className="fa-regular fa-credit-card me-1"></i>
                    {pedido.metodoPago}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {totalPaginas > 1 && (
        <div className="carrusel-controles">
          <button
            className="carrusel-btn"
            onClick={() => irAPagina(indiceActual - 1)}
            disabled={indiceActual === 0}
          >
            <i className="fa-solid fa-chevron-left"></i>
          </button>

          <div className="carrusel-dots">
            {Array.from({ length: totalPaginas }).map((_, idx) => (
              <button
                key={idx}
                className={`carrusel-dot ${indiceActual === idx ? 'active' : ''}`}
                onClick={() => irAPagina(idx)}
              />
            ))}
          </div>

          <button
            className="carrusel-btn"
            onClick={() => irAPagina(indiceActual + 1)}
            disabled={indiceActual === totalPaginas - 1}
          >
            <i className="fa-solid fa-chevron-right"></i>
          </button>
        </div>
      )}
    </div>
  );
}

export default CarruselPedidos;