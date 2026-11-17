const db = require("../config/database");

const obtenerCategorias = async (req, res) => {
    try {
        const [categorias] = await db.query(`
            SELECT
                idTipo_Plato AS id,
                nombre_tipo AS nombre
            FROM tipo_plato
            ORDER BY idTipo_Plato
        `);

        res.json(categorias);

    } catch (error) {
        console.error(error);

        res.status(500).json({
            mensaje: "Error al obtener las categorias"
        });
    }
};

module.exports = {
    obtenerCategorias
};