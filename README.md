## 🔴 EP-01 — Authentication & Accounts (BLOCKING) - ✅ COMPLETED

**Assignee:** Lead
**Framework:** Laravel 11 + Laravel Sanctum

_Architecture Note: Implemented using "Single Table Inheritance" (a single `Usuario` table with a `rol` column) instead of separate tables for Cliente, Mesero, etc. This simplifies queries and maintenance._

**Model Tasks (Laravel - `app/Models/`):**

- [x] `Usuario.php` (idUsuario, names, email, password_hash, telefono, direccion, rol, estado) implementing `HasApiTokens`.

**Endpoint Tasks (`routes/api.php`):**

- [x] `POST /api/register` (Creates user with 'cliente' role by default and returns Token).
- [x] `POST /api/login` (Validates Bcrypt credentials and returns Token).
- [x] `GET /api/me` (Protected route to view profile).
- [x] `PUT /api/me` (Protected route to update profile).
- [x] `POST /api/logout` (Destroys the current token).
- [x] `POST /api/forgot-password` (Sends a simulated reset link to the log file).
- [x] `POST /api/reset-password` (Resets the password using the token).

**Middlewares:**

- [x] `auth:sanctum` (Replaces the old Python `@require_auth` decorator, protects private routes).
- [x] `AdminMiddleware` (Created and registered to protect admin-only routes).

---

# 🚀 Backend Sabor Caleño (Cheat Sheet - Laravel)

Apuntes y comandos esenciales para el desarrollo del backend con Laravel.

## 🧠 Conceptos Clave

- **ORM (Object-Relational Mapping)**: Es una forma de traducir un lenguaje incompatible entre bases de datos relacionales y nuestro código (PHP). Todo esto pasa de forma automática (en Laravel se llama **Eloquent**).

---

## 1. Creación del Proyecto y Configuración Inicial

**Crear el proyecto:**

```bash
composer create-project laravel/laravel sabor-caleno-api
cd sabor-caleno-api
```

**Configurar la Base de Datos:**
Abrimos el archivo `.env` local y configuramos los datos de XAMPP (MySQL):

```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=sabor_caleno_sgo
DB_USERNAME=root
DB_PASSWORD=
```

**Instalar dependencias:**

```bash
composer install
```

---

## 2. Modelos, Migraciones y Controladores

**Crear Modelo y Migración al mismo tiempo:**

```bash
php artisan make:model Usuario -m
```

_(Luego vamos a `database/migrations` para definir las columnas exactas)._

**Crear un Controlador:**

```bash
php artisan make:controller AuthController
```

---

## 3. Seguridad, Autenticación y Middlewares

**Instalar Sanctum (Sistema de Tokens para la API):**

```bash
php artisan install:api
```

**Generar la llave de encriptación (APP_KEY):**

```bash
php artisan key:generate
```

**Crear un Middleware (Ej. para proteger rutas de Admin):**

```bash
php artisan make:middleware AdminMiddleware
```

**Configuración Crucial de Autenticación (Modelo Personalizado):**
Si usas un modelo `Usuario` en lugar de `User`, debes ir a **`config/auth.php`** y cambiar el provider:

```php
'providers' => [
    'users' => [
        'driver' => 'eloquent',
        'model' => App\Models\Usuario::class, // Cambiar App\Models\User::class
    ],
],
```

---

## 4. Ejecución y Mantenimiento (Base de Datos)

**Correr el servidor local:**

```bash
php artisan serve
```

**Ejecutar migraciones (crear tablas):**

```bash
php artisan migrate
```

**Reiniciar la base de datos (¡Borra todos los datos y vuelve a crear las tablas!):**

```bash
php artisan migrate:fresh
```

**Limpiar la caché (configuración, rutas, vistas):**
_(Muy útil cuando los cambios en rutas o .env no se reflejan)_

```bash
php artisan optimize:clear
```

**Crear tabla de recuperación de contraseña (si no existe):**

```bash
php artisan make:migration create_password_reset_tokens_table
```

---

## 5. Pruebas de la API (Postman / PowerShell)

> **Recuerda siempre:** En Postman, usa el formato `Raw -> JSON` en el Body, y agrega el Header `Accept: application/json`.

### A. Registrar un nuevo usuario

- **Método:** `POST`
- **URL:** `http://127.0.0.1:8000/api/register`
- **Body:**

```json
{
    "nombre": "Andres STW",
    "email": "Andre@test.com",
    "telefono": "3001234567",
    "password": "123456",
    "direccion": "Calle 123"
}
```

### B. Iniciar Sesión (Login)

- **Método:** `POST`
- **URL:** `http://127.0.0.1:8000/api/login`
- **Body:**

```json
{
    "email": "Andre@test.com",
    "password": "123456"
}
```

_(Esto te devolverá el `accessToken`, cópialo para las rutas protegidas)._

### C. Ver mi perfil (Ruta Protegida)

- **Método:** `GET`
- **URL:** `http://127.0.0.1:8000/api/me`
- **Auth:** Ve a la pestaña **Auth** -> Tipo **Bearer Token** -> Pega el `accessToken`.
- **Body:** Ninguno.

### D. Actualizar mi perfil (Ruta Protegida)

- **Método:** `PUT`
- **URL:** `http://127.0.0.1:8000/api/me`
- **Auth:** Bearer Token
- **Body:**

```json
{
    "primerNombre": "Andres Actualizado",
    "telefono": "3119998888",
    "direccion": "Nueva Direccion 456"
}
```

### E. Cerrar Sesión (Logout)

- **Método:** `POST`
- **URL:** `http://127.0.0.1:8000/api/logout`
- **Auth:** Bearer Token (el mismo del login).

### F. Solicitar Recuperación de Contraseña

- **Método:** `POST`
- **URL:** `http://127.0.0.1:8000/api/forgot-password`
- **Body:**

```json
{
    "email": "Andre@test.com"
}
```

_(Nota: Revisar el token generado en `storage/logs/laravel.log`)_

### G. Restablecer Contraseña

- **Método:** `POST`
- **URL:** `http://127.0.0.1:8000/api/reset-password`
- **Body:**

```json
{
    "email": "Andre@test.com",
    "token": "PEGA_EL_TOKEN_DEL_LOG_AQUI",
    "password": "nueva_clave_123",
    "password_confirmation": "nueva_clave_123"
}
```

---

## 6. Endpoints de Platos (EP-02) - _En Progreso_

_(Modelos y Migraciones creados. Falta probar Controladores en Postman)_

- `GET /api/productos` (Público)
- `GET /api/productos/{id}` (Público)
- `POST /api/productos` (Requiere Token)
