// src/App.jsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./Components/Header";
import Footer from "./Components/Footer";
import Inicio from "./pages/Inicio";
import Menu from "./pages/Menu";
import Login from "./pages/Login";
import Registro from "./pages/Registro";
import Carrito from "./pages/Carrito";
import Nosotros from "./pages/Nosotros";
import Perfil from "./pages/Perfil";
import Pedidos from "./pages/Pedidos";
import PlacingOrder from "./pages/PlacingOrder";

function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<Inicio />} />
        <Route path="/menu" element={<Menu />} />
        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<Registro />} />
        <Route path="/carrito" element={<Carrito />} />
        <Route path="/nosotros" element={<Nosotros />} />
        <Route path="/perfil" element={<Perfil />} />
        <Route path="/pedidos" element={<Pedidos />} />
        <Route path="/placing-order" element={<PlacingOrder />} />
      </Routes>
      <Footer />
    </BrowserRouter>
  );
}

export default App;