import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./Components/Header";
import Inicio from "./pages/Inicio"; // aun no funciona
import Menu from "./pages/Menu"; //funciona tiene login
import Login from "./pages/Login"; //funciona tiene login
import Plato from "../src/assets/Img/platos/arroz.jpg";
import Css from "../src/"

function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<Inicio />} /> {/* ← Usa el componente */}
        <Route path="/nosotros" element={<h1>Pagina nosotros</h1>} />
        {/* ← Aun no funciona */}
        <Route path="/menu" element={<Menu />} />
        <Route path="/login" element={<Login />} />
      </Routes>
      <div>
                    <div id="carruselPrincipal" classname="carousel slide">
                <div classname="carousel-inner">
                    <div classname="carousel-item active">
                        <div classname="carrusel-contenido">
                            <p classname="textoPrincipal"><i>La autenticidad del sabor valluno</i></p>
                            <img src={Plato} alt="" /> {/* */}
                        </div>
                    </div>
                    <div classname="carousel-item">
                        <div classname="carrusel-contenido">
                            <p classname="textoPrincipal"><i>Un espacio diseñado para compartir</i></p>
                        </div>
                    </div>
                    <div classname="carousel-item">
                        <div classname="carrusel-contenido">
                            <p classname="textoPrincipal"><i>La esencia del Valle en un solo lugar</i></p>
                        </div>
                    </div>
                </div>
                <button classname="carousel-control-prev" type="button" data-bs-target="#carruselPrincipal"
                    data-bs-slide="prev">
                    <span classname="carousel-control-prev-icon"></span>
                </button>
                <button classname="carousel-control-next" type="button" data-bs-target="#carruselPrincipal"
                    data-bs-slide="next">
                    <span classname="carousel-control-next-icon"></span>
                </button>
            </div>
      </div>
    </BrowserRouter>
    
  );
}

export default App;
