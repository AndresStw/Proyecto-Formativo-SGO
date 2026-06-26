
let pedidos = [
    {
        id: 1,
        mesa: "Mesa 3",
        hora: "12:05 PM",
        platos: ["1 Hamburguesa ", "1 Papas a la francesa", "1 Limonada"],
        nota: "Sin cebolla",
        estado: "pendiente"
    },
    {
        id: 2,
        mesa: "Mesa 7",
        hora: "12:10 PM",
        platos: ["2 Pizza familiar", "1 Gaseosa 1.5L"],
        nota: "",
        estado: "listo"
    },
    {
        id: 3,
        mesa: "Domicilio",
        hora: "12:14 PM",
        platos: ["1 Bandeja paisa", "1 Jugo de mora"],
        nota: "Entregar en bolsa sellada",
        estado: "pendiente"
    },
    {
        id: 4,
        mesa: "Mesa 1",
        hora: "11:50 AM",
        platos: ["1 Ensalada César", "1 Agua con gas"],
        nota: "",
        estado: "pendiente"
    }
];

function renderPedidos() {
    const contenedor = document.getElementById("contenedorPedidos");
    contenedor.innerHTML = "";
 
    if (pedidos.length === 0) {
        contenedor.innerHTML = `<p class="sin-pedidos">No hay pedidos registrados.</p>`;
        actualizarContadores();
        return;
    }
 
    pedidos.forEach(pedido => {
        const estaListo = pedido.estado === "listo";
 
        const listaPlatos = pedido.platos
            .map(plato => `<li>${plato}</li>`)
            .join("");
 
        const card = document.createElement("div");
        card.className = `pedido-card ${estaListo ? "listo" : ""}`;
        card.innerHTML = `
            <div class="pedido-card-header">
                <h3>${pedido.mesa}</h3>
                <span class="badge-mesa">#${pedido.id}</span>
            </div>
 
            <span class="badge-estado ${estaListo ? "listo" : "pendiente"}">
                ${estaListo ? "Listo" : "Pendiente"}
            </span>
 
            <p class="hora"><i class="fa-regular fa-clock"></i> ${pedido.hora}</p>
 
            <ul>${listaPlatos}</ul>
 
            ${pedido.nota ? `<p class="nota"><i class="fa-solid fa-circle-info"></i> ${pedido.nota}</p>` : ""}
 
            <button
                class="btn-listo"
                onclick="marcarComoListo(${pedido.id})"
                ${estaListo ? "disabled" : ""}
            >
                ${estaListo ? '<i class="fa-solid fa-check"></i> Listo' : '<i class="fa-solid fa-utensils"></i> Marcar como listo'}
            </button>
        `;
 
        contenedor.appendChild(card);
    });
 
    actualizarContadores();
}
 

function marcarComoListo(idPedido) {
    const pedido = pedidos.find(p => p.id === idPedido);
    if (!pedido) return;
 
    pedido.estado = "listo";
    renderPedidos();
 
    
}
 
function actualizarContadores() {
    const pendientes = pedidos.filter(p => p.estado === "pendiente").length;
    const listos = pedidos.filter(p => p.estado === "listo").length;
 
    document.getElementById("contadorPendientes").textContent = pendientes;
    document.getElementById("contadorListos").textContent = listos;
    document.getElementById("contadorTotal").textContent = pedidos.length;
}
 
document.addEventListener("DOMContentLoaded", renderPedidos);
 