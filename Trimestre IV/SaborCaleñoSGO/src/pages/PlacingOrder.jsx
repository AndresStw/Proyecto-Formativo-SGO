// src/pages/PlacingOrder.jsx
import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import "../assets/CSS/placing-order.css";

function PlacingOrder() {
  const [carrito, setCarrito] = useState([]);
  const [total, setTotal] = useState(0);
  const [direccionSeleccionada, setDireccionSeleccionada] = useState("new");
  const [cartMinimized, setCartMinimized] = useState(false);
  const [direccionesGuardadas, setDireccionesGuardadas] = useState([
    {
      id: 1,
      direccion: "Lviv, St. Red, 12A, entrance 6, floor 7, flat 76, intercom - 7621"
    },
    {
      id: 2,
      direccion: "Kyiv, St. Green, 22A, entrance 3, floor 9, flat 98, intercom - 8742"
    }
  ]);

  const [nuevaDireccion, setNuevaDireccion] = useState({
    ciudad: "",
    calle: "",
    numero: "",
    entrada: "",
    piso: "",
    apartamento: "",
    intercom: ""
  });

  const [metodoEntrega, setMetodoEntrega] = useState("delivery");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }

    const carritoGuardado = localStorage.getItem("carrito");
    let carritoData = [];
    if (carritoGuardado) {
      carritoData = JSON.parse(carritoGuardado);
    }
    
    setCarrito(carritoData);

    const totalCalculado = carritoData.reduce((acc, item) => {
      return acc + (item.precio * (item.cantidad || 1));
    }, 0);
    setTotal(totalCalculado);
  }, [navigate]);

  const handleDireccionChange = (e) => {
    setDireccionSeleccionada(e.target.value);
  };

  const handleNuevaDireccionChange = (e) => {
    setNuevaDireccion({
      ...nuevaDireccion,
      [e.target.name]: e.target.value
    });
  };

  const handleGuardarDireccion = () => {
    const direccionCompleta = `${nuevaDireccion.ciudad}, St. ${nuevaDireccion.calle}, ${nuevaDireccion.numero}, entrance ${nuevaDireccion.entrada}, floor ${nuevaDireccion.piso}, flat ${nuevaDireccion.apartamento}, intercom - ${nuevaDireccion.intercom}`;
    
    const nuevaDir = {
      id: Date.now(),
      direccion: direccionCompleta
    };
    
    setDireccionesGuardadas([...direccionesGuardadas, nuevaDir]);
    setDireccionSeleccionada("new");
    setNuevaDireccion({
      ciudad: "",
      calle: "",
      numero: "",
      entrada: "",
      piso: "",
      apartamento: "",
      intercom: ""
    });
    alert("Dirección guardada exitosamente");
  };

  const handleContinuarPago = () => {
    if (direccionSeleccionada === "new" && !nuevaDireccion.ciudad) {
      alert("Por favor completa la dirección de entrega");
      return;
    }
    alert("Redirigiendo al pago...");
  };

  const handlePedido = () => {
    if (carrito.length === 0) {
      alert("Tu carrito está vacío");
      return;
    }
    alert("¡Pedido realizado con éxito!");
    localStorage.removeItem("carrito");
    navigate("/pedidos");
  };

  const toggleCart = () => {
    setCartMinimized(!cartMinimized);
  };

  if (carrito.length === 0) {
    return (
      <div className="placing-container">
        <div className="container py-5">
          <div className="text-center">
            <h2>Tu carrito está vacío</h2>
            <p className="text-muted">Agrega algunos platos antes de realizar tu pedido</p>
            <Link to="/menu" className="btn-primary-custom mt-3">
              <i className="fa-solid fa-utensils me-2"></i> Ver Menú
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`placing-container ${cartMinimized ? "cart-minimized" : ""}`}>
      <div className="container py-4">
        <div className="placing-grid">
          {/* Sección Izquierda: Delivery */}
          <div className="placing-delivery">
            <div className="placing-header">
              <h2 className="placing-title">REALIZAR UN PEDIDO</h2>
              <button className="btn-toggle-cart" onClick={toggleCart}>
                {cartMinimized ? (
                  <><i className="fa-solid fa-chevron-down me-1"></i> </>
                ) : (
                  <><i className="fa-solid fa-chevron-up me-1"></i> </>
                )}
              </button>
            </div>

            <div className="delivery-section">
              <h3 className="section-title">Entrega <span className="step-badge">1/2</span></h3>
              
              <div className="direcciones-guardadas">
                {direccionesGuardadas.map((dir) => (
                  <label key={dir.id} className="direccion-radio">
                    <input
                      type="radio"
                      name="direccion"
                      value={dir.id}
                      checked={direccionSeleccionada === String(dir.id)}
                      onChange={handleDireccionChange}
                    />
                    <span>{dir.direccion}</span>
                  </label>
                ))}
                
                <label className="direccion-radio">
                  <input
                    type="radio"
                    name="direccion"
                    value="new"
                    checked={direccionSeleccionada === "new"}
                    onChange={handleDireccionChange}
                  />
                  <span className="new-address-label">Nueva dirección</span>
                </label>
              </div>

              {direccionSeleccionada === "new" && (
                <div className="nueva-direccion">
                  <div className="form-row">
                    <div className="form-group">
                      <label>Ciudad</label>
                      <input
                        type="text"
                        name="ciudad"
                        value={nuevaDireccion.ciudad}
                        onChange={handleNuevaDireccionChange}
                        placeholder="Ternopil"
                      />
                    </div>
                    <div className="form-group">
                      <label>Calle</label>
                      <input
                        type="text"
                        name="calle"
                        value={nuevaDireccion.calle}
                        onChange={handleNuevaDireccionChange}
                        placeholder="Enter street name"
                      />
                    </div>
                  </div>

                  <div className="form-row">
                    <div className="form-group">
                      <label>NÚMERO DE CASA N°°</label>
                      <input
                        type="text"
                        name="numero"
                        value={nuevaDireccion.numero}
                        onChange={handleNuevaDireccionChange}
                        placeholder="Enter building number"
                      />
                    </div>
                    <div className="form-group">
                      <label>ENTRADA</label>
                      <input
                        type="text"
                        name="entrada"
                        value={nuevaDireccion.entrada}
                        onChange={handleNuevaDireccionChange}
                        placeholder="1"
                      />
                    </div>
                  </div>

                  <div className="form-row">
                    <div className="form-group">
                      <label>PISO</label>
                      <input
                        type="text"
                        name="piso"
                        value={nuevaDireccion.piso}
                        onChange={handleNuevaDireccionChange}
                        placeholder="7"
                      />
                    </div>
                    <div className="form-group">
                      <label>DEPARTAMENTO</label>
                      <input
                        type="text"
                        name="apartamento"
                        value={nuevaDireccion.apartamento}
                        onChange={handleNuevaDireccionChange}
                        placeholder="76"
                      />
                    </div>
                    <div className="form-group">
                      <label>INTERCOMUNICADOR</label>
                      <input
                        type="text"
                        name="intercom"
                        value={nuevaDireccion.intercom}
                        onChange={handleNuevaDireccionChange}
                        placeholder="7621"
                      />
                    </div>
                  </div>

                  <button className="btn-save-address" onClick={handleGuardarDireccion}>
                    Guardar direccion
                  </button>
                </div>
              )}

              <button className="btn-continue-payment" onClick={handleContinuarPago}>
                Continuar con metodo de pago
              </button>
            </div>
          </div>

          {/* Sección Derecha: Cart (con toggle) */}
          <div className={`placing-cart ${cartMinimized ? "minimized" : ""}`}>
            <div className="cart-header">
              <h3 className="cart-title">Cart</h3>
              <button className="btn-toggle-cart-small" onClick={toggleCart}>
                <i className={`fa-solid ${cartMinimized ? "fa-chevron-down" : "fa-chevron-up"}`}></i>
              </button>
            </div>

            {!cartMinimized && (
              <>
                <div className="cart-options">
                  <button 
                    className={`cart-option ${metodoEntrega === "pickup" ? "active" : ""}`}
                    onClick={() => setMetodoEntrega("pickup")}
                  >
                    Pick-up
                  </button>
                  <button 
                    className={`cart-option ${metodoEntrega === "delivery" ? "active" : ""}`}
                    onClick={() => setMetodoEntrega("delivery")}
                  >
                    Delivery
                  </button>
                </div>

                <div className="cart-items">
                  {carrito.map((item) => (
                    <div key={item.id} className="cart-item">
                      <div className="cart-item-info">
                        <h5 className="cart-item-name">{item.nombre}</h5>
                        <p className="cart-item-desc">{item.descripcion}</p>
                        <span className="cart-item-price">+ {item.cantidad || 1} = ${item.precio}</span>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="cart-total">
                  <span>Total:</span>
                  <span className="cart-total-amount">${total.toLocaleString()}</span>
                </div>

                <button className="btn-order" onClick={handlePedido}>
                  Ordenar
                </button>
              </>
            )}

            {cartMinimized && (
              <div className="cart-minimized-info">
                <span className="cart-minimized-total">${total.toLocaleString()}</span>
                <span className="cart-minimized-items">{carrito.length} items</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default PlacingOrder;