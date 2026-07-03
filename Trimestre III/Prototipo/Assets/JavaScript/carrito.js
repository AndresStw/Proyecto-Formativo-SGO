document.addEventListener("DOMContentLoaded", () => {
    const tablaCarrito = document.getElementById("items-carrito");
    const subtotalPedido = document.getElementById("subtotal-pedido");
    const totalPedido = document.getElementById("total-pedido");
    const btnProceder = document.getElementById("btn-proceder");
    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    function renderizarCarrito() {
        if (!tablaCarrito) return;
        tablaCarrito.innerHTML = "";
        if (carrito.length === 0) {
            tablaCarrito.innerHTML = `<tr><td colspan="5" class="text-center text-muted py-4">Tu carrito está vacío.</td></tr>`;
            if(subtotalPedido) subtotalPedido.textContent = "$0";
            if(totalPedido) totalPedido.textContent = "$0";
            return;
        }
        let total = 0;
        carrito.forEach((item, index) => {
            const subtotal = item.precio * item.cantidad;
            total += subtotal;
            tablaCarrito.innerHTML += `
                <tr>
                    <td><b>${item.nombre}</b></td>
                    <td>$${item.precio.toLocaleString()}</td>
                    <td>${item.cantidad}</td>
                    <td>$${subtotal.toLocaleString()}</td>
                    <td>
                        <button class="btn btn-sm btn-danger btn-eliminar" data-index="${index}">
                            <i class="fa-solid fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        if(subtotalPedido) subtotalPedido.textContent = `$${total.toLocaleString()}`;
        if(totalPedido) totalPedido.textContent = `$${total.toLocaleString()}`;
        document.querySelectorAll(".btn-eliminar").forEach(btn => {
            btn.addEventListener("click", (e) => {
                const idx = btn.getAttribute("data-index");
                carrito.splice(idx, 1);
                localStorage.setItem("carrito", JSON.stringify(carrito));
                renderizarCarrito();
            });
        });
    }
    if (btnProceder) {
        btnProceder.addEventListener("click", () => {
            if(carrito.length === 0) {
                alert("No tienes productos en el carrito");
                return;
            }
            alert("¡Pedido realizado con éxito! Simulación de orden enviada.");
            localStorage.removeItem("carrito");
            window.location.href = "perfil.html";
        });
    }
    renderizarCarrito();
});