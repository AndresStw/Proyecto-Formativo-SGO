## Base de datos — Archivos SQL

Por ahora los tengo alojados en DB SQL

## REQRIMIENTO PARA ESCALABILIDAD Y ORDEN
Para las consultas use el siguiente nombre "01_select_queries.sql" 

Resumen
Este directorio contiene los scripts SQL necesarios para crear y poblar la base de datos del proyecto:
- `schema.sql` — crea la estructura (tablas, índices, constraints).
- `seed.sql` — datos iniciales (registros de ejemplo/semilla).
Ejecutar primero `schema.sql` y luego `seed.sql`.

Requisitos
- XAMPP (MySQL/MariaDB) u otro servidor MySQL compatible
- MySQL Workbench o phpMyAdmin (opcional)
- MySQL client (CLI) para importación por línea de comandos

Configuración de desarrollo (ejemplo)
- Host: `localhost` (o `127.0.0.1`)
- Puerto: `3306`
- Base de datos: `sgo_db` (recomendado; cambiar si es necesario)
- Usuario (desarrollo): `root`
- Contraseña root (XAMPP por defecto): (vacía)

Credenciales recomendadas para la aplicación (ejemplo)
- Usuario: `sgo_user`
- Contraseña de ejemplo: `SGOdevPass123!`
--- Recordar  que son simuladas esto no quiere decir que las dejaremos así.

Pasos para importar (CLI)
1. Arranca MySQL en XAMPP.
2. Crear la base de datos (si no existe):
   ```bash
   mysql -u root -e "CREATE DATABASE IF NOT EXISTS sgo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"