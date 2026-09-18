import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { register } from "../services/Auth";
import logo from "../assets/Img/logos/logo.png";

import "../assets/CSS/global.css"; 
import "../assets/CSS/registro.css";

function Registro() {
  const [nombre, setNombre] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [telefono, setTelefono] = useState("");
  const [error, setError] = useState("");
  const [exito, setExito] = useState(false);
  const [cargando, setCargando] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (password.length < 6) {
      setError("La contraseña debe tener al menos 6 caracteres");
      return;
    }

    setCargando(true);

    try {
      // Envía los datos al servidor mediante la función register de Auth.js
      const data = await register({
        nombre,
        email: email.trim(),
        password,
        telefono,
      });

      setPassword("");
      setExito(true);

      // Si el servidor devuelve token (inició sesión automáticamente), redirige a /Perfil; si no, a /login
      setTimeout(() => {
  navigate("/login", { replace: true });
}, 1200);

    } catch (err) {
      setError(err.message || "No fue posible crear la cuenta");
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="registro-page">
      <div className="registro-container">
        <div className="registro-card">
          <div className="registro-header">
            <img src={logo} alt="Sabor Caleño" className="registro-logo" />
            <h2 className="registro-title">Crear Cuenta</h2>
            <p className="registro-subtitle">
              Regístrate para disfrutar de la mejor sazón valluna
            </p>
          </div>

          {error && (
            <div className="registro-error" role="alert">
              <i className="fa-solid fa-circle-exclamation me-2"></i>
              {error}
            </div>
          )}

          {exito && (
            <div className="registro-exito" role="alert">
              <i className="fa-solid fa-circle-check me-2"></i>
              ¡Registro exitoso! Redirigiendo...
            </div>
          )}

          <form onSubmit={handleSubmit} className="registro-form">
            {/* Nombre Completo */}
            <div className="form-group">
              <div className="input-capsule">
                <div className="icon-circle">
                  <i className="fa-solid fa-user"></i>
                </div>
                <input
                  type="text"
                  className="capsule-input"
                  placeholder="Nombre completo"
                  value={nombre}
                  onChange={(e) => setNombre(e.target.value)}
                  required
                />
              </div>
            </div>

            {/* Teléfono */}
            <div className="form-group">
              <div className="input-capsule">
                <div className="icon-circle">
                  <i className="fa-solid fa-phone"></i>
                </div>
                <input
                  type="tel"
                  className="capsule-input"
                  placeholder="Teléfono"
                  value={telefono}
                  onChange={(e) => setTelefono(e.target.value)}
                />
              </div>
            </div>

            {/* Correo Electrónico */}
            <div className="form-group">
              <div className="input-capsule">
                <div className="icon-circle">
                  <i className="fa-solid fa-envelope"></i>
                </div>
                <input
                  type="email"
                  className="capsule-input"
                  placeholder="Correo electrónico"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
            </div>

            {/* Contraseña */}
            <div className="form-group">
              <div className="input-capsule">
                <input
                  type={showPassword ? "text" : "password"}
                  className="capsule-input"
                  placeholder="Contraseña (mín. 6 caracteres)"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <button
                  type="button"
                  className="icon-circle toggle-btn"
                  onClick={() => setShowPassword((visible) => !visible)}
                  aria-label="Mostrar u ocultar contraseña"
                >
                  <i
                    className={`fa-solid ${
                      showPassword ? "fa-lock-open" : "fa-lock"
                    }`}
                  ></i>
                </button>
              </div>
            </div>

            {/* Botón de Registro */}
            <button
              type="submit"
              className="btn-registro"
              disabled={cargando}
            >
              {cargando ? "Registrando..." : "Registrarme"}
            </button>
          </form>

          <div className="registro-footer">
            <p>
              ¿Ya tienes cuenta?{" "}
              <Link to="/login" className="registro-link">
                Inicia sesión aquí
              </Link>
            </p>
            <Link to="/" className="back-link">
              <i className="fa-solid fa-arrow-left me-1"></i> Volver al Inicio
            </Link>
          </div>
        </div>

        {/* Panel Decorativo Derecho */}
        <div className="registro-decoration">
          <div className="decoration-content">
            <h3>Sabor Caleño</h3>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Registro;