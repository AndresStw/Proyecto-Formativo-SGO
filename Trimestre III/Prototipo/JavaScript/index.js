document.querySelector('.btn-ingresar').addEventListener('click', function(event){

    event.preventDefault();

  
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();

    // Usuarios del sistema
    const usuarios = {

        'admin@saborcaleno.com': {
            password: '123',
            rol: 'Administrador',
            redireccion: 'pages/administrador.html'
        },

        'cliente@saborcaleno.com': {
            password: '1234',
            rol: 'Cliente',
            redireccion: 'pages/cliente.html'
        },

        'cocinero@saborcaleno.com': {
            password: '5678',
            rol: 'Cocinero',
            redireccion: 'cocinero.html'
        },

        'cajero@saborcaleno.com': {
            password: '9999',
            rol: 'Cajero',
            redireccion: 'pages/cajero.html'
        }

    };

    
    if(email === "" || password === ""){

        Swal.fire({
            icon: "warning",
            title: "Campos Vacíos",
            text: "Por favor complete los campos",
            confirmButtonColor: '#ffb347'
        });

        return;
    }
  
    const usuario = usuarios[email];

    if(usuario && usuario.password === password){

        Swal.fire({
            icon: 'success',
            title: 'Inicio Exitoso',
            text: "Bienvenido" + " " + usuario.rol,  // segunda forma ${usuario.rol}
            confirmButtonColor: '#ffb347'
        }).then(() => {

            window.location.href = usuario.redireccion;

        });

    }else{

        Swal.fire({
            icon: "error",
            title: "Credenciales incorrectas",
            text: "Correo o contraseña inválidos",
            confirmButtonColor: '#ffb347'
        });

    }

});