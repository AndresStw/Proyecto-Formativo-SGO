//src/Components/Header.jsx

import { Link } from "react-router-dom"; //Importante para navegación
import logo from "../assets/Img/logos/logo.png"; //importar png logo

// EL HEADER SE REPITE EN CADA PAGINA ENTONCES hacemos function LO USAMOS Y LO LLAMAMOS

function Header() {
  return (
    <header>
      <nav className="d-flex justify-content-around align-items-center gap-4 p-3 navegacion">
        <img src={logo} alt="Logo Restaurante" className="logo" />

        <p id="tituloR" className="abril-fatface-regular m-0 text-white">
          Sabor Caleño
        </p>

        <div className="d-flex justify-content-end gap-4 align-items-center">
          <Link className="text-white text-decoration-none" to="/">
            Inicio
          </Link>

          <Link className="text-white text-decoration-none" to="/nosotros">
            Nosotros
          </Link>

          <Link className="text-white text-decoration-none" to="/menu">
            Menu
          </Link>

          <button
            className="btn btn-login-nav login"
            onClick={() => {
              console.log("Se abrio solicitud a modal login");
            }}
          >
            Login
          </button>
        </div>
      </nav>
    </header>
  );
}

export default Header;
