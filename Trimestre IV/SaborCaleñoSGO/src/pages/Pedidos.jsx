import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import CarruselPedidos from "../components/CarruselPedidos";
import { authFetch, getUser } from "../services/Auth";
import "../assets/CSS/pedidos.css";

function Pedidos() {
  const [pedidos, setPedidos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [pedidoSeleccionado, setPedidoSeleccionado] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const userEmail = getUser()?.email || localStorage.getItem("userEmail");
    authFetch("/pedidos")
      .then((response) => {
        if (!response.ok) throw new Error("Error al cargar los pedidos");
        return response.json();
      })
      .then((data) => {
        const propios = userEmail
          ? data.filter((pedido) => pedido.usuarioEmail === userEmail)
          : [];
        setPedidos(propios);
        setPedidoSeleccionado(propios[0] || null);
      })
      .catch((err) => {
        setError(err.message);
        if (!localStorage.getItem("token"))
          navigate("/login", { replace: true });
      })
      .finally(() => setCargando(false));
  }, [navigate]);

  const getEstadoBadge = (estado) =>
    ({
      Entregado: "success",
      "En preparación": "warning",
      Pendiente: "warning",
      Cancelado: "danger",
      "En camino": "info",
    })[estado] || "secondary";
  if (cargando)
    return (
      <div className="container text-center py-5">
        <div className="spinner-border text-warning" role="status"></div>
        <p>Cargando pedidos...</p>
      </div>
    );
  if (error)
    return (
      <div className="container text-center py-5">
        <div className="alert alert-danger">{error}</div>
        <button
          className="btn btn-primary"
          onClick={() => window.location.reload()}
        >
          Reintentar
        </button>
      </div>
    );
  return (
    <div className="pedidos-container">
      <div className="container py-4">
        <div className="pedidos-header">
          <h2 className="pedidos-titulo">Mis Pedidos</h2>
          <p className="pedidos-subtitulo">
            Tus pedidos realizados en Sabor Caleño
          </p>
        </div>
        {pedidos.length === 0 ? (
          <div className="pedidos-vacio text-center py-5">
            <h4>No tienes pedidos aún</h4>
            <p className="text-muted">¡Realiza tu primer pedido!</p>
            <Link to="/menu">
              <button className="btn-primary-custom mt-2">Ver Menú</button>
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
                  <h4>Detalle del Pedido #{pedidoSeleccionado.id}</h4>
                  <span
                    className={`badge bg-${getEstadoBadge(pedidoSeleccionado.estado)}`}
                  >
                    {pedidoSeleccionado.estado}
                  </span>
                </div>
                <div className="pedido-detalle-grid">
                  <div className="pedido-detalle-info">
                    <p>
                      <strong>Cliente:</strong> {pedidoSeleccionado.cliente}
                    </p>
                    <p>
                      <strong>Fecha:</strong> {pedidoSeleccionado.fecha}
                    </p>
                    <p>
                      <strong>Método de pago:</strong>{" "}
                      {pedidoSeleccionado.metodoPago}
                    </p>
                  </div>
                  <div className="pedido-detalle-items">
                    <h6>Items del pedido</h6>
                    {pedidoSeleccionado.items.map((item, index) => (
                      <div key={index} className="detalle-item">
                        <span>{item.nombre}</span>
                        <span>x{item.cantidad}</span>
                        <span>${item.precio.toLocaleString()}</span>
                      </div>
                    ))}
                  </div>
                  <div className="pedido-detalle-total">
                    <span>Total:</span>
                    <span className="fw-bold fs-4">
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
