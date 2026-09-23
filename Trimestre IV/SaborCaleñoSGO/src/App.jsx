import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [productos, setProductos] = useState([]);
  const [pedido, setPedido] = useState([]);

  useEffect(() => {
    fetch("http://localhost:3000/products")
      .then((respuesta) => respuesta.json())
      .then((datos) => setProductos(datos))
      .catch((error) => console.error("Error:", error));
  }, []);

  const agregarAlPedido = (producto) => {
    setPedido([...pedido, producto]);
  };

  return (
    <div className="app">
      <h1>Sabor Caleño</h1>

      <h2>Productos</h2>

      <div className="productos">
        {productos.map((producto) => (
          <div className="producto" key={producto.id}>
            <h3>{producto.nombre}</h3>

            <p>{producto.categoria}</p>

            <strong>
              ${Number(producto.precio).toLocaleString("es-CO")}
            </strong>

            <br />

            <button onClick={() => agregarAlPedido(producto)}>
              Agregar al pedido
            </button>
          </div>
        ))}
      </div>

      <h2>Mi pedido</h2>

      {pedido.length === 0 ? (
        <p>No hay productos en el pedido.</p>
      ) : (
        <div>
          {pedido.map((producto, index) => (
            <p key={index}>
              {producto.nombre} - $
              {Number(producto.precio).toLocaleString("es-CO")}
            </p>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;