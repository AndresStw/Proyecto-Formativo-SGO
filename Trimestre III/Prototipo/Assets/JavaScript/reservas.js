document.addEventListener("DOMContentLoaded", () => {
    const formReserva = document.getElementById("form-reserva");

    if (formReserva) {
        formReserva.addEventListener("submit", (e) => {
            e.preventDefault();
            
            const nombre = document.getElementById("reserva-nombre").value;
            const fecha = document.getElementById("reserva-fecha").value;
            const hora = document.getElementById("reserva-hora").value;
            const personas = document.getElementById("reserva-personas").value;

            alert(`Reserva confirmada con éxito.\nA nombre de: ${nombre}\nMesa para: ${personas} personas el día ${fecha} a las ${hora}.`);
            formReserva.reset();
        });
    }
}); 