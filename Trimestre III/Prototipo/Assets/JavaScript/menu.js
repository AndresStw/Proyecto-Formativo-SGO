document.addEventListener("DOMContentLoaded", () => {
    // Inicializar Carrito Local
    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    actualizarContador();

    // Filtros de Categorías
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

    // Capturar Clicks en Botones "Agregar"
    const botonesAgregar = document.querySelectorAll(".btn-agregar");
    botonesAgregar.forEach(boton => {
        boton.addEventListener("click", () => {
            const id = boton.getAttribute("data-id");
            const nombre = boton.getAttribute("data-name") || boton.getAttribute("data-nombre");
            const precio = parseInt(boton.getAttribute("data-precio"));

            // Verificar si ya existe
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