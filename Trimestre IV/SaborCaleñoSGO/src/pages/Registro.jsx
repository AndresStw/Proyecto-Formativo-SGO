// src/pages/Registro.jsx
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../assets/CSS/registro.css";

function Registro() {
  const [nombre, setNombre] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [telefono, setTelefono] = useState("");
  const [error, setError] = useState("");
  const [exito, setExito] = useState(false);
  const [cargando, setCargando] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setCargando(true);

    // Validaciones básicas
    if (password.length < 6) {
      setError("La contraseña debe tener al menos 6 caracteres");
      setCargando(false);
      return;
    }

    try {
      const response = await fetch("http://localhost:3000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
          email, 
          password,
          nombre,
          telefono
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Guardar el token
        localStorage.setItem("token", data.accessToken);
        setExito(true);
        setTimeout(() => {
          navigate("/menu");
        }, 1500);
      } else {
        setError(data.message || "Error al registrarse. El correo podría estar en uso.");
      }
    } catch (err) {
      setError("Error de conexión. Asegúrate que el servidor está corriendo.");
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-md-6 col-lg-5">
          <div className="registro-card">
            <div className="registro-header">
              <h3 className="registro-title">Crear Cuenta</h3>
              <p className="registro-subtitle">Regístrate para disfrutar de la mejor sazón valluna</p>
            </div>

            {error && (
              <div className="alert alert-danger" role="alert">
                <i className="fa-solid fa-circle-exclamation me-2"></i>
                {error}
              </div>
            )}

            {exito && (
              <div className="alert alert-success" role="alert">
                <i className="fa-solid fa-circle-check me-2"></i>
                ¡Registro exitoso! Redirigiendo al menú...
              </div>
            )}

            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label htmlFor="nombre" className="form-label fw-semibold">
                  <i className="fa-regular fa-user me-1"></i> Nombre Completo
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="nombre"
                  placeholder="Juan Pérez"
                  value={nombre}
                  onChange={(e) => setNombre(e.target.value)}
                  required
                />
              </div>

              <div className="mb-3">
                <label htmlFor="telefono" className="form-label fw-semibold">
                  <i className="fa-solid fa-phone me-1"></i> Teléfono
                </label>
                <input
                  type="tel"
                  className="form-control"
                  id="telefono"
                  placeholder="300 123 4567"
                  value={telefono}
                  onChange={(e) => setTelefono(e.target.value)}
                />
              </div>

              <div className="mb-3">
                <label htmlFor="email" className="form-label fw-semibold">
                  <i className="fa-regular fa-envelope me-1"></i> Correo Electrónico
                </label>
                <input
                  type="email"
                  className="form-control"
                  id="email"
                  placeholder="correo@ejemplo.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>

              <div className="mb-3">
                <label htmlFor="password" className="form-label fw-semibold">
                  <i className="fa-solid fa-lock me-1"></i> Contraseña
                </label>
                <input
                  type="password"
                  className="form-control"
                  id="password"
                  placeholder="Mínimo 6 caracteres"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <small className="text-muted">
                  <i className="fa-regular fa-circle-info me-1"></i>
                  
                </small>
              </div>

              <button
                type="submit"
                className="btn btn-primary-custom w-100"
                disabled={cargando}
              >
                {cargando ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2"></span>
                    Registrando...
                  </>
                ) : (
                  <>
                    <i className="fa-regular fa-user me-2"></i> Registrarme
                  </>
                )}
              </button>
            </form>

            <div className="registro-footer">
              <p className="mb-0 text-muted">
                ¿Ya tienes cuenta?{" "}
                <Link to="/login" className="registro-link">
                  Inicia sesión aquí
                </Link>
              </p>
              <Link to="/" className="registro-volver">
                <i className="fa-solid fa-arrow-left me-1"></i> Volver al Inicio
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Registro;