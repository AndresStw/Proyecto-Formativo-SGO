
# Sabor Caleño SGO - Backend

## Descripción del proyecto

Sabor Caleño SGO es un sistema de gestión para restaurantes
que permite administrar los procesos operativos del negocio.

Actualmente se está realizando la migración del backend
de Python a Node.js, utilizando Express y MySQL.

## Módulo: Menú y Catálogo

Este módulo permite administrar los productos del restaurante,
consultar el menú, registrar nuevos productos, actualizar
información, eliminar productos y controlar su disponibilidad.

## Tecnologías utilizadas

- Node.js
- Express
- MySQL
- XAMPP
- mysql2
- dotenv
- CORS
- Git y GitHub

## Estructura del backend

backend-node/
    config/
        database.js
    controllers/
        productosController.js
    routes/
        productosRoutes.js
    .env.example
    app.js
    package.json
    package-lock.json
    README.md

## Instalación

1. Instalar Node.js y XAMPP.
2. Iniciar MySQL desde XAMPP.
3. Abrir una terminal en la carpeta backend-node.
4. Ejecutar:

    npm install

5. Crear un archivo .env utilizando .env.example.
6. Configurar los datos de conexión a MySQL.

## Configuración de la base de datos

PORT=8000
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=sabor_caleno_sgo
DB_PORT=3306

La base de datos debe existir y contener la tabla productos
antes de utilizar los endpoints.

## Ejecutar el servidor

Modo normal:

    npm start

Modo desarrollo:

    npm run dev

Servidor local:

http://localhost:8000

## Endpoints de productos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /productos | Consultar todos los productos |
| GET | /productos/:id | Consultar un producto |
| POST | /productos | Registrar un producto |
| PUT | /productos/:id | Actualizar un producto |
| DELETE | /productos/:id | Eliminar un producto |
| PATCH | /productos/:id/disponibilidad | Cambiar disponibilidad |

## Ejemplo de registro de producto

{
    "nombre": "Sancocho de Gallina",
    "descripcion": "Plato típico colombiano",
    "precio": 25000,
    "categoria": "Plato fuerte",
    "disponible": true
}

## Ejemplo de cambio de disponibilidad

{
    "disponible": false
}

## Códigos de respuesta HTTP

- 200: Operación exitosa.
- 201: Producto creado correctamente.
- 400: Datos incorrectos.
- 404: Producto no encontrado.
- 500: Error interno del servidor.

## Seguridad

Las credenciales de conexión se administran mediante
variables de entorno.

Los archivos .env y node_modules no deben subirse
al repositorio de GitHub.

## Estado del desarrollo

- Conexión con MySQL implementada.
- Controlador de productos implementado.
- Rutas de productos implementadas.
- Seis endpoints probados manualmente.
- Migración de los demás módulos pendiente.
- Pruebas automatizadas pendientes.
- Autenticación y autorización pendientes.

## Proyecto formativo

Servicio Nacional de Aprendizaje - SENA.
Análisis y Desarrollo de Software.
Proyecto Sabor Caleño SGO.
