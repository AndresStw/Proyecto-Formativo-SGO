// src/pages/Inicio.jsx

/*
Pagina principal con hero section y features.
  Estructura:
    - Hero: titulo principal, subtitulo y botones de accion
    - Features: 3 tarjetas destacando los valores del restaurante

 */

import { Link } from "react-router-dom";
import "../assets/CSS/inicio.css";

function Inicio() {
  return (
    <main>
      <section className="hero-section">
        <div className="hero-overlay"></div>
        <div className="hero-content container">
          <h1 className="hero-title">
            <span className="hero-highlight">Sabor Caleño</span>
            <br />
            La autenticidad del sabor valluno
          </h1>
          <p className="hero-subtitle">
            Descubre los platos tradicionales del Valle del Cauca, preparados
            con pasión y la mejor sazón.
          </p>
          <div className="hero-buttons">
            <Link to="/menu">
              <button className="btn-primary-custom">
                Ver Menu <i className="fa-solid fa-arrow-right ms-2"></i>
              </button>
            </Link>
            <Link to="/nosotros">
              <button className="btn-outline-custom">Conócenos</button>
            </Link>
          </div>
        </div>
      </section>

      <section className="features-section container">
        <div className="row g-4">
          <div className="col-md-4">
            <div className="feature-card">
              <i className="fa-solid fa-utensils feature-icon"></i>
              <h4>Platos Auténticos</h4>{" "}
              {/*Eror de tamañooooo usar  de h4 / h2*/}
              <p>Recetas tradicionales del Valle del Cauca</p>
            </div>
          </div>
          <div className="col-md-4">
            <div className="feature-card">
              <i className="fa-solid fa-truck feature-icon"></i>
              <h4>Delivery Rápido</h4>
              <p>Recibe tu pedido en la comodidad de tu hogar</p>
            </div>
          </div>
          <div className="col-md-4">
            <div className="feature-card">
              <i className="fa-solid fa-star feature-icon"></i>
              <h4>Calidad Garantizada</h4>
              <p>Ingredientes frescos y sazón inigualable</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

export default Inicio;
