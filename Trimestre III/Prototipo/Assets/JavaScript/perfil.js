document.addEventListener("DOMContentLoaded", () => {
    if (!verificarSesion()) return;
    const usuario = obtenerUsuarioLogueado();
    const nombrePerfil = document.getElementById("perfil-nombre");
    const correoPerfil = document.getElementById("perfil-correo");
    const telefonoPerfil = document.getElementById("perfil-telefono");
    if (nombrePerfil) nombrePerfil.textContent = usuario.nombre;
    if (correoPerfil) correoPerfil.textContent = usuario.email;
    if (telefonoPerfil) telefonoPerfil.textContent = usuario.telefono || "No registrado";
    const btnCerrarSesion = document.getElementById("btn-cerrar-sesion");
    if (btnCerrarSesion) {
        btnCerrarSesion.addEventListener("click", cerrarSesion);
    }
});