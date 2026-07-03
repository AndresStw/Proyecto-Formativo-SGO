const USUARIOS = [
    { email: "admin@saborcaleno.com", password: "admin123", nombre: "Admin", rol: "admin" },
    { email: "cocinero@saborcaleno.com", password: "cocina123", nombre: "Chef", rol: "cocinero" },
    { email: "cliente@saborcaleno.com", password: "cliente123", nombre: "Cliente", rol: "cliente" }
    
];

function obtenerUsuarioLogueado() {
    const data = localStorage.getItem("usuarioLogueado");
    return data ? JSON.parse(data) : null;
}

function verificarSesion() {
    const usuario = obtenerUsuarioLogueado();
    if (!usuario) {
        window.location.href = "../index.html";
        return false;
    }
    return true;
}

function cerrarSesion() {
    localStorage.removeItem("usuarioLogueado");
    window.location.href = "../index.html";
}

function redirigirSegunRol(usuario) {
    if (!usuario) usuario = obtenerUsuarioLogueado();
    if (!usuario) return;

    const base = window.location.pathname.includes("/Pages/") ? "../" : "";
    switch (usuario.rol) {
        case "admin":
            window.location.href = base + "Admin/dashboard.html";
            break;
        case "cocinero":
            window.location.href = base + "Pages/cocinero.html";
            break;
        default:
            window.location.href = base + "Pages/perfil.html";
            break;
    }
}

function iniciarSesion(email, password) {
    const usuario = USUARIOS.find(u => u.email === email && u.password === password);
    if (usuario) {
        const { password: _, ...usuarioSeguro } = usuario;
        localStorage.setItem("usuarioLogueado", JSON.stringify(usuarioSeguro));
        return { success: true, usuario: usuarioSeguro };
    }
    return { success: false, message: "Credenciales incorrectas" };
}

function actualizarBotonLogin(selector = ".btn-login-nav") {
    const btn = document.querySelector(selector);
    if (!btn) return;

    const usuario = obtenerUsuarioLogueado();
    if (usuario) {
    
        btn.textContent = "Login";
        btn.classList.remove("btn-warning", "text-dark", "fw-bold");
        btn.classList.add("btn-dark", "login");
        btn.setAttribute("data-bs-toggle", "modal");
        btn.setAttribute("data-bs-target", "#loginModal");
        btn.onclick = null;
    // if (usuario) {
    //     // btn.textContent = "Mi Cuenta";
    //     btn.classList.remove("btn-dark", "login");
    //     // btn.classList.add("btn-warning", "text-dark", "fw-bold");
    //     btn.onclick = (e) => {
    //         e.preventDefault();
    //         redirigirSegunRol(usuario);
    //     };
    //     btn.removeAttribute("data-bs-toggle");
    //     btn.removeAttribute("data-bs-target");
    // } else {
    //     btn.textContent = "Login";
    //     btn.classList.remove("btn-warning", "text-dark", "fw-bold");
    //     btn.classList.add("btn-dark", "login");
    //     btn.setAttribute("data-bs-toggle", "modal");
    //     btn.setAttribute("data-bs-target", "#loginModal");
    //     btn.onclick = null;
    }
}