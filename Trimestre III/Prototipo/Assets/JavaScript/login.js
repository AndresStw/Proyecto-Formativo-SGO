document.addEventListener("DOMContentLoaded", () => {
    const formLogin = document.getElementById("form-login");
    if (formLogin) {
        formLogin.addEventListener("submit", (e) => {
            e.preventDefault();
            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value.trim();

            const resultado = iniciarSesion(email, password);
            if (resultado.success) {
                alert(`¡Bienvenido ${resultado.usuario.nombre}!`);
                redirigirSegunRol(resultado.usuario);
            } else {
                alert("Credenciales incorrectas. Verifica tus datos.");
            }
        });
    }
});