
const db = require("../config/database");

// Consulta general de platos y categorias
const consultaBase = `
    SELECT
        p.idPlato AS id,
        p.nombre,
        p.descripcion,
        p.precio,
        p.disponible,
        p.imagen,
        p.calorias,
        p.rating,
        p.tiempo,
        t.idTipo_Plato AS id_categoria,
        t.nombre_tipo AS nombre_categoria,
        CASE t.nombre_tipo
            WHEN 'Desayunos' THEN 'desayunos'
            WHEN 'Caldos' THEN 'caldos'
            WHEN 'Bebidas' THEN 'bebidas'
            WHEN 'Platos Fuertes' THEN 'platos'
            ELSE LOWER(t.nombre_tipo)
        END AS categoria
    FROM plato p
    INNER JOIN tipo_plato t
    ON p.Tipo_Plato_idTipo_Plato = t.idTipo_Plato
`;

// Convertir los datos al formato del frontend
const formatearProducto = (producto) => ({
    ...producto,
    precio: Number(producto.precio),
    disponible: Boolean(producto.disponible),
    rating: producto.rating === null
        ? null
        : Number(producto.rating)
});

// Consultar todos los productos
const obtenerProductos = async (req, res) => {
    try {
        const { categoria } = req.query;

        let sql = consultaBase;
        const parametros = [];

        if (categoria && categoria !== "todos") {
            sql += `
                WHERE LOWER(t.nombre_tipo) = ?
                OR (? = 'platos'
                AND t.nombre_tipo = 'Platos Fuertes')
            `;

            parametros.push(
                String(categoria).toLowerCase(),
                String(categoria).toLowerCase()
            );
        }

        sql += " ORDER BY p.idPlato";

        const [productos] = await db.query(sql, parametros);

        res.json(productos.map(formatearProducto));

    } catch (error) {
        console.error(error);
        res.status(500).json({
            mensaje: "Error al consultar los productos"
        });
    }
};

// Consultar producto por ID
const obtenerProductoPorId = async (req, res) => {
    try {
        const { id } = req.params;

        const [productos] = await db.query(
            consultaBase + " WHERE p.idPlato = ?",
            [id]
        );

        if (productos.length === 0) {
            return res.status(404).json({
                mensaje: "Producto no encontrado"
            });
        }

        res.json(formatearProducto(productos[0]));

    } catch (error) {
        console.error(error);
        res.status(500).json({
            mensaje: "Error al consultar el producto"
        });
    }
};

// Validar datos
const datosValidos = (datos) => {
    return (
        typeof datos.nombre === "string" &&
        datos.nombre.trim().length > 0 &&
        datos.nombre.trim().length <= 45 &&
        typeof datos.precio === "number" &&
        Number.isFinite(datos.precio) &&
        datos.precio > 0 &&
        datos.precio <= 99999999.99 &&
        Number.isInteger(datos.id_categoria) &&
        datos.id_categoria > 0 &&
        typeof datos.disponible === "boolean" &&
        (datos.calorias == null ||
            (Number.isInteger(datos.calorias) &&
            datos.calorias >= 0)) &&
        (datos.rating == null ||
            (typeof datos.rating === "number" &&
            datos.rating >= 0 &&
            datos.rating <= 5))
    );
};

