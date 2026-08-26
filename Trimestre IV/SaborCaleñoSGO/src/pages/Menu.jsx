import { useEffect, useState } from "react";

function Menu() {
  const [productos, setProductos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const obtenerProductos = async () => {
      try {
        // 1. Obtener el token guardado en localStorage
        const token = localStorage.getItem("token");

        // 2. Si no hay token, mostrar error
        if (!token) {
          setError("Debes iniciar sesión para ver el menú");
          setCargando(false);
          return;
        }

        // 3. Hacer la petición con el token en el header
        const response = await fetch("http://localhost:3000/productos", {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        // 4. Si el token es inválido (401)
        if (response.status === 401) {
          setError("Sesión expirada. Por favor, inicia sesión nuevamente");
          localStorage.removeItem("token"); // Eliminar token inválido
          setCargando(false);
          return;
        }

        // 5. Si la respuesta es exitosa
        if (!response.ok) {
          throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        setProductos(data);
        setError(null);
      } catch (err) {
        setError("Error al cargar los productos: " + err.message);
        console.error("Error:", err);
      } finally {
        setCargando(false);
      }
    };

    obtenerProductos();
  }, []);

  // Mostrar mensaje de carga
  if (cargando) {
    return (
      <div className="container text-center py-5">
        <div className="spinner-border text-warning" role="status">
          <span className="visually-hidden">Cargando...</span>
        </div>
        <p>Cargando nuestro delicioso menú...</p>
      </div>
    );
  }

  // Mostrar error si ocurrió
  if (error) {
    return (
      <div className="container text-center py-5">
        <div className="alert alert-danger" role="alert">
          <i className="fa-solid fa-circle-exclamation me-2"></i>
          {error}
        </div>
        <button
          className="btn btn-warning"
          onClick={() => (window.location.href = "/login")}
        >
          <i className="fa-solid fa-right-to-bracket me-2"></i>
          Ir a Iniciar Sesión
        </button>
      </div>
    );
  }

  // Mostrar productos
  return (
    <div className="container py-5">
      <h2 className="text-center fw-bold mb-4" style={{ color: "#ff6b00" }}>
        Nuestro Menú Auténtico
      </h2>

      {productos.length === 0 ? (
        <p className="text-center text-muted">No hay productos disponibles</p>
      ) : (
        <div className="row g-4">
          {productos.map((producto) => (
            <div key={producto.id} className="col-md-4">
              <div className="card h-100 shadow-sm border-0">
                <div className="card-body text-center">
                  <h5 className="card-title fw-bold">{producto.nombre}</h5>
                  <p className="card-text text-muted small">
                    {producto.descripcion}
                  </p>
                  <span
                    className="fs-5 fw-bold d-block mb-2"
                    style={{ color: "#ff8c00" }}
                  >
                    ${producto.precio.toLocaleString()}
                  </span>
                  <button
                    className="btn btn-dark w-100"
                    onClick={() => {
                      console.log("Agregar al carrito:", producto);
                    }}
                  >
                    <i className="fa-solid fa-plus me-1"></i> Agregar
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Menu;
