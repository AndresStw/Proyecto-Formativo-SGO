// src/Components/ThemeSelector.jsx

import { useState, useEffect } from "react";
import "../assets/CSS/theme-selector.css";

function ThemeSelector({ onClose }) {
  const [theme, setTheme] = useState("green");
  const [showWelcome, setShowWelcome] = useState(false);

  useEffect(() => {
    const savedTheme = localStorage.getItem("userColorTheme") || "green";
    setTheme(savedTheme);
    applyTheme(savedTheme);

    const hasSeenAlert = localStorage.getItem("hasSeenColorAlert");
    if (!hasSeenAlert) {
      setShowWelcome(true);
    }
  }, []);

  const applyTheme = (themeName) => {
    document.documentElement.setAttribute("data-theme", themeName);
    localStorage.setItem("userColorTheme", themeName);
  };

  const handleThemeChange = (themeName) => {
    setTheme(themeName);
    applyTheme(themeName);
  };

  const handleCloseWelcome = () => {
    setShowWelcome(false);
    localStorage.setItem("hasSeenColorAlert", "true");
  };

  const themes = [
    { name: "green", label: "Verde", color: "#07dc07" },
    { name: "yellow", label: "Amarillo neón", color: "#fff700" },
    { name: "pink", label: "Rosa", color: "#ff6699" },
    { name: "blue", label: "Azul", color: "#0000ff" },
  ];

  return (
    <div className="theme-selector-panel">
      {showWelcome && (
        <div className="theme-welcome">
          <div className="theme-welcome-content">
            <i className="fa-solid fa-palette theme-welcome-icon"></i>
            <div>
              <strong>¡Personaliza tu experiencia!</strong>
              <p>Elige el color de los iconos de tu app 🎨</p>
            </div>
            <button
              className="theme-welcome-close"
              onClick={handleCloseWelcome}
              aria-label="Cerrar mensaje"
            >
              <i className="fa-solid fa-xmark"></i>
            </button>
          </div>
        </div>
      )}

      <div className="theme-header">
        <h5>
          <i className="fa-solid fa-palette me-2"></i>
          Color de iconos
        </h5>
        <button
          className="theme-close-btn"
          onClick={onClose}
          aria-label="Cerrar selector"
        >
          <i className="fa-solid fa-xmark"></i>
        </button>
      </div>

      <div className="theme-options">
        {themes.map((t) => (
          <button
            key={t.name}
            className={`theme-btn ${theme === t.name ? "active" : ""}`}
            style={{ backgroundColor: t.color }}
            onClick={() => handleThemeChange(t.name)}
            title={t.label}
            aria-label={`Tema ${t.label}`}
          >
            {theme === t.name && (
              <i className="fa-solid fa-check theme-check"></i>
            )}
          </button>
        ))}
      </div>

      <p className="theme-hint">
        <i className="fa-regular fa-lightbulb me-1"></i>
        Los iconos cambian de color al instante
      </p>
    </div>
  );
}

export default ThemeSelector;
