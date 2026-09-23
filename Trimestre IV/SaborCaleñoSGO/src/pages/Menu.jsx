// src/pages/Menu.jsx

/*
    - Muestra productos agrupados por categorías
    - Filtro por categoría y orden por precio
    - Carrito lateral con toggle (minimizar/expandir)
    - Agregar productos al carrito (solo usuarios logueados)
    - Persistencia del carrito en localStorage
*/

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import MenuCard from "../Components/MenuCard";
import {
  menuData,
  categorias,
  getProductosByCategoria,
} from "../Components/menuData";
import "../assets/CSS/menu.css";

function Menu() {
  const [productos, setProductos] = useState([]);
  const [productosFiltrados, setProductosFiltrados] = useState([]);
  const [categoriaActiva, setCategoriaActiva] = useState("todos");
  const [cargando, setCargando] = useState(true);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [orden, setOrden] = useState("asc");
  const [carrito, setCarrito] = useState([]);
  const [total, setTotal] = useState(0);
  const [cartMinimized, setCartMinimized] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsLoggedIn(!!token);
  }, []);

  useEffect(() => {
    if (isLoggedIn) {
      const carritoGuardado = JSON.parse(
        localStorage.getItem("carrito") || "[]",
      );
      setCarrito(carritoGuardado);
      calcularTotal(carritoGuardado);
    } else {
      setCarrito([]);
      setTotal(0);
    }
  }, [isLoggedIn]);

  //Consume API  Local +Backend
  useEffect(() => {
    const productosLocales = getProductosByCategoria("todos");
    setProductos(productosLocales);
    setProductosFiltrados(productosLocales);
    setCargando(false);

    fetch("http://localhost:3000/productos")
      .then((res) => (res.ok ? res.json() : []))
      .then((data) => {
        if (!Array.isArray(data) || data.length === 0) return;

        const productosAPI = data.map((p) => ({
          ...p,
          rating: p.rating || 4.5,
          tiempo: p.tiempo || "30min",
          calorias: p.calorias || "300",
          imagen:
            menuData.productos.find(
              (local) => local.nombre.toLowerCase() === p.nombre.toLowerCase(),
            )?.imagen || "",
        }));

        const nombresAPI = new Set(
          productosAPI.map((p) => p.nombre.toLowerCase()),
        );

        // FIX: prefijo "local-" en el id
        const localesExtra = productosLocales
          .filter((p) => !nombresAPI.has(p.nombre.toLowerCase()))
          .map((p) => ({ ...p, id: `local-${p.id}` }));

        setProductos([...productosAPI, ...localesExtra]);
      })
      .catch(() => console.log("Usando datos locales (API no disponible)"));
  }, []);

  useEffect(() => {
    const filtrados =
      categoriaActiva === "todos"
        ? productos
        : productos.filter((p) => p.categoria === categoriaActiva);

    const ordenados = [...filtrados].sort((a, b) => {
      return orden === "asc" ? a.precio - b.precio : b.precio - a.precio;
    });

    setProductosFiltrados(ordenados);
  }, [categoriaActiva, productos, orden]);

  const calcularTotal = (items) => {
    const totalCalculado = items.reduce((acc, item) => {
      return acc + item.precio * (item.cantidad || 1);
    }, 0);
    setTotal(totalCalculado);
  };

  const handleFiltrar = (categoria) => {
    setCategoriaActiva(categoria);
  };

  const handleOrdenar = () => {
    setOrden(orden === "asc" ? "desc" : "asc");
  };

  const toggleCart = () => {
    setCartMinimized(!cartMinimized);
  };

  const handleAgregar = (producto) => {
    if (!isLoggedIn) {
      alert("Debes iniciar sesión para agregar productos al carrito");
      navigate("/login");
      return;
    }

    const carritoActual = JSON.parse(localStorage.getItem("carrito") || "[]");
    const existe = carritoActual.find((item) => item.id === producto.id);

    let nuevoCarrito;
    if (existe) {
      nuevoCarrito = carritoActual.map((item) =>
        item.id === producto.id
          ? { ...item, cantidad: (item.cantidad || 1) + 1 }
          : item,
      );
    } else {
      nuevoCarrito = [...carritoActual, { ...producto, cantidad: 1 }];
    }

    localStorage.setItem("carrito", JSON.stringify(nuevoCarrito));
    setCarrito(nuevoCarrito);
    calcularTotal(nuevoCarrito);
    alert(`${producto.nombre} agregado al carrito`);
  };

  const handleEliminar = (id) => {
    const nuevoCarrito = carrito.filter((item) => item.id !== id);
    localStorage.setItem("carrito", JSON.stringify(nuevoCarrito));
    setCarrito(nuevoCarrito);
    calcularTotal(nuevoCarrito);
  };

  const handleActualizarCantidad = (id, nuevaCantidad) => {
    if (nuevaCantidad < 1) {
      handleEliminar(id);
      return;
    }

    const nuevoCarrito = carrito.map((item) =>
      item.id === id ? { ...item, cantidad: nuevaCantidad } : item,
    );
    localStorage.setItem("carrito", JSON.stringify(nuevoCarrito));
    setCarrito(nuevoCarrito);
    calcularTotal(nuevoCarrito);
  };

  if (cargando) {
    return (
      <div className="container text-center py-5">
        <div className="spinner-border text-warning" role="status">
          <span className="visually-hidden">Cargando...</span>
        </div>
        <p className="mt-2 text-muted">Cargando nuestro delicioso menú...</p>
      </div>
    );
  }

  return (
    <div
      className={`menu-layout ${isLoggedIn ? "with-cart" : "without-cart"} ${cartMinimized ? "cart-minimized" : ""}`}
    >
      <div className="menu-layout-container">
        <div className="menu-productos">
          <div className="menu-header">
            <h2 className="menu-title">Nuestro Menú</h2>
            <p className="menu-subtitle">Elige tus platos favoritos</p>
          </div>

          <div className="menu-controls">
            <div className="menu-filtros">
              {categorias.map((cat) => (
                <button
                  key={cat.id}
                  className={`btn-filter ${categoriaActiva === cat.id ? "active" : ""}`}
                  onClick={() => handleFiltrar(cat.id)}
                >
                  {cat.label}
                </button>
              ))}
            </div>
            <div className="menu-orden">
              <button className="btn-orden" onClick={handleOrdenar}>
                <i className="fa-solid fa-arrow-up-wide-short me-1"></i>
                Precio: {orden === "asc" ? "Menor a mayor" : "Mayor a menor"}
              </button>
            </div>
          </div>

          <div
            className={`menu-grid ${isLoggedIn ? "grid-with-cart" : "grid-full"}`}
          >
            {productosFiltrados.length === 0 ? (
              <div className="text-center py-4">
                <p className="text-muted">No hay productos en esta categoría</p>
              </div>
            ) : (
              productosFiltrados.map((producto) => (
                <MenuCard
                  key={producto.id}
                  producto={producto}
                  onAgregar={handleAgregar}
                  isLoggedIn={isLoggedIn}
                />
              ))
            )}
          </div>
        </div>

        {isLoggedIn && (
          <div className="menu-carrito">
            <div className="carrito-sidebar">
              <div className="carrito-sidebar-header">
                <h3 className="carrito-sidebar-title">
                  <i className="fa-solid fa-basket-shopping me-2"></i>
                  Tu Pedido
                </h3>
                <button className="btn-toggle-cart" onClick={toggleCart}>
                  <i
                    className={`fa-solid ${cartMinimized ? "fa-chevron-down" : "fa-chevron-up"}`}
                  ></i>
                </button>
              </div>

              {!cartMinimized && (
                <>
                  {carrito.length === 0 ? (
                    <div className="carrito-vacio-sidebar">
                      <i className="fa-regular fa-cart-plus"></i>
                      <p>No hay productos</p>
                      <span className="text-muted small">
                        Agrega platos del menú
                      </span>
                    </div>
                  ) : (
                    <>
                      <div className="carrito-items-sidebar">
                        {carrito.map((item) => (
                          <div key={item.id} className="carrito-item-sidebar">
                            <div className="carrito-item-info">
                              <h5 className="carrito-item-nombre">
                                {item.nombre}
                              </h5>
                              <div className="carrito-item-controls">
                                <button
                                  className="btn-qty"
                                  onClick={() =>
                                    handleActualizarCantidad(
                                      item.id,
                                      (item.cantidad || 1) - 1,
                                    )
                                  }
                                >
                                  −
                                </button>
                                <span className="qty-number">
                                  {item.cantidad || 1}
                                </span>
                                <button
                                  className="btn-qty"
                                  onClick={() =>
                                    handleActualizarCantidad(
                                      item.id,
                                      (item.cantidad || 1) + 1,
                                    )
                                  }
                                >
                                  +
                                </button>
                                <span className="carrito-item-precio">
                                  ${item.precio}
                                </span>
                                <button
                                  className="btn-remove"
                                  onClick={() => {
                                    if (
                                      window.confirm(
                                        `¿Eliminar "${item.nombre}" del carrito?`,
                                      )
                                    ) {
                                      handleEliminar(item.id);
                                    }
                                  }}
                                >
                                  <i className="fa-solid fa-trash-can"></i>
                                </button>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>

                      <div className="carrito-sidebar-footer">
                        <div className="carrito-total-sidebar">
                          <span className="total-label">Total:</span>
                          <span className="total-amount">
                            ${total.toLocaleString()}
                          </span>
                        </div>
                        <button
                          className="btn-checkout"
                          onClick={() => navigate("/placing-order")}
                          disabled={carrito.length === 0}
                        >
                          <i className="fa-solid fa-credit-card me-2"></i>
                          Proceder al Pago
                        </button>
                      </div>
                    </>
                  )}
                </>
              )}

              {cartMinimized && (
                <div className="carrito-minimizado-info">
                  <span className="minimizado-total">
                    ${total.toLocaleString()}
                  </span>
                  <span className="minimizado-items">
                    {carrito.length} items
                  </span>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Menu;
