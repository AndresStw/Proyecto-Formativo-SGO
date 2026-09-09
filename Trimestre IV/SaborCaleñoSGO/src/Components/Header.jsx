// src/Components/Header.jsx

/*
  Que hace: Barra de navegacion principal.
    - Muestra el logo y nombre del restaurante
    - Navegacion a las secciones principales Inicio, Menu, Nosotros
    - Si el usuario esta logueado muestra Perfil, Carrito y botón Salir
    - Si no está logueado: muestra boton Login
    - El contador del carrito muestra la cantidad total de items
  
*/

import { Link, useLocation } from "react-router-dom";
import { menuData } from "./menuData";
import { IoLogIn } from "react-icons/io5";


function Header() {
  const location = useLocation();
  const token = localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  const isActive = (path) => location.pathname === path ? "active" : "";

  const carrito = JSON.parse(localStorage.getItem("carrito") || "[]");
  const totalItems = carrito.reduce((acc, item) => acc + (item.cantidad || 1), 0);

  return (
    <nav className="header-nav">
      <div className="header-logo">
        <img src={menuData.logo} alt="Sabor Caleño" />
        <span>Sabor Caleño</span>
      </div>

      <div className="header-nav-links">
        <Link to="/" className={isActive("/")}>Inicio</Link>
        <Link to="/menu" className={isActive("/menu")}>Menú</Link>
        <Link to="/nosotros" className={isActive("/nosotros")}>Nosotros</Link>
        
        {token ? (
          <>
            <Link to="/perfil" className={isActive("/perfil")}>
              <i className="fa-regular fa-user me-1"></i> Perfil
            </Link>
            <Link to="/carrito" className={isActive("/carrito")}>
              <i className="fa-solid fa-basket-shopping me-1"></i>
              {totalItems > 0 && (
                <span className="badge bg-danger rounded-pill" style={{ fontSize: "0.6rem" }}>
                  {totalItems}
                </span>
              )}
            </Link>
            <button className="btn-logout-nav" onClick={handleLogout}>
              <i className="fa-solid fa-right-from-bracket me-1"></i> Salir
            </button>
          </>
        ) : (
          <Link to="/login">
            <button className="btn-login-nav">
              <i className="fa-regular fa-user me-1"></i> Login
            </button>
          </Link>
        )}
      </div>
    </nav>
  );
}

export default Header;