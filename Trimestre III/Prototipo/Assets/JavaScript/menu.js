document.addEventListener("DOMContentLoaded", () => {
    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    actualizarContador();
    const botonesFiltro = document.querySelectorAll(".btn-filtro");
    const itemsMenu = document.querySelectorAll(".item-menu");
    botonesFiltro.forEach(boton => {
        boton.addEventListener("click", () => {
            botonesFiltro.forEach(b => b.classList.remove("active"));
            boton.classList.add("active");
            const categoria = boton.getAttribute("data-categoria");
            itemsMenu.forEach(item => {
                if (categoria === "todos" || item.getAttribute("data-categoria") === categoria) {
                    item.style.display = "block";
                } else {
                    item.style.display = "none";
                }
            });
        });
    });
    const botonesAgregar = document.querySelectorAll(".btn-agregar");
    botonesAgregar.forEach(boton => {
        boton.addEventListener("click", () => {
            const id = boton.getAttribute("data-id");
            const nombre = boton.getAttribute("data-name") || boton.getAttribute("data-nombre");
            const precio = parseInt(boton.getAttribute("data-precio"));
            const existe = carrito.find(item => item.id === id);
            if (existe) {
                existe.cantidad++;
            } else {
                carrito.push({ id, nombre, precio, cantidad: 1 });
            }
            localStorage.setItem("carrito", JSON.stringify(carrito));
            actualizarContador();
        });
    });
    function actualizarContador() {
        const contador = document.getElementById("contador-carrito");
        if (contador) {
            const totalItems = carrito.reduce((sum, item) => sum + item.cantidad, 0);
            contador.textContent = totalItems;
        }
    }
});