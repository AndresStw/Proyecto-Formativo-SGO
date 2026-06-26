const Validaciones = {
    validarEmail: (email) => {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;//analizar 
        return regex.test(email);
    },
    validarPassword: (password) => {
        return password.length >= 6;
    },
    validarTelefono: (telefono) => {
        return telefono.length === 10 && !isNaN(telefono);
    }
};