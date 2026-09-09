// src/Components/Footer.jsx

/*
  
  Que hace: Pie de pagina de la aplicacion.
    - Informacion del restaurante nombre, descripcion
    - Redes sociales Instagram, Facebook, WhatsApp
    - Enlaces rapidos a secciones importantes
    - Datos de contacto , email, direccion, horarios
    - Estatico
*/

import "../assets/CSS/footer.css";
import { FaPhoneAlt } from "react-icons/fa";
import { MdMarkEmailRead } from "react-icons/md";
import { FaMapMarkerAlt } from "react-icons/fa";
import { FaCalendar } from "react-icons/fa";
import { FaFacebook } from "react-icons/fa";
import { IoLogoWhatsapp } from "react-icons/io";
import { AiFillInstagram } from "react-icons/ai";

function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="row g-4">
          <div className="col-md-4">
            <h5 className="footer-titulo">Sabor Caleño</h5>
            <p className="footer-desc">
              La autenticidad del sabor valluno en cada plato. Recetas
              tradicionales con la mejor sazón.
            </p>
            <div className="footer-social">
              <a href="#" aria-label="Instagram">
                <i className="fa-brands fa-instagram">
                  <AiFillInstagram />
                </i>
              </a>
              <a href="#" aria-label="Facebook">
                <i className="fa-brands fa-facebook">
                  <FaFacebook />
                </i>
              </a>
              <a href="#" aria-label="WhatsApp">
                <i className="fa-brands fa-whatsapp">
                  <IoLogoWhatsapp />
                </i>
              </a>
            </div>
          </div>

          <div className="col-md-4">
            <h5 className="footer-titulo">Enlaces Rápidos</h5>
            <ul className="footer-links">
              <li>
                <a href="/menu">Nuestro Menú</a>
              </li>
              <li>
                <a href="/nosotros">Nosotros</a>
              </li>
              <li>
                <a href="/reservas">Reservas</a>
              </li>
              <li>
                <a href="/contacto">Contacto</a>
              </li>
            </ul>
          </div>

          <div className="col-md-4">
            <h5 className="footer-titulo">Contacto</h5> {/* Falta orregirlo esta centrado*/}
            <ul className="footer-contact">
              <li>
                <i className="fa-solid fa-phone"></i>
                <span>
                  <FaPhoneAlt /> +57 300 123 4567
                </span>
              </li>
              <li>
                <i className="fa-regular fa-envelope"></i>
                <span>
                  <MdMarkEmailRead />
                  saborcaleno@gmail.com
                </span>
              </li>
              <li>
                <i className="fa-solid fa-location-dot"></i>
                <span>
                  <FaMapMarkerAlt />
                  Santa Lucía, Colombia
                </span>
              </li>
              <li>
                <i className="fa-regular fa-clock"></i>
                <span>
                  <FaCalendar />
                  Lun-Dom: 11:30 AM - 10:00 PM
                </span>
              </li>
            </ul>
          </div>
        </div>

        <div className="footer-bottom">
          <p className="mb-0">
            &copy; {new Date().getFullYear()} Sabor Caleño. Todos los derechos
            reservados.
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
