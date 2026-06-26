document.addEventListener("DOMContentLoaded", () => {
    // Validar sesión activa
    const usuarioLogueado = JSON.parse(localStorage.getItem("usuarioLogueado"));

    if (!usuarioLogueado) {
        alert("Acceso denegado. Debes iniciar sesión.");
        window.location.href = "../Pages/login.html";
        return;
    }

    const nombreAdmin = document.getElementById("nombre-admin");
    const labelRol = document.getElementById("label-rol");
    
    if (nombreAdmin) nombreAdmin.textContent = usuarioLogueado.nombre;
    if (labelRol) {
        labelRol.textContent = usuarioLogueado.rol.toUpperCase();
        // Cambiar color del badge según el rol
        const clasesColor = {
            admin: "bg-danger",
            cocinero: "bg-primary",
            mesero: "bg-info text-dark",
            cajero: "bg-success"
        };
        labelRol.className = `badge ${clasesColor[usuarioLogueado.rol] || "bg-secondary"}`;
    }

   const rolActual = usuarioLogueado.rol;
    
    const itemsMenu = document.querySelectorAll("[data-permiso]");

    itemsMenu.forEach(item => {
        const permisosPermitidos = item.getAttribute("data-permiso").split(",");
        
        if (!permisosPermitidos.includes(rolActual)) {
            item.remove(); 
        }
    });

    const botonesEstado = document.querySelectorAll(".btn-cambiar-estado");
    botonesEstado.forEach(boton => {
        boton.addEventListener("click", (e) => {
            const fila = e.target.closest("tr");
            const celdaEstado = fila.querySelector(".estado-pedido");
            
            if (rolActual === "cocinero") {
                celdaEstado.className = "estado-pedido bg-info text-dark p-2 rounded";
                celdaEstado.textContent = "Listo para Servir";
                boton.remove(); // El cocinero termina su flujo aquí
            } else if (rolActual === "cajero" || rolActual === "admin") {
                celdaEstado.className = "estado-pedido bg-success text-white p-2 rounded";
                celdaEstado.textContent = "Pagado";
                boton.textContent = "Archivar";
            } else {
                alert("Tu rol no tiene permisos para modificar este estado.");
            }
        });
    });

    // Cerrar Sesión
    const btnSalirAdmin = document.getElementById("btn-salir-admin");
    if (btnSalirAdmin) {
        btnSalirAdmin.addEventListener("click", () => {
            localStorage.removeItem("usuarioLogueado");
            window.location.href = "../index.html";
        });
    }
});