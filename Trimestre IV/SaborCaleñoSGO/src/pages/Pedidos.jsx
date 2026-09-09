// src/pages/Pedidos.jsx
import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import CarruselPedidos from "../components/CarruselPedidos";
import "../assets/CSS/pedidos.css";

function Pedidos() {
  const [pedidos, setPedidos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [pedidoSeleccionado, setPedidoSeleccionado] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }

    const userEmail = localStorage.getItem("userEmail");

    fetch("http://localhost:3000/pedidos")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Error al cargar los pedidos");
        }
        return response.json();
      })
      .then((data) => {
        let pedidosFiltrados = [];
        
        if (userEmail) {
          pedidosFiltrados = data.filter(
            (pedido) => pedido.usuarioEmail === userEmail
          );
        } else {
          pedidosFiltrados = data;
        }

        setPedidos(pedidosFiltrados);
        if (pedidosFiltrados.length > 0) {
          setPedidoSeleccionado(pedidosFiltrados[0]);
        }
        setCargando(false);
      })
      .catch((err) => {
        console.error("Error:", err);
        setError(err.message);
        setCargando(false);
      });
  }, [navigate]);

  const getEstadoBadge = (estado) => {
    const estados = {
      "Entregado": "success",
      "En preparación": "warning",
      "Pendiente": "warning",
      "Cancelado": "danger",
      "En camino": "info"
    };
    return estados[estado] || "secondary";
  };

  if (cargando) {
    return (
      <div className="container text-center py-5">
        <div className="spinner-border text-warning" role="status">
          <span className="visually-hidden">Cargando...</span>
        </div>
        <p>Cargando pedidos...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container text-center py-5">
        <div className="alert alert-danger">
          <i className="fa-solid fa-circle-exclamation me-2"></i>
          {error}
        </div>
        <button 
          className="btn btn-primary"
          onClick={() => window.location.reload()}
        >
          Reintentar
        </button>
      </div>
    );
  }

  return (
    <div className="pedidos-container">
      <div className="container py-4">
        <div className="pedidos-header">
          <h2 className="pedidos-titulo">
            <i className="fa-regular fa-receipt me-2" style={{ color: 'var(--secondary)' }}></i>
            Mis Pedidos
          </h2>
          <p className="pedidos-subtitulo">Tus pedidos realizados en Sabor Caleño</p>
        </div>

        {pedidos.length === 0 ? (
          <div className="pedidos-vacio text-center py-5">
            <i className="fa-regular fa-receipt" style={{ fontSize: '4rem', color: 'var(--text-light)' }}></i>
            <h4 className="mt-3">No tienes pedidos aún</h4>
            <p className="text-muted">¡Realiza tu primer pedido y disfruta de la mejor sazón!</p>
            <Link to="/menu">
              <button className="btn-primary-custom mt-2">
                <i className="fa-solid fa-utensils me-2"></i> Ver Menú
              </button>
            </Link>
          </div>
        ) : (
          <>
            <CarruselPedidos
              pedidos={pedidos}
              onSelect={setPedidoSeleccionado}
            />

            {pedidoSeleccionado && (
              <div className="pedido-detalle">
                <div className="pedido-detalle-header">
                  <h4>
                    <i className="fa-regular fa-receipt me-2" style={{ color: 'var(--secondary)' }}></i>
                    Detalle del Pedido #{pedidoSeleccionado.id}
                  </h4>
                  <span className={`badge bg-${getEstadoBadge(pedidoSeleccionado.estado)}`}>
                    {pedidoSeleccionado.estado}
                  </span>
                </div>

                <div className="pedido-detalle-grid">
                  <div className="pedido-detalle-info">
                    <p><strong>Cliente:</strong> {pedidoSeleccionado.cliente}</p>
                    <p><strong>Fecha:</strong> {pedidoSeleccionado.fecha}</p>
                    <p><strong>Método de pago:</strong> {pedidoSeleccionado.metodoPago}</p>
                  </div>

                  <div className="pedido-detalle-items">
                    <h6>Items del pedido</h6>
                    {pedidoSeleccionado.items.map((item, index) => (
                      <div key={index} className="detalle-item">
                        <span className="detalle-item-nombre">{item.nombre}</span>
                        <span className="detalle-item-cantidad">x{item.cantidad}</span>
                        <span className="detalle-item-precio">${item.precio.toLocaleString()}</span>
                      </div>
                    ))}
                  </div>

                  <div className="pedido-detalle-total">
                    <span className="text-muted">Total:</span>
                    <span className="fw-bold fs-4" style={{ color: 'var(--secondary)' }}>
                      ${pedidoSeleccionado.total.toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default Pedidos;