// Registrar un nuevo producto
const crearProducto = async (req, res) => {
    try {
        const {
            nombre,
            descripcion,
            precio,
            disponible = true,
            imagen,
            calorias,
            rating,
            tiempo,
            id_categoria
        } = req.body;

        if (!datosValidos({
            nombre, precio, disponible,
            id_categoria, calorias, rating
        })) {
            return res.status(400).json({
                mensaje: "Datos del producto no validos"
            });
        }

        const [categorias] = await db.query(
            "SELECT idTipo_Plato FROM tipo_plato WHERE idTipo_Plato = ?",
            [id_categoria]
        );

        if (categorias.length === 0) {
            return res.status(400).json({
                mensaje: "La categoria no existe"
            });
        }

        const [resultado] = await db.query(
            `INSERT INTO plato (
                nombre,
                descripcion,
                precio,
                disponible,
                imagen,
                calorias,
                rating,
                tiempo,
                Tipo_Plato_idTipo_Plato
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
            [
                nombre.trim(),
                descripcion ?? null,
                precio,
                disponible,
                imagen ?? null,
                calorias ?? null,
                rating ?? null,
                tiempo ?? null,
                id_categoria
            ]
        );

        res.status(201).json({
            mensaje: "Producto registrado correctamente",
            id: resultado.insertId
        });

    } catch (error) {
        console.error(error);
        res.status(500).json({
            mensaje: "Error al registrar el producto"
        });
    }
};

// Actualizar un producto
const actualizarProducto = async (req, res) => {
    try {
        const { id } = req.params;

        const {
            nombre,
            descripcion,
            precio,
            disponible,
            imagen,
            calorias,
            rating,
            tiempo,
            id_categoria
        } = req.body;

        if (!datosValidos(req.body)) {
            return res.status(400).json({
                mensaje: "Datos del producto no validos"
            });
        }

        const [categorias] = await db.query(
            "SELECT idTipo_Plato FROM tipo_plato WHERE idTipo_Plato = ?",
            [id_categoria]
        );

        if (categorias.length === 0) {
            return res.status(400).json({
                mensaje: "La categoria no existe"
            });
        }

        const [resultado] = await db.query(
            `UPDATE plato SET
                nombre = ?,
                descripcion = ?,
                precio = ?,
                disponible = ?,
                imagen = ?,
                calorias = ?,
                rating = ?,
                tiempo = ?,
                Tipo_Plato_idTipo_Plato = ?
            WHERE idPlato = ?`,
            [
                nombre.trim(),
                descripcion ?? null,
                precio,
                disponible,
                imagen ?? null,
                calorias ?? null,
                rating ?? null,
                tiempo ?? null,
                id_categoria,
                id
            ]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                mensaje: "Producto no encontrado"
            });
        }

        res.json({
            mensaje: "Producto actualizado correctamente",
            id: Number(id)
        });

    } catch (error) {
        console.error(error);
        res.status(500).json({
            mensaje: "Error al actualizar el producto"
        });
    }
};

// Eliminar producto
const eliminarProducto = async (req, res) => {
    try {
        const { id } = req.params;

        const [resultado] = await db.query(
            "DELETE FROM plato WHERE idPlato = ?",
            [id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                mensaje: "Producto no encontrado"
            });
        }

        res.json({
            mensaje: "Producto eliminado correctamente",
            id: Number(id)
        });

    } catch (error) {
        console.error(error);

        if (error.code === "ER_ROW_IS_REFERENCED_2") {
            return res.status(409).json({
                mensaje: "El producto tiene registros relacionados"
            });
        }

        res.status(500).json({
            mensaje: "Error al eliminar el producto"
        });
    }
};

// Cambiar disponibilidad
const cambiarDisponibilidad = async (req, res) => {
    try {
        const { id } = req.params;
        const { disponible } = req.body;

        if (typeof disponible !== "boolean") {
            return res.status(400).json({
                mensaje: "La disponibilidad debe ser true o false"
            });
        }

        const [resultado] = await db.query(
            "UPDATE plato SET disponible = ? WHERE idPlato = ?",
            [disponible, id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                mensaje: "Producto no encontrado"
            });
        }

        res.json({
            mensaje: "Disponibilidad actualizada correctamente",
            id: Number(id),
            disponible
        });

    } catch (error) {
        console.error(error);
        res.status(500).json({
            mensaje: "Error al cambiar disponibilidad"
        });
    }
};

module.exports = {
    obtenerProductos,
    obtenerProductoPorId,
    crearProducto,
    actualizarProducto,
    eliminarProducto,
    cambiarDisponibilidad
};
