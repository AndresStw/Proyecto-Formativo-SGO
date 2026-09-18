import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import logo from "../assets/Img/logos/logo.png";
import { login } from "../services/Auth";
import "../assets/CSS/global.css";
import "../assets/CSS/login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [cargando, setCargando] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setCargando(true);
    try {
      await login(email.trim(), password);
      setPassword("");
      navigate("/Perfil", { replace: true });
    } catch (err) {
      setError(err.message || "No fue posible iniciar sesión");
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        {/* Panel Izquierdo: Formulario */}
        <div className="login-card">
          <div className="login-header">
            <img src={logo} alt="Sabor Caleño" className="login-logo" />
            <h2 className="login-title">¡Bienvenido de vuelta!</h2>
            <p className="login-subtitle">
              Inicia sesión para disfrutar de la mejor sazón valluna
            </p>
          </div>

          {error && (
            <div className="login-error" role="alert">
              <i className="fa-solid fa-circle-exclamation me-2"></i>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="login-form">
            {/* Campo Correo: Ícono de usuario dentro de la bolita izquierda */}
            <div className="form-group">
              <div className="input-capsule">
                <div className="icon-circle">
                  <i className="fa-solid fa-user"></i>
                </div>
                <input
                  type="email"
                  className="capsule-input"
                  placeholder="correo@ejemplo.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
            </div>

            {/* Campo Contraseña: Ícono de candado dentro de la bolita derecha */}
            <div className="form-group">
              <div className="input-capsule">
                <input
                  type={showPassword ? "text" : "password"}
                  className="capsule-input"
                  placeholder="Ingresa tu contraseña"
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
                  <i className={`fa-solid ${showPassword ? "fa-lock-open" : "fa-lock"}`}></i>
                </button>
              </div>
            </div>

            {/* Enlace ¿Olvidaste tu contraseña? */}
            <div className="forgot-password-container">
              <Link to="/recuperar-contrasena" className="forgot-link">
                ¿Olvidaste tu contraseña?
              </Link>
            </div>

            {/* Botón Verde Plano con border-radius de 10px */}
            <button type="submit" className="btn-login" disabled={cargando}>
              {cargando ? "Ingresando..." : "Iniciar Sesión"}
            </button>
          </form>

          <div className="login-footer">
            <p>
              ¿No tienes cuenta?{" "}
              <Link to="/registro" className="register-link">
                Regístrate aquí
              </Link>
            </p>
            <Link to="/" className="back-link">
              <i className="fa-solid fa-arrow-left me-1"></i> Volver al Inicio
            </Link>
          </div>
        </div>

        {/* Panel Derecho: Solo texto Sabor Caleño */}
        <div className="login-decoration">
          <div className="decoration-content">
            <h3>Sabor Caleño</h3>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;