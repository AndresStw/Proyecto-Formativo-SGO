document.addEventListener("DOMContentLoaded", () => {
    if (!verificarSesion()) return;
    const usuario = obtenerUsuarioLogueado();
    const nombreAdmin = document.getElementById("nombre-admin");
    const labelRol = document.getElementById("label-rol");
    if (nombreAdmin) nombreAdmin.textContent = usuario.nombre;
    if (labelRol) {
        labelRol.textContent = usuario.rol.toUpperCase();
        const clasesColor = {
            admin: "bg-danger",
            cocinero: "bg-primary",
            mesero: "bg-info text-dark",
            cajero: "bg-success"
        };
        labelRol.className = `badge ${clasesColor[usuario.rol] || "bg-secondary"}`;
    }
    const itemsMenu = document.querySelectorAll("[data-permiso]");
    itemsMenu.forEach(item => {
        const permisosPermitidos = item.getAttribute("data-permiso").split(",");
        if (!permisosPermitidos.includes(usuario.rol)) {
            item.remove();
        }
    });
    const botonesEstado = document.querySelectorAll(".btn-cambiar-estado");
    botonesEstado.forEach(boton => {
        boton.addEventListener("click", (e) => {
            const fila = e.target.closest("tr");
            const celdaEstado = fila.querySelector(".estado-pedido");
            if (usuario.rol === "cocinero") {
                celdaEstado.className = "estado-pedido bg-info text-dark p-2 rounded";
                celdaEstado.textContent = "Listo para Servir";
                boton.remove();
            } else if (usuario.rol === "cajero" || usuario.rol === "admin") {
                celdaEstado.className = "estado-pedido bg-success text-white p-2 rounded";
                celdaEstado.textContent = "Pagado";
                boton.textContent = "Archivar";
            } else {
                alert("Tu rol no tiene permisos para modificar este estado.");
            }
        });
    });
    const btnSalirAdmin = document.getElementById("btn-salir-admin");
    if (btnSalirAdmin) {
        btnSalirAdmin.addEventListener("click", cerrarSesion);
    }
});