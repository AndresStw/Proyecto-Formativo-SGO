// src/pages/Login.jsx

/*
    - Formulario con email y contraseña
    - Validacion de credenciales contra JSON Server
    - Almacena token y email en localStorage al iniciar sesion
    - Redirige al menu despus del login exitoso
    - Muestra/oculta contraseña con toggle
    -obiamente se necesita tener la db.json

*/

import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import logo from "../assets/Img/logos/logo.png";
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
      const response = await fetch("http://localhost:3000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("token", data.accessToken);
        localStorage.setItem("userEmail", email);
        navigate("/menu");
      } else {
        setError(data.message || "Credenciales incorrectas");
      }
    } catch (err) {
      setError("Error de conexión. Asegúrate que el servidor está corriendo.");
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
            <p className="login-subtitle">Inicia sesión para disfrutar de la mejor sazón valluna</p>
          </div>

          {error && (
            <div className="login-error">
              <i className="fa-solid fa-circle-exclamation me-2"></i>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label className="form-label">
                <i className="fa-regular fa-envelope me-2"></i>
                Correo Electrónico
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
                <i className="fa-solid fa-lock me-2"></i>
                Contraseña
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
                  onClick={() => setShowPassword(!showPassword)}
                ></i>
              </div>
            </div>

            <div className="form-options">
              <label className="checkbox-label">
                <input type="checkbox" />
                <span>Recordarme</span>
              </label>
              <Link to="/recuperar" className="forgot-link">
                ¿Olvidaste tu contraseña?
              </Link>
            </div>

            <button
              type="submit"
              className="btn-login"
              disabled={cargando}
            >
              {cargando ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2"></span>
                  Ingresando...
                </>
              ) : (
                <>
                  Iniciar Sesión
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
            <div className="decoration-features">
              <span><i className="fa-solid fa-utensils"></i> Platos típicos</span>
              <span><i className="fa-solid fa-truck"></i> Delivery</span>
              <span><i className="fa-solid fa-star"></i> Calidad</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;