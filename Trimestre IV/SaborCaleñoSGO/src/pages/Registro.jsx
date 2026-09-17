import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { register } from "../services/Auth";
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
    if (password.length < 6) {
      setError("La contraseña debe tener al menos 6 caracteres");
      return;
    }
    setCargando(true);
    try {
      const data = await register({
        nombre,
        email: email.trim(),
        password,
        telefono,
      });
      setPassword("");
      setExito(true);
      setTimeout(
        () =>
          navigate(data.accessToken || data.token ? "/menu" : "/login", {
            replace: true,
          }),
        1200,
      );
    } catch (err) {
      setError(err.message || "No fue posible crear la cuenta");
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
              <p className="registro-subtitle">
                Regístrate para disfrutar de la mejor sazón valluna
              </p>
            </div>
            {error && (
              <div className="alert alert-danger" role="alert">
                {error}
              </div>
            )}
            {exito && (
              <div className="alert alert-success" role="alert">
                ¡Registro exitoso! Redirigiendo...
              </div>
            )}
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label htmlFor="nombre" className="form-label fw-semibold">
                  Nombre Completo
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="nombre"
                  value={nombre}
                  onChange={(e) => setNombre(e.target.value)}
                  required
                />
              </div>
              <div className="mb-3">
                <label htmlFor="telefono" className="form-label fw-semibold">
                  Teléfono
                </label>
                <input
                  type="tel"
                  className="form-control"
                  id="telefono"
                  value={telefono}
                  onChange={(e) => setTelefono(e.target.value)}
                />
              </div>
              <div className="mb-3">
                <label htmlFor="email" className="form-label fw-semibold">
                  Correo Electrónico
                </label>
                <input
                  type="email"
                  className="form-control"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="mb-3">
                <label htmlFor="password" className="form-label fw-semibold">
                  Contraseña
                </label>
                <input
                  type="password"
                  className="form-control"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <button
                type="submit"
                className="btn btn-primary-custom w-100"
                disabled={cargando}
              >
                {cargando ? "Registrando..." : "Registrarme"}
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
