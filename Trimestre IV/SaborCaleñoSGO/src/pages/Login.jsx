import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import logo from "../assets/Img/logos/logo.png";
import { login } from "../services/Auth"; // Nuevo ajuste
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
      navigate("/menu", { replace: true });
    } catch (err) {
      setError(err.message || "No fue posible iniciar sesion");
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
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
            <div className="form-group">
              <label className="form-label">
                <i className="fa-regular fa-envelope me-2"></i>Correo
                Electrónico
              </label>
              <div className="input-wrapper">
                <input
                  type="email"
                  className="form-input"
                  placeholder="correo@ejemplo.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
                <i className="fa-regular fa-envelope input-icon"></i>
              </div>
            </div>
            <div className="form-group">
              <label className="form-label">
                <i className="fa-solid fa-lock me-2"></i>Contraseña
              </label>
              <div className="input-wrapper">
                <input
                  type={showPassword ? "text" : "password"}
                  className="form-input"
                  placeholder="Ingresa tu contraseña"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <i
                  className={`fa-solid ${showPassword ? "fa-eye-slash" : "fa-eye"} input-icon password-toggle`}
                  onClick={() => setShowPassword((visible) => !visible)}
                ></i>
              </div>
            </div>
            <button type="submit" className="btn-login" disabled={cargando}>
              {cargando ? (
                "Ingresando..."
              ) : (
                <>
                  Iniciar Sesión{" "}
                  <i className="fa-solid fa-arrow-right ms-2"></i>
                </>
              )}
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
        <div className="login-decoration">
          <div className="decoration-content">
            <h3>Sabor Caleño</h3>
            <p>La autenticidad del sabor valluno</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
