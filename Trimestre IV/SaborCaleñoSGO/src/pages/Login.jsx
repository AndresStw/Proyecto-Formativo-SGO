// src/pages/Login.jsx
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [cargando, setCargando] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setCargando(true);

    try {
      const response = await fetch("http://localhost:3000/login", {
        //directo al login
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("token", data.accessToken);
        console.log("Bienvenid@!");
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
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-md-5">
          <div className="card shadow border-0 p-4">
            <div className="text-center mb-4">
              <h3 className="fw-bold" style={{ color: "#ff6b00" }}>
                Iniciar Sesión
              </h3>
              <p className="text-muted">¡Qué bueno tenerte de vuelta!</p>
            </div>

            {error && (
              <div className="alert alert-danger" role="alert">
                <i className="fa-solid fa-circle-exclamation me-2"></i>
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label htmlFor="email" className="form-label fw-semibold">
                  Correo Electrónico
                </label>
                <div className="input-group">
                  <span className="input-group-text bg-white">
                    <i className="fa-solid fa-envelope text-muted"></i>
                  </span>
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
              </div>

              <div className="mb-3">
                <label htmlFor="password" className="form-label fw-semibold">
                  Contraseña
                </label>
                <div className="input-group">
                  <span className="input-group-text bg-white">
                    <i className="fa-solid fa-lock text-muted"></i>
                  </span>
                  <input
                    type="password"
                    className="form-control"
                    id="password"
                    placeholder="********"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
              </div>

              <button
                type="submit"
                className="btn w-100 text-white my-2 fw-bold"
                style={{
                  background:
                    "linear-gradient(90deg, #ff6b00, #ff8c00, #ffb347)",
                  border: "none",
                }}
                disabled={cargando}
              >
                {cargando ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2"></span>
                    Ingresando...
                  </>
                ) : (
                  "Ingresar"
                )}
              </button>
            </form>

            <div className="text-center mt-3">
              <p className="mb-0 text-muted">
                ¿No tienes cuenta?{" "}
                <Link
                  to="/registro"
                  className="text-decoration-none fw-bold"
                  style={{ color: "#ff8c00" }}
                >
                  Regístrate aquí
                </Link>
              </p>
              <Link
                to="/"
                className="d-block mt-3 text-muted text-decoration-none small"
              >
                <i className="fa-solid fa-arrow-left me-1"></i> Volver al Inicio
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
