document.addEventListener("DOMContentLoaded", () => {
    actualizarBotonLogin();

    const formLogin = document.getElementById("form-login");
    if (formLogin) {
        formLogin.addEventListener("submit", (e) => {
            e.preventDefault();
            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value.trim();

            const resultado = iniciarSesion(email, password);
            if (resultado.success) {
                const modal = bootstrap.Modal.getInstance(document.getElementById("loginModal"));
                if (modal) modal.hide();

                Swal.fire({
                    icon: 'success',
                    title: '¡Bienvenido!',
                    text: `Has iniciado sesión como ${resultado.usuario.nombre}`,
                    timer: 2000,
                    showConfirmButton: false
                });

                setTimeout(() => {
                    redirigirSegunRol(resultado.usuario);
                }, 1500);

                formLogin.reset();
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Credenciales incorrectas',
                    text: 'Revisa tu correo y contraseña',
                    timer: 2000,
                    showConfirmButton: false
                });
            }
        });
    }
});