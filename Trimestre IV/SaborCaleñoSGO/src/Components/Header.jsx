// src/Components/Header.jsx

/*
  Componente: Header
  Descripción: Barra de navegación principal de la aplicación.
  Funcionalidades:
    - Logo + navegación a Inicio, Menú, Nosotros
    - Si está logueado: Perfil, Pedidos, Chat, Carrito, Selector de tema y Salir
    - Si no está logueado: botón Login
    - Iconos con clase icon-accent (cambian de color según el tema)
*/

import { Link, useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import { menuData } from "./menuData";
import { PiShoppingCartSimpleFill } from "react-icons/pi";
import { TbMessageChatbotFilled } from "react-icons/tb";
import { FaPalette } from "react-icons/fa";
import ThemeSelector from "./ThemeSelector";
import { clearAuth } from "../services/Auth";

function Header() {
  const location = useLocation();
  const navigate = useNavigate();
  const [showThemePanel, setShowThemePanel] = useState(false);

  const token = localStorage.getItem("token");

  const handleLogout = () => {
    clearAuth();
    navigate("/", { replace: true });
  };

  const isActive = (path) => (location.pathname === path ? "active" : "");

  const carrito = JSON.parse(localStorage.getItem("carrito") || "[]");
  const totalItems = carrito.reduce(
    (acc, item) => acc + (item.cantidad || 1),
    0,
  );

  return (
    <nav className="header-nav">
      {/* Logo a la izquierda */}
      <div className="header-logo">
        <img src={menuData.logo} alt="Sabor Caleño" />
        <span></span>
      </div>

      {/* Enlaces centrales */}
      <div className="header-nav-links">
        <Link to="/" className={isActive("/")}>
          Inicio
        </Link>

        <Link to="/menu" className={isActive("/menu")}>
          Menú
        </Link>

        <Link to="/nosotros" className={isActive("/nosotros")}>
          Nosotros
        </Link>

        {token && (
          <>
            <Link to="/perfil" className={isActive("/perfil")}>
              Perfil
            </Link>

            <Link to="/pedidos" className={isActive("/pedidos")}>
              Pedidos
            </Link>
          </>
        )}
      </div>

      {/* Acciones a la derecha */}
      <div className="header-actions">
        {token ? (
          <>
            {/* Botón de tema */}
            <div className="theme-wrapper">
              <button
                className="btn-theme-toggle"
                onClick={() => setShowThemePanel(!showThemePanel)}
                aria-label="Cambiar color de iconos"
                title="Personalizar colores"
              >
                <FaPalette className="icon-accent" />
              </button>

              {showThemePanel && (
                <ThemeSelector onClose={() => setShowThemePanel(false)} />
              )}
            </div>

            {/* Chat */}
            <Link to="/chat-pedido" className={isActive("/chat-pedido")}>
              <TbMessageChatbotFilled className="icon-accent" />
            </Link>

            {/* Carrito */}
            <Link to="/carrito" className={isActive("/carrito")}>
              <PiShoppingCartSimpleFill className="icon-accent" />

              {totalItems > 0 && (
                <span className="badge bg-danger rounded-pill">
                  {totalItems}
                </span>
              )}
            </Link>

            <button className="btn-logout-nav" onClick={handleLogout}>
              Salir
            </button>
          </>
        ) : (
          <Link to="/login">
            <button className="btn-login-nav">
              <i className="fa-regular fa-user me-1"></i>
              Login
            </button>
          </Link>
        )}
      </div>
    </nav>
  );
}

export default Header;