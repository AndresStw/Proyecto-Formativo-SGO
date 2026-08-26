import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./Components/Header";
import Inicio from "./pages/Inicio"; // aun no funciona
import Menu from "./pages/Menu"; //funciona tiene login
import Login from "./pages/Login"; //funciona tiene login

function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<Inicio />} /> {/* ← Usa el componente */}
        <Route path="/nosotros" element={<h1>Página Nosotros</h1>} />
        <Route path="/menu" element={<Menu />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
