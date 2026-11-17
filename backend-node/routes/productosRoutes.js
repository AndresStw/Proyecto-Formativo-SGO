
const express = require("express");
const router = express.Router();

const {
    obtenerProductos,
    obtenerProductoPorId,
    crearProducto,
    actualizarProducto,
    eliminarProducto,
    cambiarDisponibilidad
} = require("../controllers/productosController");

// Consultar todos los productos
router.get("/", obtenerProductos);

// Consultar un producto por ID
router.get("/:id", obtenerProductoPorId);

// Registrar un nuevo producto
router.post("/", crearProducto);

// Actualizar un producto
router.put("/:id", actualizarProducto);

// Eliminar un producto
router.delete("/:id", eliminarProducto);

// Cambiar disponibilidad
router.patch("/:id/disponibilidad", cambiarDisponibilidad);

module.exports = router;
