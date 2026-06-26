document.addEventListener("DOMContentLoaded", () => {
    const btnLogin = document.getElementById("btn-login");
    const usuarioLogueado = JSON.parse(localStorage.getItem("usuarioLogueado"));

    if (btnLogin && usuarioLogueado) {
        btnLogin.textContent = "Mi Cuenta";
        btnLogin.classList.remove("btn-dark");
        btnLogin.classList.add("btn-warning", "text-dark", "fw-bold");
    }

    if (btnLogin) {
        btnLogin.addEventListener("click", () => {
            if (usuarioLogueado) {
                if (usuarioLogueado.rol === "admin") {
                    window.location.href = "Admin/dashboard.html";
                } else {
                    window.location.href = "Pages/perfil.html";
                }
            } else {
                window.location.href = "Pages/login.html";
            }
        });
    }
});