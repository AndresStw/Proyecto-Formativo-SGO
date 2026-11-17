
const db = require("../config/database");

// Consultar todos los productos
const obtenerProductos = async (req, res) => {
    try {
        const [productos] = await db.query(
            "SELECT * FROM productos"
        );

        res.json(productos);
    } catch (error) {
        console.error("Error al consultar productos:", error);
        res.status(500).json({
            mensaje: "Error al consultar los productos"
        });
    }
};

// Consultar un producto por ID
const obtenerProductoPorId = async (req, res) => {
    try {
        const { id } = req.params;

        const [productos] = await db.query(
            "SELECT * FROM productos WHERE id = ?",
            [id]
        );

        if (productos.length === 0) {
            return res.status(404).json({
                mensaje: "Producto no encontrado"
            });
        }

        res.json(productos[0]);

    } catch (error) {
        console.error("Error al consultar producto:", error);
        res.status(500).json({
            mensaje: "Error al consultar el producto"
        });
    }
};


// Registrar un nuevo producto
const crearProducto = async (req, res) => {
    try {
        const {
            nombre,
            descripcion,
            precio,
            categoria,
            disponible = true
        } = req.body;

        if (!nombre || typeof precio !== "number" || precio <= 0) {
            return res.status(400).json({
                mensaje: "Nombre y precio válido son obligatorios"
            });
        }

        const [resultado] = await db.query(
            `INSERT INTO productos
            (nombre, descripcion, precio, categoria, disponible)
            VALUES (?, ?, ?, ?, ?)`,
            [nombre, descripcion ?? null, precio, categoria ?? null, disponible]
        );

        res.status(201).json({
            mensaje: "Producto registrado correctamente",
            id: resultado.insertId
        });

    } catch (error) {
        console.error("Error al crear producto:", error);
        res.status(500).json({
            mensaje: "Error al registrar el producto"
        });
    }
};


// Actualizar un producto existente
const actualizarProducto = async (req, res) => {
    try {
        const { id } = req.params;

        const {
            nombre,
            descripcion,
            precio,
            categoria,
            disponible
        } = req.body;

        if (!nombre || typeof precio !== "number" ||
            precio <= 0 || typeof disponible !== "boolean") {
            return res.status(400).json({
                mensaje: "Datos del producto no válidos"
            });
        }

        const [resultado] = await db.query(
            `UPDATE productos SET
                nombre = ?,
                descripcion = ?,
                precio = ?,
                categoria = ?,
                disponible = ?
            WHERE id = ?`,
            [
                nombre,
                descripcion ?? null,
                precio,
                categoria ?? null,
                disponible,
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
        console.error("Error al actualizar producto:", error);

        res.status(500).json({
            mensaje: "Error al actualizar el producto"
        });
    }
};


// Eliminar un producto por ID
const eliminarProducto = async (req, res) => {
    try {
        const { id } = req.params;

        const [resultado] = await db.query(
            "DELETE FROM productos WHERE id = ?",
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
        console.error("Error al eliminar producto:", error);

        res.status(500).json({
            mensaje: "Error al eliminar el producto"
        });
    }
};


// Cambiar disponibilidad de un producto
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
            "UPDATE productos SET disponible = ? WHERE id = ?",
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
        console.error("Error al cambiar disponibilidad:", error);

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

