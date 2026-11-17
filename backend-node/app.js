
const express = require("express");
const cors = require("cors");
const path = require("path");

require("dotenv").config();

const productosRoutes = require("./routes/productosRoutes");
const categoriasRoutes = require("./routes/categoriasRoutes");

const app = express();

app.use(cors());
app.use(express.json());

// Configuracion de imagenes
app.use("/imagenes", express.static(
    path.join(__dirname, "public", "imagenes")
));

// Rutas del sistema
app.use("/productos", productosRoutes);
app.use("/categorias", categoriasRoutes);

// Ruta principal
app.get("/", (req, res) => {
    res.json({
        mensaje: "Bienvenido a Sabor Caleño",
        estado: "API funcionando",
        tecnologia: "Node.js y Express"
    });
});

// Estado del servidor
app.get("/health", (req, res) => {
    res.json({
        status: "ok",
        service: "Sabor Caleño SGO"
    });
});

// Puerto del servidor
const PORT = process.env.PORT || 8000;

app.listen(PORT, () => {
    console.log(`Servidor Sabor Caleño funcionando en http://localhost:${PORT}`);
});
