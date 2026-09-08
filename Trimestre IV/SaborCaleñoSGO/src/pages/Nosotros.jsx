import React from "react";
import { Link } from "react-router-dom";

function Nosotros (){
     returns(
       
        <div className="row g-5">
            <div className="col-md-6">
                <h4 className="fw-bold mb-3">Horarios de Atención</h4>
                <ul className="list-unstyled mb-4">
                    <li><i className="fa-regular fa-clock me-2 text-warning"></i><b>Lunes a Viernes:</b> 11:30 AM - 9:00 PM</li>
                    <li><i className="fa-regular fa-clock me-2 text-warning"></i><b>Sábados y Domingos:</b> 11:00 AM - 10:00 PM</li>
                </ul>

                <h4 className="fw-bold mb-3">Nuestra Misión</h4>
                <p className="text-muted">Traer un pedacito del Valle del Cauca a tu mesa, rescatando las recetas tradicionales de las abuelas caleñas con ingredientes frescos y un servicio impecable.</p>
            </div>

            <div className="col-md-6">
                <div className="card p-4 border-0 shadow-sm bg-white">
                    <h5 className="fw-bold mb-3">Déjanos un mensaje</h5>
                    <form>
                        <div className="mb-3">
                            <label className="form-label small fw-semibold">Nombre</label>
                        </div>
                        <div className="mb-3">
                            <label className="form-label small fw-semibold">Correo</label>
                        </div>
                        <div className="mb-3">
                            <label className="form-label small fw-semibold">Mensaje</label>
                            <textarea className="form-control" rows="3" required></textarea>
                        </div>
                        <button type="submit" className="btn w-100 text-white fw-bold" style="background: linear-gradient(90deg, #ff6b00, #ff8c00, #ffb347); border: none;">Enviar</button>
                    </form>
                </div>
            </div>
        </div>
     );
}
export default Nosotros;
