document.addEventListener("DOMContentLoaded", () => {
    const formLogin = document.getElementById("form-login");

    if (formLogin) {
        formLogin.addEventListener("submit", (e) => {
            e.preventDefault();

            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value;

            const usuariosPrueba = {
                "admin@saborcaleno.com": { pass: "admin123", nombre: "David Villanueva", rol: "admin" },
                "cocina@saborcaleno.com": { pass: "cocina123", nombre: "Chef Samuel", rol: "cocinero" },
                "mesero@saborcaleno.com": { pass: "mesero123", nombre: "Brandom rojas", rol: "mesero" },
                "caja@saborcaleno.com": { pass: "caja123", nombre: "Cajero kevin", rol: "cajero" }
                // "cliente@saborcaleno.com": { pass: "cliente123", nombre: "Aleja dani", rol: "cliente" }
            };

            if (usuariosPrueba[email] && usuariosPrueba[email].pass === password) {
                const usuario = usuariosPrueba[email];

                localStorage.setItem("usuarioLogueado", JSON.stringify({ //Sugerencia que agrege del chat gpt
                    nombre: usuario.nombre,
                    rol: usuario.rol,
                    correo: email
                }));

                alert(`¡Bienvenido ${usuario.nombre}! Ingresando como ${usuario.rol}.`);
                window.location.href = "../Admin/dashboard.html";

            } else if (email === "cliente@saborcaleno.com" && password === "123456") {
                localStorage.setItem("usuarioLogueado", JSON.stringify({
                    nombre: "Carlos Mario",
                    rol: "cliente",
                    correo: email,
                    telefono: "3157654321"
                }));

                alert("¡Sesión iniciada con éxito!");
                window.location.href = "../index.html";

            } else {
                // Feedback interactivo en caso de error
                alert("Credenciales incorrectas. Verifica el correo y la contraseña de simulación.");
            }
        });
    }
});