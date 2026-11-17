
const db = require("../config/database");
const datos = require("./menuData.json");

async function cargarMenu() {
    let conexion;

    try {
        conexion = await db.getConnection();

        await conexion.beginTransaction();

        console.log("Iniciando carga del menu...");

        // Registrar categorias
        for (const categoria of datos.categorias) {

            const [existentes] = await conexion.query(
                "SELECT nombre_tipo FROM tipo_plato WHERE idTipo_Plato = ?",
                [categoria.idTipo_Plato]
            );

            if (existentes.length === 0) {

                await conexion.query(
                    `INSERT INTO tipo_plato
                    (idTipo_Plato, nombre_tipo)
                    VALUES (?, ?)`,
                    [
                        categoria.idTipo_Plato,
                        categoria.nombre_tipo
                    ]
                );

            } else if (
                existentes[0].nombre_tipo !== categoria.nombre_tipo
            ) {
                throw new Error(
                    "Conflicto en categoria: " + categoria.idTipo_Plato
                );
            }

            console.log("Categoria OK:", categoria.nombre_tipo);
        }

        // Registrar platos
        for (const plato of datos.platos) {

            const [existentes] = await conexion.query(
                "SELECT nombre FROM plato WHERE idPlato = ?",
                [plato.idPlato]
            );

            if (existentes.length === 0) {

                await conexion.query(
                    `INSERT INTO plato (
                        idPlato,
                        nombre,
                        descripcion,
                        precio,
                        disponible,
                        imagen,
                        calorias,
                        rating,
                        tiempo,
                        Tipo_Plato_idTipo_Plato
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
                    [
                        plato.idPlato,
                        plato.nombre,
                        plato.descripcion,
                        plato.precio,
                        plato.disponible,
                        plato.imagen,
                        plato.calorias,
                        plato.rating,
                        plato.tiempo,
                        plato.Tipo_Plato_idTipo_Plato
                    ]
                );

            } else if (
                existentes[0].nombre !== plato.nombre
            ) {
                throw new Error(
                    "Conflicto en plato: " + plato.idPlato
                );
            }

            console.log("Plato OK:", plato.nombre);
        }

        await conexion.commit();

        console.log("------------------------------");
        console.log("MENU CARGADO CORRECTAMENTE");
        console.log("Categorias:", datos.categorias.length);
        console.log("Platos:", datos.platos.length);
        console.log("------------------------------");

    } catch (error) {

        if (conexion) {
            await conexion.rollback();
        }

        console.error("Error al cargar el menu:", error.message);
        process.exitCode = 1;

    } finally {

        if (conexion) {
            conexion.release();
        }

        await db.end();
    }
}

cargarMenu();
