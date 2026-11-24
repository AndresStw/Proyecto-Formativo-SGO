# Sabor Caleño SGO — Backend API

API del sistema desarrollada con FastAPI, SQLAlchemy y Alembic. La autenticación usa JWT, sesiones persistidas y una tabla única `users` con el rol de cada cuenta.

## Preparar el entorno local

Desde la raíz del repositorio, en PowerShell:

```powershell
if (-not (Test-Path .venv)) { python -m venv .venv }
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Conserva tu `.env` actual si ya tiene configurada la conexión a MySQL. Inicia la API con:

```powershell
uvicorn app.main:app --reload --port 8000
```

La documentación de OpenAPI está en `http://127.0.0.1:8000/docs`.

## Autenticación y cuentas

Todas las rutas de autenticación están bajo `/api/v1/auth` y aparecen agrupadas como **Autenticación** en OpenAPI.

| Método | Ruta | Acceso | Función |
| --- | --- | --- | --- |
| `POST` | `/api/v1/auth/register` | Público | Crea una cuenta `CLIENTE` |
| `POST` | `/api/v1/auth/login` | Público | Inicia sesión y devuelve un JWT |
| `GET` | `/api/v1/auth/me` | Bearer token | Consulta el perfil actual |
| `PUT` | `/api/v1/auth/me` | Bearer token | Actualiza el perfil actual |
| `POST` | `/api/v1/auth/logout` | Bearer token | Revoca la sesión actual |
| `POST` | `/api/v1/auth/forgot-password` | Público | Registra un enlace de recuperación en los logs |
| `POST` | `/api/v1/auth/reset-password` | Público | Cambia la contraseña con un token válido |
| `GET` | `/api/v1/auth/users` | `ADMIN` o `SUPER_ADMIN` | Lista cuentas sin devolver hashes |
| `POST` | `/api/v1/auth/users` | `ADMIN` o `SUPER_ADMIN` | Crea una cuenta de personal |

### Registrar una cuenta

Se requieren nombres separados. `segundoNombre` y `segundoApellido` son opcionales; no se acepta un campo combinado `nombre`.

```json
{
  "primerNombre": "Ana",
  "segundoNombre": "María",
  "primerApellido": "Torres",
  "segundoApellido": "Pérez",
  "email": "ana@example.com",
  "telefono": "+573001234567",
  "direccion": "Cali",
  "password": "Clave123"
}
```

Las respuestas de registro e inicio de sesión usan `access_token`, `token_type`, `expires_in` y `user`. El perfil contiene campos Python como `id`, `first_name`, `email` y `role`.

### Crear una cuenta de personal

Envía un Bearer token de administrador y uno de estos roles: `MESERO`, `COCINERO`, `CAJERO` o `ADMIN`. El registro público solo asigna `CLIENTE`.

```json
{
  "primerNombre": "Luis",
  "primerApellido": "Prueba",
  "email": "luis@example.com",
  "telefono": "3001112233",
  "rol": "MESERO",
  "password": "Clave123"
}
```

En las rutas protegidas, selecciona **Authorization → Bearer Token** y pega el JWT. En PowerShell puedes ejecutar las pruebas automatizadas con:

```powershell
..venv\Scripts\Activate.ps1
pytest -q
```

## Pedidos y reservas

Las rutas de negocio están agrupadas por módulo en OpenAPI:

- **Pedidos:** `/api/v1/pedidos`
- **Reservas:** `/api/v1/reservas`

Las tablas de negocio comienzan vacías. Para cargar los estados y modalidades de pedidos, ejecuta `python -m scripts.seed_pedidos` después de aplicar las migraciones. Crear pedidos y reservas también requiere cuentas, platos y mesas existentes.

## Base de datos y migraciones

El backend utiliza `users` como tabla activa de cuentas. La tabla fuente existente `usuario` se conserva, y las cuentas se copian a `users` manteniendo sus IDs y hashes. Las claves foráneas de pedidos, mesas, reservas, inventario y ventas apuntan a `users.id`.

La cadena de Alembic contiene estas revisiones:

1. `84b4b07429c2`: crea `users` y `user_sessions` si no existen.
2. `c9a7d2e84110`: completa los campos de cuenta, adopta registros existentes y configura la recuperación de contraseña.
3. `e09827dd3b4d`: crea las 14 tablas de negocio.

La base local está en `e09827dd3b4d (head)`. Para aplicar las revisiones pendientes en otro entorno, configura `DATABASE_URL` en `.env` y ejecuta:

```powershell
alembic upgrade head
```

Comprueba si el modelo y la base siguen alineados con:

```powershell
alembic check
```

## Configuración CORS

Los orígenes, métodos y encabezados se definen con `CORS_ORIGINS`, `CORS_ALLOW_METHODS` y `CORS_ALLOW_HEADERS`. En producción agrega el origen exacto del frontend; no uses `*` junto con credenciales.

## Convenciones de código

Los identificadores, clases y funciones usan nombres en inglés —por ejemplo `User`, `first_name` y `get_current_user`— para facilitar búsquedas y mantenimiento del código. Los campos de entrada en español se conservan donde el proyecto los requiere.
