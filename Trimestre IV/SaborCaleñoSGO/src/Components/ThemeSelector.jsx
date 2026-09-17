import { useState } from "react";

function ThemeSelector() {
  const [theme, setTheme] =
    useState("green"); /*Verde por default o cambiar depende*/
  const [showAler, setShowAlert] = useState(false);

  useState(() => {
    const savedTheme = localStorage.getItem("userColorTheme") || "green";
    setTheme(savedTheme);
    applyTheme(savedTheme);

    const hasSeenAlert = localStorage.getItem("hasSeenColorAlert");
    if (!hasSeenAlert) {
      setShowAlert(true);
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
  const themes = [
    { name: "yellow", label: "Amarillo neon", color: "#fff700" },
    { name: "pink", label: "rosa", color: "#ff6699" },
    { name: "blue", label: "azul", color: "#0000ff" },
  ];

  return (
    <div className="theme-selector">
      <h5>Personaliza tus iconos</h5>
      <div className="theme-options">
        {themes.map((t) => (
          <button
            key={t.name}
            className={`theme-btn $ {theme === t.name ? "active" : ""}`}
            style={{ backgroundColor: t.color }}
            onClick={() => handleThemeChange(t.name)}
            title={t.label}
          ></button>
        ))}
      </div>
    </div>
  );
}

export default ThemeSelector;
