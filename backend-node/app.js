
const express = require("express");
const cors = require("cors");
require("dotenv").config();

const productosRoutes = require("./routes/productosRoutes");

const app = express();

app.use(cors());
app.use(express.json());

// Rutas de productos
app.use("/productos", productosRoutes);

// Ruta principal
app.get("/", (req, res) => {
    res.json({
        mensaje: "Bienvenido a Sabor Caleño",
        estado: "API funcionando",
        tecnologia: "Node.js y Express"
    });
});

// Comprobar servidor
app.get("/health", (req, res) => {
    res.json({
        status: "ok",
        service: "Sabor Caleño SGO"
    });
});

// Iniciar servidor
const PORT = process.env.PORT || 8000;

app.listen(PORT, () => {
    console.log(
        `Servidor Sabor Caleño funcionando en http://localhost:${PORT}`
    );
});
