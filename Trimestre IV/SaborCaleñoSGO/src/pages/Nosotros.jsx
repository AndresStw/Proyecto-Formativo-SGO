import { useState } from "react";
import "../assets/CSS/nosotros.css";

function Nosotros() {
  const [formData, setFormData] = useState({
    nombre: "",
    correo: "",
    mensaje: ""
  });
  const [enviado, setEnviado] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Mensaje enviado:", formData);
    setEnviado(true);
    setTimeout(() => setEnviado(false), 5000);
    setFormData({ nombre: "", correo: "", mensaje: "" });
  };

  return (
    <div className="container py-5">
      <div className="nosotros-header">
        <h2 className="nosotros-titulo">Contáctanos y Conócenos</h2>
        <p className="nosotros-subtitulo">
          Estamos ubicados en Santa Lucía, listos para atenderte con la mejor alegría valluna.
        </p>
      </div>

      <div className="row g-5">
        {/* Información */}
        <div className="col-md-6">
          <div className="nosotros-info">
            <h4 className="info-titulo">
              <i className="fa-regular fa-clock me-2" style={{ color: 'var(--secondary, #10b981)' }}></i>
              Horarios de Atención
            </h4>
            <ul className="info-lista">
              <li>
                <span className="info-dia">Lunes a Viernes:</span>
                <span className="info-hora">11:30 AM - 9:00 PM</span>
              </li>
              <li>
                <span className="info-dia">Sábados y Domingos:</span>
                <span className="info-hora">11:00 AM - 10:00 PM</span>
              </li>
            </ul>

            <h4 className="info-titulo mt-4">
              <i className="fa-regular fa-heart me-2" style={{ color: 'var(--secondary, #10b981)' }}></i>
              Nuestra Misión
            </h4>
            <p className="info-mision">
              Traer un pedacito del Valle del Cauca a tu mesa, rescatando las recetas 
              tradicionales de las abuelas caleñas con ingredientes frescos y un servicio impecable.
            </p>

            <div className="info-ubicacion">
              <h4 className="info-titulo">
                <i className="fa-solid fa-location-dot me-2" style={{ color: 'var(--secondary, #10b981)' }}></i>
                Encuéntranos
              </h4>
              <p>
                <strong>Sede Principal:</strong> Santa Lucía, Bogotá D.C.
              </p>
              <p>
                <strong>Sede Cali:</strong> Aguacatal / El Pondaje / Pance
              </p>
            </div>
          </div>
        </div>

        {/* Formulario */}
        <div className="col-md-6">
          <div className="nosotros-formulario">
            <h5 className="form-titulo">Déjanos un mensaje</h5>
            
            {enviado && (
              <div className="alert alert-success mt-3 mb-3">
                <i className="fa-solid fa-circle-check me-2"></i>
                ¡Mensaje enviado con éxito! Te responderemos pronto.
              </div>
            )}

            <form onSubmit={handleSubmit} className="nosotros-form-block">
              <div className="form-group-custom">
                <label className="form-label fw-semibold">Nombre</label>
                <input
                  type="text"
                  name="nombre"
                  className="form-control custom-input-field"
                  placeholder="Tu nombre"
                  value={formData.nombre}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group-custom">
                <label className="form-label fw-semibold">Correo Electrónico</label>
                <input
                  type="email"
                  name="correo"
                  className="form-control custom-input-field"
                  placeholder="correo@ejemplo.com"
                  value={formData.correo}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group-custom">
                <label className="form-label fw-semibold">Mensaje</label>
                <textarea
                  name="mensaje"
                  className="form-control custom-input-field"
                  rows={4}
                  placeholder="Cuéntanos tu experiencia o lo que necesites..."
                  value={formData.mensaje}
                  onChange={handleChange}
                  required
                />
              </div>

              <button type="submit" className="btn-primary-custom w-100">
                <i className="fa-regular fa-paper-plane me-2"></i> Enviar Mensaje
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Nosotros;