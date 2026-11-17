
const test = require("node:test");
const assert = require("node:assert/strict");

const API = "http://localhost:8000";

// Prueba 1: servidor funcionando
test("Servidor funcionando", async () => {
    const respuesta = await fetch(`${API}/health`);
    assert.equal(respuesta.status, 200);

    const datos = await respuesta.json();
    assert.equal(datos.status, "ok");
});

// Prueba 2: listar los 21 platos
test("Listar todos los productos", async () => {
    const respuesta = await fetch(`${API}/productos`);
    assert.equal(respuesta.status, 200);

    const productos = await respuesta.json();
    assert.ok(Array.isArray(productos));
    assert.equal(productos.length, 21);
});

// Prueba 3: consultar un producto por ID
test("Consultar producto por ID", async () => {
    const respuesta = await fetch(`${API}/productos/1`);
    assert.equal(respuesta.status, 200);

    const producto = await respuesta.json();
    assert.equal(producto.id, 1);
    assert.equal(producto.nombre, "Arepa con Panela");
});

// Prueba 4: producto inexistente
test("Producto no encontrado", async () => {
    const respuesta = await fetch(`${API}/productos/999999`);
    assert.equal(respuesta.status, 404);
});

// Prueba 5: consultar categorias
test("Listar categorias", async () => {
    const respuesta = await fetch(`${API}/categorias`);
    assert.equal(respuesta.status, 200);

    const categorias = await respuesta.json();
    assert.equal(categorias.length, 4);
});

// Pruebas 6 a 9: filtros por categoria
const filtros = [
    { categoria: "desayunos", cantidad: 5 },
    { categoria: "caldos", cantidad: 5 },
    { categoria: "bebidas", cantidad: 2 },
    { categoria: "platos", cantidad: 9 }
];

for (const filtro of filtros) {
    test(`Filtrar categoria: ${filtro.categoria}`, async () => {
        const respuesta = await fetch(
            `${API}/productos?categoria=${filtro.categoria}`
        );

        assert.equal(respuesta.status, 200);

        const productos = await respuesta.json();
        assert.equal(productos.length, filtro.cantidad);

        for (const producto of productos) {
            assert.equal(producto.categoria, filtro.categoria);
        }
    });
}

// Prueba 10: comprobar las 21 imagenes
test("Imagenes de los productos funcionando", async () => {
    const respuesta = await fetch(`${API}/productos`);
    assert.equal(respuesta.status, 200);

    const productos = await respuesta.json();
    assert.equal(productos.length, 21);

    for (const producto of productos) {
        assert.ok(producto.imagen);

        const imagen = await fetch(`${API}${producto.imagen}`);

        assert.equal(
            imagen.status,
            200,
            `Error en imagen de ${producto.nombre}`
        );

        assert.ok(
            imagen.headers.get("content-type")?.startsWith("image/")
        );

        await imagen.arrayBuffer();
    }
});



test("CRUD completo de productos", async () => {
    let id;

    const producto = {
        nombre: "Producto prueba automatizada",
        descripcion: "Prueba del modulo",
        precio: 15000,
        id_categoria: 4,
        disponible: true
    };

    try {
        // Crear producto
        const crear = await fetch(`${API}/productos`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(producto)
        });

        assert.equal(crear.status, 201);

        const creado = await crear.json();
        id = creado.id;
        assert.ok(id);

        // Consultar producto
        const consultar = await fetch(`${API}/productos/${id}`);
        assert.equal(consultar.status, 200);

        const datos = await consultar.json();
        assert.equal(datos.nombre, producto.nombre);

        // Actualizar producto
        const actualizar = await fetch(`${API}/productos/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                ...producto,
                precio: 18000
            })
        });

        assert.equal(actualizar.status, 200);

        // Cambiar disponibilidad
        const disponibilidad = await fetch(
            `${API}/productos/${id}/disponibilidad`,
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    disponible: false
                })
            }
        );

        assert.equal(disponibilidad.status, 200);

        // Verificar cambios
        const verificar = await fetch(`${API}/productos/${id}`);
        assert.equal(verificar.status, 200);

        const actualizado = await verificar.json();

        assert.equal(actualizado.precio, 18000);
        assert.equal(actualizado.disponible, false);

    } finally {
        // Eliminar solamente el producto de prueba
        if (id) {
            const eliminar = await fetch(`${API}/productos/${id}`, {
                method: "DELETE"
            });

            assert.equal(eliminar.status, 200);

            const comprobar = await fetch(`${API}/productos/${id}`);
            assert.equal(comprobar.status, 404);
        }
    }
});



// Prueba 12: rechazar producto sin nombre
test("Rechazar producto sin nombre", async () => {
    const respuesta = await fetch(`${API}/productos`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nombre: "",
            precio: 15000,
            id_categoria: 4,
            disponible: true
        })
    });

    assert.equal(respuesta.status, 400);
});

// Prueba 13: rechazar precio negativo
test("Rechazar precio negativo", async () => {
    const respuesta = await fetch(`${API}/productos`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nombre: "Producto invalido",
            precio: -5000,
            id_categoria: 4,
            disponible: true
        })
    });

    assert.equal(respuesta.status, 400);
});

// Prueba 14: rechazar categoria inexistente
test("Rechazar categoria inexistente", async () => {
    const respuesta = await fetch(`${API}/productos`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nombre: "Producto invalido",
            precio: 15000,
            id_categoria: 999999,
            disponible: true
        })
    });

    assert.equal(respuesta.status, 400);
});

// Prueba 15: rechazar disponibilidad incorrecta
test("Rechazar disponibilidad incorrecta", async () => {
    const respuesta = await fetch(`${API}/productos`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nombre: "Producto invalido",
            precio: 15000,
            id_categoria: 4,
            disponible: "incorrecto"
        })
    });

    assert.equal(respuesta.status, 400);
});
