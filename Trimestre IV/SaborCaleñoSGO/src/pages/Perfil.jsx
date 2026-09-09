// src/pages/Perfil.jsx
import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../assets/CSS/perfil.css";

function Perfil() {
  const [user, setUser] = useState(null);
  const [pedidos, setPedidos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }

    // Simular carga de datos del usuario
    const userData = {
      nombre: "Cliente Demo",
      email: "cliente@saborcaleno.com",
      telefono: "300 123 4567",
      puntos: 150
    };
    setUser(userData);

    // Pedidos simulados
    const pedidosData = [
      {
        id: "#1001",
        fecha: "Hoy",
        total: 25000,
        estado: "En preparación",
        estadoBadge: "warning"
      },
      {
        id: "#1000",
        fecha: "Ayer",
        total: 32000,
        estado: "Entregado",
        estadoBadge: "success"
      },
      {
        id: "#999",
        fecha: "15/08/2024",
        total: 18000,
        estado: "Entregado",
        estadoBadge: "success"
      }
    ];
    setPedidos(pedidosData);
    setCargando(false);
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
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
    <div className="container py-5">
      <div className="row g-4">
        {/* Perfil usuario */}
        <div className="col-md-4">
          <div className="perfil-card">
            <div className="perfil-avatar">
              <i className="fa-solid fa-circle-user"></i>
            </div>
            <h4 className="perfil-nombre">{user?.nombre}</h4>
            <p className="perfil-email">{user?.email}</p>
            
            <div className="perfil-puntos">
              <i className="fa-solid fa-star" style={{ color: '#FFD700' }}></i>
              <span>{user?.puntos} puntos</span>
            </div>

            <hr />

            <div className="perfil-detalles">
              <p>
                <i className="fa-solid fa-phone me-2" style={{ color: 'var(--secondary)' }}></i>
                {user?.telefono}
              </p>
            </div>

            <button 
              className="btn-outline-custom w-100 mt-3"
              onClick={handleLogout}
            >
              <i className="fa-solid fa-right-from-bracket me-2"></i> Cerrar Sesión
            </button>
          </div>
        </div>

        {/* Pedidos recientes */}
        <div className="col-md-8">
          <div className="pedidos-card">
            <h5 className="pedidos-titulo">
              <i className="fa-regular fa-clock me-2" style={{ color: 'var(--secondary)' }}></i>
              Mis Pedidos Recientes
            </h5>

            <div className="table-responsive">
              <table className="table perfil-table">
                <thead>
                  <tr>
                    <th>ID Pedido</th>
                    <th>Fecha</th>
                    <th>Total</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {pedidos.map((pedido) => (
                    <tr key={pedido.id}>
                      <td><strong>{pedido.id}</strong></td>
                      <td>{pedido.fecha}</td>
                      <td>${pedido.total.toLocaleString()}</td>
                      <td>
                        <span className={`badge bg-${pedido.estadoBadge} text-dark`}>
                          {pedido.estado}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <Link to="/pedidos" className="pedidos-ver-todos">
              Ver todos los pedidos <i className="fa-solid fa-arrow-right ms-1"></i>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Perfil;