// src/pages/Cocinero.jsx

/*
 
*/

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../assets/CSS/cocinero.css";

function Cocinero() {
  const [pedidos, setPedidos] = useState([]);
  const [pendientes, setPendientes] = useState(0);
  const [listos, setListos] = useState(0);
  const [cargando, setCargando] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }

    const pedidosData = [
      {
        id: "#2048",
        cliente: "Carlos Mario",
        items: [
          { nombre: "Chuleta Valluna", cantidad: 2, precio: 22000 },
          { nombre: "Champús Caleño", cantidad: 3, precio: 8000 }
        ],
        total: 68000,
        estado: "Pendiente",
        hora: "12:45 PM",
        notas: "Sin cebolla"
      },
      {
        id: "#2047",
        cliente: "Ana Restrepo",
        items: [
          { nombre: "Sancocho de Pescado", cantidad: 2, precio: 25000 },
          { nombre: "Arroz Atollado", cantidad: 1, precio: 28000 }
        ],
        total: 78000,
        estado: "Pendiente",
        hora: "12:30 PM",
        notas: ""
      },
      {
        id: "#2046",
        cliente: "Juan Pérez",
        items: [
          { nombre: "Caldo de costilla", cantidad: 1, precio: 9000 }
        ],
        total: 9000,
        estado: "Pendiente",
        hora: "12:15 PM",
        notas: "Extra aguacate"
      },
      {
        id: "#2045",
        cliente: "María González",
        items: [
          { nombre: "Chuleta Valluna", cantidad: 1, precio: 22000 },
          { nombre: "Champús Caleño", cantidad: 1, precio: 8000 }
        ],
        total: 30000,
        estado: "Listo",
        hora: "11:45 AM",
        notas: ""
      }
    ];

    setPedidos(pedidosData);
    actualizarContadores(pedidosData);
    setCargando(false);
  }, [navigate]);

  const actualizarContadores = (lista) => {
    const pend = lista.filter(p => p.estado === "Pendiente").length;
    const list = lista.filter(p => p.estado === "Listo").length;
    setPendientes(pend);
    setListos(list);
  };

  const handleMarcarListo = (id) => {
    const nuevosPedidos = pedidos.map(pedido => {
      if (pedido.id === id) {
        return { ...pedido, estado: "Listo" };
      }
      return pedido;
    });
    setPedidos(nuevosPedidos);
    actualizarContadores(nuevosPedidos);
  };

  const getEstadoBadge = (estado) => {
    return estado === "Pendiente" ? "warning" : "success";
  };

  if (cargando) {
    return (
      <div className="container text-center py-5">
        <div className="spinner-border text-warning" role="status">
          <span className="visually-hidden">Cargando...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="cocinero-container">
      <div className="container py-4">
        <div className="cocinero-header">
          <div>
            <h1 className="cocinero-titulo">
              <i className="fa-solid fa-kitchen-set me-2" style={{ color: 'var(--secondary)' }}></i>
              Panel Cocinero
            </h1>
            <p className="cocinero-subtitulo">Gestiona los pedidos que llegan a cocina</p>
          </div>
          <div className="cocinero-admin">
            <i className="fa-solid fa-circle-user me-2"></i>
            <span>Cocinero</span>
          </div>
        </div>

        <div className="row g-4 mb-4">
          <div className="col-md-4">
            <div className="card-resumen" style={{ borderLeftColor: 'var(--secondary)' }}>
              <i className="fa-solid fa-clock" style={{ color: 'var(--secondary)' }}></i>
              <div>
                <h3>{pendientes}</h3>
                <p>Pedidos pendientes</p>
              </div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card-resumen" style={{ borderLeftColor: '#10B981' }}>
              <i className="fa-solid fa-check" style={{ color: '#10B981' }}></i>
              <div>
                <h3>{listos}</h3>
                <p>Pedidos listos</p>
              </div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card-resumen" style={{ borderLeftColor: '#3B82F6' }}>
              <i className="fa-solid fa-bowl-food" style={{ color: '#3B82F6' }}></i>
              <div>
                <h3>{pedidos.length}</h3>
                <p>Total de pedidos</p>
              </div>
            </div>
          </div>
        </div>

        <div className="cocinero-pedidos">
          <div className="cocinero-pedidos-header">
            <h5>Pedidos en cocina</h5>
            <p>Marca cada pedido como listo cuando termines de prepararlo</p>
          </div>

          <div className="pedidos-grid">
            {pedidos.filter(p => p.estado === "Pendiente").length === 0 ? (
              <div className="text-center py-4">
                <i className="fa-regular fa-circle-check" style={{ fontSize: '3rem', color: '#10B981' }}></i>
                <h5 className="mt-2">¡Todos los pedidos están listos!</h5>
                <p className="text-muted">No hay pedidos pendientes en cocina</p>
              </div>
            ) : (
              pedidos.filter(p => p.estado === "Pendiente").map((pedido) => (
                <div key={pedido.id} className="pedido-cocina">
                  <div className="pedido-cocina-header">
                    <div className="pedido-cocina-id">
                      <span className="fw-bold">{pedido.id}</span>
                      <span className="pedido-cocina-hora">
                        <i className="fa-regular fa-clock me-1"></i> {pedido.hora}
                      </span>
                    </div>
                    <span className="badge bg-warning text-dark">Pendiente</span>
                  </div>

                  <div className="pedido-cocina-cliente">
                    <i className="fa-regular fa-user me-1"></i> {pedido.cliente}
                  </div>

                  <div className="pedido-cocina-items">
                    {pedido.items.map((item, index) => (
                      <div key={index} className="pedido-cocina-item">
                        <span>{item.nombre}</span>
                        <span className="badge bg-secondary">x{item.cantidad}</span>
                      </div>
                    ))}
                  </div>

                  {pedido.notas && (
                    <div className="pedido-cocina-notas">
                      <i className="fa-regular fa-note-sticky me-1"></i>
                      <span className="text-muted">{pedido.notas}</span>
                    </div>
                  )}

                  <div className="pedido-cocina-footer">
                    <span className="pedido-cocina-total">
                      Total: <strong>${pedido.total.toLocaleString()}</strong>
                    </span>
                    <button
                      className="btn-success-custom btn-sm"
                      onClick={() => handleMarcarListo(pedido.id)}
                    >
                      <i className="fa-solid fa-check me-1"></i> Marcar Listo
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Cocinero;