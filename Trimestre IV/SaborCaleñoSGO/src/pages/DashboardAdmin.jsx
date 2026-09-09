// src/pages/DashboardAdmin.jsx

/*
  EEEEEEEEEEEEESTEEEE va en la aplicacion movil.requiere rol aadmin
*/

import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import "../assets/CSS/dashboard.css";

function DashboardAdmin() {
  const [user, setUser] = useState(null);
  const [stats, setStats] = useState({
    ventas: 0,
    pedidosActivos: 0,
    mesasReservadas: 0,
    totalPedidos: 0
  });
  const [pedidosRecientes, setPedidosRecientes] = useState([]);
  const [cargando, setCargando] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }

    setUser({
      nombre: "Administrador",
      email: "admin@saborcaleno.com",
      rol: "Administrador"
    });

    setStats({
      ventas: 450000,
      pedidosActivos: 4,
      mesasReservadas: 3,
      totalPedidos: 12
    });

    setPedidosRecientes([
      {
        id: "#2048",
        cliente: "Carlos Mario",
        detalle: "1 Chuleta Valluna, 2 Champús",
        total: 38000,
        estado: "Pendiente"
      },
      {
        id: "#2047",
        cliente: "Ana Restrepo",
        detalle: "2 Sancocho de Pescado",
        total: 50000,
        estado: "En preparación"
      },
      {
        id: "#2046",
        cliente: "Juan Pérez",
        detalle: "1 Caldo de costilla",
        total: 9000,
        estado: "Listo"
      },
      {
        id: "#2045",
        cliente: "María González",
        detalle: "1 Chuleta Valluna, 1 Champús",
        total: 30000,
        estado: "Entregado"
      }
    ]);

    setCargando(false);
  }, [navigate]);

  const getEstadoBadge = (estado) => {
    const estados = {
      "Pendiente": "warning",
      "En preparación": "info",
      "Listo": "success",
      "Entregado": "success",
      "Cancelado": "danger"
    };
    return estados[estado] || "secondary";
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
    <div className="dashboard-container">
      <div className="container-fluid">
        <div className="row">
          <nav className="col-md-3 col-lg-2 d-md-block bg-white sidebar-admin">
            <div className="sidebar-sticky pt-3">
              <div className="text-center mb-4 pb-3 border-bottom">
                <i className="fa-solid fa-user-gear text-dark fs-1 mb-2"></i>
                <h6 className="fw-bold mb-0">{user?.nombre}</h6>
                <span className="badge bg-warning text-dark">{user?.rol}</span>
              </div>

              <ul className="nav flex-column gap-2">
                <li className="nav-item">
                  <Link className="nav-link active" to="/admin">
                    <i className="fa-solid fa-chart-line me-2"></i> Dashboard
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/admin/platos">
                    <i className="fa-solid fa-utensils me-2"></i> Gestión Platos
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/admin/categorias">
                    <i className="fa-solid fa-tags me-2"></i> Categorías
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/admin/pedidos">
                    <i className="fa-solid fa-receipt me-2"></i> Pedidos
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/admin/reservas">
                    <i className="fa-solid fa-calendar-check me-2"></i> Reservas
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/admin/usuarios">
                    <i className="fa-solid fa-users me-2"></i> Usuarios
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/admin/reportes">
                    <i className="fa-solid fa-file-invoice-dollar me-2"></i> Reportes
                  </Link>
                </li>
              </ul>
            </div>
          </nav>

          <main className="col-md-9 ms-sm-auto col-lg-10 px-md-4 py-4">
            <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
              <h1 className="dashboard-title">Panel de Control General</h1>
            </div>

            <div className="row g-4 mb-4">
              <div className="col-md-3 col-sm-6">
                <div className="stat-card" style={{ borderLeftColor: 'var(--secondary)' }}>
                  <span className="stat-label">Ventas del Día</span>
                  <h3 className="stat-value">${stats.ventas.toLocaleString()}</h3>
                  <span className="stat-change text-success">
                    <i className="fa-solid fa-arrow-up"></i> +12% vs ayer
                  </span>
                </div>
              </div>
              <div className="col-md-3 col-sm-6">
                <div className="stat-card" style={{ borderLeftColor: '#3B82F6' }}>
                  <span className="stat-label">Pedidos Activos</span>
                  <h3 className="stat-value">{stats.pedidosActivos}</h3>
                  <span className="stat-change text-warning">En cocina y envíos</span>
                </div>
              </div>
              <div className="col-md-3 col-sm-6">
                <div className="stat-card" style={{ borderLeftColor: '#8B5CF6' }}>
                  <span className="stat-label">Mesas Reservadas Hoy</span>
                  <h3 className="stat-value">{stats.mesasReservadas} Mesas</h3>
                  <span className="stat-change text-muted">Para jornada de la noche</span>
                </div>
              </div>
              <div className="col-md-3 col-sm-6">
                <div className="stat-card" style={{ borderLeftColor: '#10B981' }}>
                  <span className="stat-label">Total Pedidos</span>
                  <h3 className="stat-value">{stats.totalPedidos}</h3>
                  <span className="stat-change text-success">Este mes</span>
                </div>
              </div>
            </div>

            <div className="dashboard-table">
              <h5 className="fw-bold mb-3 text-secondary">
                <i className="fa-regular fa-receipt me-2"></i>
                Control Operativo de Pedidos
              </h5>

              <div className="table-responsive">
                <table className="table align-middle">
                  <thead className="table-light">
                    <tr>
                      <th># Orden</th>
                      <th>Cliente</th>
                      <th>Detalle</th>
                      <th>Total</th>
                      <th>Estado</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {pedidosRecientes.map((pedido) => (
                      <tr key={pedido.id}>
                        <td><b>{pedido.id}</b></td>
                        <td>{pedido.cliente}</td>
                        <td>{pedido.detalle}</td>
                        <td>${pedido.total.toLocaleString()}</td>
                        <td>
                          <span className={`badge bg-${getEstadoBadge(pedido.estado)}`}>
                            {pedido.estado}
                          </span>
                        </td>
                        <td>
                          <button className="btn btn-sm btn-outline-primary">
                            <i className="fa-regular fa-eye"></i>
                          </button>
                          <button className="btn btn-sm btn-outline-warning ms-1">
                            <i className="fa-solid fa-pen"></i>
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}

export default DashboardAdmin;