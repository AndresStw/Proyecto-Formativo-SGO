// src/pages/ChatPedido.jsx

/*
  Componente: ChatPedido
  Descripcion: Mockup tipo WhatsApp para simular un chat de pedidos.
  Funcionalidades:
    - Chat simulado con respuestas automaticas
    - Botones rapidos para agregar platos
    - Carrito lateral con total
*/

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaCheckDouble, FaPaperPlane, FaWhatsapp } from "react-icons/fa";
import "../assets/CSS/chatpedido.css";

const platos = [
  { id: 1, nombre: "Sancocho valluno", precio: 18000 },
  { id: 2, nombre: "Arroz atollado", precio: 16000 },
  { id: 3, nombre: "Aborrajado", precio: 9000 },
  { id: 4, nombre: "Champús", precio: 6000 },
];

const dinero = (valor) => `$${valor.toLocaleString("es-CO")}`;

function ChatPedido() {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
    }
  }, [navigate]);

  const [mensajes, setMensajes] = useState([
    {
      id: 1,
      autor: "restaurante",
      texto: "¡Hola! 👋 Soy el asistente de Sabor Caleño.",
      hora: "Ahora",
    },
    {
      id: 2,
      autor: "restaurante",
      texto: "Puedes escribir tu pedido o elegir una opción para comenzar.",
      hora: "Ahora",
    },
  ]);
  const [texto, setTexto] = useState("");
  const [pedido, setPedido] = useState([]);

  const responder = (entrada) => {
    const normalizado = entrada.toLowerCase();
    if (
      normalizado.includes("menú") ||
      normalizado.includes("menu") ||
      normalizado.includes("hola")
    ) {
      return "Nuestro menú de hoy: Sancocho valluno $18.000, Arroz atollado $16.000, Aborrajado $9.000 y Champús $6.000. Pulsa un plato para agregarlo.";
    }
    if (normalizado.includes("pedido") || normalizado.includes("carrito")) {
      return pedido.length
        ? `Tu pedido lleva ${pedido.map((item) => `${item.cantidad} ${item.nombre}`).join(", ")}. Total: ${dinero(pedido.reduce((t, i) => t + i.precio * i.cantidad, 0))}.`
        : "Aún no tienes productos en el pedido. Elige un plato del menú para agregarlo.";
    }
    if (normalizado.includes("confirmar") || normalizado.includes("listo")) {
      return pedido.length
        ? "¡Pedido recibido! 🎉 Es una simulación: la cocina lo tendría listo aproximadamente en 30 minutos."
        : "Agrega al menos un plato antes de confirmar tu pedido.";
    }
    return "Puedo ayudarte con el menú, agregar platos o revisar tu pedido. Prueba escribiendo «menú» o usa los botones.";
  };

  const enviar = (mensaje = texto) => {
    const limpio = mensaje.trim();
    if (!limpio) return;
    const hora = new Date().toLocaleTimeString("es-CO", {
      hour: "2-digit",
      minute: "2-digit",
    });
    setMensajes((actuales) => [
      ...actuales,
      { id: Date.now(), autor: "cliente", texto: limpio, hora },
      {
        id: Date.now() + 1,
        autor: "restaurante",
        texto: responder(limpio),
        hora,
      },
    ]);
    setTexto("");
  };

  const agregar = (plato) => {
    setPedido((actual) => {
      const existe = actual.find((item) => item.id === plato.id);
      return existe
        ? actual.map((item) =>
            item.id === plato.id
              ? { ...item, cantidad: item.cantidad + 1 }
              : item,
          )
        : [...actual, { ...plato, cantidad: 1 }];
    });
    setMensajes((actuales) => [
      ...actuales,
      {
        id: Date.now(),
        autor: "cliente",
        texto: `Quiero ${plato.nombre}`,
        hora: "Ahora",
      },
      {
        id: Date.now() + 1,
        autor: "restaurante",
        texto: `${plato.nombre} agregado a tu pedido. ¿Deseas algo más?`,
        hora: "Ahora",
      },
    ]);
  };

  const total = pedido.reduce(
    (suma, item) => suma + item.precio * item.cantidad,
    0,
  );

  return (
    <main className="chat-page">
      <section className="chat-shell" aria-label="Chat simulado de pedidos">
        <header className="chat-header">
          <div className="chat-avatar">
            <FaWhatsapp />
          </div>
          <div>
            <h1>Sabor Caleño</h1>
            <p>
              <span className="online-dot"></span> En línea · chat simulado
            </p>
          </div>
          <span className="simulation-badge">DEMO</span>
        </header>

        <div className="chat-body">
          <div className="chat-notice">
            Los mensajes de este chat son una simulación para realizar pedidos.
          </div>
          {mensajes.map((mensaje) => (
            <div
              key={mensaje.id}
              className={`message-row ${mensaje.autor === "cliente" ? "message-row-client" : ""}`}
            >
              <div
                className={`message ${mensaje.autor === "cliente" ? "message-client" : "message-business"}`}
              >
                <span>{mensaje.texto}</span>
                <small>
                  {mensaje.hora}{" "}
                  {mensaje.autor === "cliente" && <FaCheckDouble />}
                </small>
              </div>
            </div>
          ))}
          <div className="quick-actions">
            {platos.map((plato) => (
              <button key={plato.id} onClick={() => agregar(plato)}>
                {plato.nombre}
                <b>{dinero(plato.precio)}</b>
              </button>
            ))}
          </div>
        </div>

        <div className="order-summary">
          <div>
            <strong>Tu pedido</strong>
            <span>
              {pedido.length
                ? `${pedido.reduce((s, item) => s + item.cantidad, 0)} producto(s) · ${dinero(total)}`
                : "Vacío"}
            </span>
          </div>
          <button
            disabled={!pedido.length}
            onClick={() => enviar("confirmar pedido")}
          >
            Confirmar pedido
          </button>
        </div>
        <form
          className="chat-input"
          onSubmit={(e) => {
            e.preventDefault();
            enviar();
          }}
        >
          <input
            value={texto}
            onChange={(e) => setTexto(e.target.value)}
            placeholder="Escribe tu pedido..."
            aria-label="Mensaje"
          />
          <button type="submit" aria-label="Enviar mensaje">
            <FaPaperPlane />
          </button>
        </form>
      </section>
    </main>
  );
}

export default ChatPedido;
