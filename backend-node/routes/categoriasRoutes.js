const express = require("express");

const router = express.Router();

const {
    obtenerCategorias
} = require("../controllers/categoriasController");

router.get("/", obtenerCategorias);

module.exports = router;