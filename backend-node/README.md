
# Sabor Caleño SGO - Backend Node.js

## EP-02 - Menú y Catálogo

Este módulo permite gestionar el menú digital del restaurante
Sabor Caleño, facilitando la consulta, creación, actualización,
eliminación y disponibilidad de los platos.

## Tecnologías utilizadas

- Node.js
- Express
- MySQL / MariaDB
- XAMPP
- MySQL2
- Dotenv
- CORS
- Git y GitHub

## Estructura del proyecto

backend-node/
    config/
        database.js
    controllers/
        productosController.js
        categoriasController.js
    database/
        schema.sql
    public/
        imagenes/
    routes/
        productosRoutes.js
        categoriasRoutes.js
    scripts/
        menuData.json
        seedPlatos.js
    tests/
        productos.test.js
    .env.example
    app.js
    package.json
    README.md

## Instalación

Ingresar a la carpeta del backend:

    cd backend-node

Instalar las dependencias:

    npm install

## Configuración de la base de datos

Iniciar MySQL desde XAMPP.

Crear un archivo .env tomando como referencia .env.example.

Variables de entorno:

    PORT=8000
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=
    DB_NAME=sabor_caleno_sgo
    DB_PORT=3306

Configurar las credenciales según el entorno local.

Ejecutar el archivo database/schema.sql desde MySQL Workbench
o MariaDB para crear las tablas necesarias.

## Tablas del módulo

### tipo_plato

- idTipo_Plato
- nombre_tipo

### plato

- idPlato
- nombre
- descripcion
- precio
- disponible
- imagen
- calorias
- rating
- tiempo
- Tipo_Plato_idTipo_Plato

## Carga inicial del menú

Ejecutar:

    npm run seed

Este comando permite cargar las cuatro categorías y los
21 platos originales del restaurante.

## Categorías disponibles

- Desayunos: 5 productos.
- Caldos: 5 productos.
- Bebidas: 2 productos.
- Platos fuertes: 9 productos.

Total: 21 productos.

## Ejecutar el servidor

Modo desarrollo:

    npm run dev

Modo normal:

    npm start

URL del servidor:

    http://localhost:8000

## Endpoints disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /health | Estado del servidor |
| GET | /productos | Consultar todos los platos |
| GET | /productos/:id | Consultar un plato específico |
| GET | /categorias | Consultar categorías |
| GET | /productos?categoria=desayunos | Filtrar productos |
| POST | /productos | Registrar un plato |
| PUT | /productos/:id | Actualizar un plato |
| PATCH | /productos/:id/disponibilidad | Cambiar disponibilidad |
| DELETE | /productos/:id | Eliminar un plato |

## Ejemplo de registro de un producto

    {
        "nombre": "Plato de ejemplo",
        "descripcion": "Descripción del plato",
        "precio": 15000,
        "id_categoria": 4,
        "disponible": true
    }

## Códigos de respuesta HTTP

- 200: Operación exitosa.
- 201: Producto creado correctamente.
- 400: Datos incorrectos.
- 404: Producto no encontrado.
- 409: Conflicto con registros relacionados.
- 500: Error interno del servidor.

## Imágenes

Las imágenes se encuentran en public/imagenes.

Ejemplo de acceso:

    http://localhost:8000/imagenes/Desayunos/Arepapanela-modified.png

El frontend debe agregar la URL del servidor a la ruta
de imagen recibida desde la API.

## Pruebas automatizadas

Mantener MySQL y el servidor funcionando.

Desde otra terminal ejecutar:

    npm test

Las pruebas verifican:

1. Estado del servidor.
2. Listado de productos.
3. Consulta por identificador.
4. Productos inexistentes.
5. Listado de categorías.
6. Filtro de desayunos.
7. Filtro de caldos.
8. Filtro de bebidas.
9. Filtro de platos fuertes.
10. Disponibilidad de imágenes.
11. CRUD completo.
12. Validación de nombre.
13. Validación de precio.
14. Validación de categoría.
15. Validación de disponibilidad.

Último resultado local:

- Pruebas ejecutadas: 15.
- Pruebas exitosas: 15.
- Pruebas fallidas: 0.

Ejecutar las pruebas únicamente en el entorno local de
desarrollo con el menú original cargado.

## Seguridad

Las credenciales se administran mediante variables de entorno.

El archivo .env y la carpeta node_modules no deben
subirse al repositorio.

La autenticación y autorización de las operaciones
administrativas están pendientes de integración con EP-01.

## Estado del desarrollo

- Migración del módulo a Node.js: completada.
- Conexión con MySQL: completada.
- CRUD de productos: completado.
- Categorías e imágenes: completadas.
- Carga inicial del menú: verificada localmente.
- Pruebas automatizadas: completadas.
- Instalación desde una base de datos vacía: verificada localmente.
- Autenticación administrativa: pendiente.
- Integración con frontend: pendiente.
- Integración con otros módulos: pendiente.

## Proyecto formativo

Servicio Nacional de Aprendizaje - SENA.

Programa: Análisis y Desarrollo de Software.

Proyecto: Sabor Caleño SGO.

Épica: EP-02 - Menú y Catálogo.
