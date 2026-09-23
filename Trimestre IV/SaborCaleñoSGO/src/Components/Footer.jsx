// src/Components/Footer.jsx

/*
  Componente: Footer
  Descripción: Pie de página de la aplicación.
  Contiene:
    - Información del restaurante (nombre, descripción)
    - Redes sociales (Instagram, Facebook, WhatsApp)
    - Enlaces rápidos a secciones
    - Datos de contacto
  Los iconos usan la clase "icon-accent" para cambiar de color según el tema elegido.
*/

import "../assets/CSS/footer.css";
import {
  FaPhoneAlt,
  FaFacebook,
  FaCalendar,
  FaMapMarkerAlt,
} from "react-icons/fa";
import { MdMarkEmailRead } from "react-icons/md";
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
                <AiFillInstagram className="icon-accent" />
              </a>
              <a href="#" aria-label="Facebook">
                <FaFacebook className="icon-accent" />
              </a>
              <a href="#" aria-label="WhatsApp">
                <IoLogoWhatsapp className="icon-accent" />
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
            <h5 className="footer-titulo">Contacto</h5>
            <ul className="footer-contact">
              <li>
                <FaPhoneAlt className="icon-accent" />
                <span>+57 300 123 4567</span>
              </li>
              <li>
                <MdMarkEmailRead className="icon-accent" />
                <span>saborcaleno@gmail.com</span>
              </li>
              <li>
                <FaMapMarkerAlt className="icon-accent" />
                <span>Bogotá D.C / Cali, Colombia</span>
              </li>
              <li>
                <FaCalendar className="icon-accent" />
                <span>Lun-Dom: 11:30 AM - 10:00 PM</span>
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