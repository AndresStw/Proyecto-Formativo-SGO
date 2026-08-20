# Base de datos - Sabor Caleño SGO

Este directorio contiene la definición de la base de datos (SQL) y datos de ejemplo pensados para pruebas y consultas básicas del proyecto SGO (Sabor Caleño).

Contenido:

- schema.sql: Sentencias DDL para crear las tablas principales (PostgreSQL)
- seed.sql: Datos de ejemplo para poblar la base y ejecutar consultas de demostración

Objetivo:
Crear una base de datos mínima pero práctica que soporte:
- Gestión de usuarios y roles
- Gestión de clientes y direcciones
- Productos, proveedores e inventario
- Pedidos y detalle de pedidos
- Encuestas y respuestas (Customer Experience)
- Definición de procesos y tareas (BPMN simplificado)
- Auditoría básica

Cómo usar (PostgreSQL):

1. Crear la base de datos (ejemplo):

```bash
createdb sgo_db
psql -d sgo_db -f "Trimestre IV/DB SQL/schema.sql"
psql -d sgo_db -f "Trimestre IV/DB SQL/seed.sql"
```

2. Consultas de ejemplo:

- Productos con bajo stock (umbral 50):
```sql
SELECT p.id, p.name, i.quantity
FROM products p
JOIN inventory i USING (product_id)
WHERE i.quantity < 50;
```

- Pedidos por cliente:
```sql
SELECT o.id, o.created_at, o.status, o.total_amount
FROM orders o
WHERE o.customer_id = 1
ORDER BY o.created_at DESC;
```

- Ventas totales por producto (sumando cantidades en order_items):
```sql
SELECT p.id, p.name, SUM(oi.quantity) AS total_sold, SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi
JOIN products p ON p.id = oi.product_id
GROUP BY p.id, p.name
ORDER BY total_sold DESC;
```

- Promedio de puntuación de encuesta (si se usan ratings numéricos):
```sql
SELECT AVG((a.answer_text)::INTEGER) AS avg_rating
FROM survey_answers a
JOIN survey_questions q ON q.id = a.question_id
WHERE q.question_type = 'rating' AND q.survey_id = 1;
```

Estructura propuesta (resumen ER):

- users (1) --- (N) user_roles (N) --- (1) roles
- customers (1) --- (N) addresses
- products (1) --- (1) inventory
- orders (1) --- (N) order_items --- (1) products
- surveys (1) --- (N) survey_questions
- survey_responses (1) --- (N) survey_answers (N) --- (1) survey_questions

Buenas prácticas y siguientes pasos:

- En producción, no almacenar contraseñas en texto ni hashes de ejemplo; integrar un proveedor de autenticación o usar bcrypt con salt.
- Añadir constraints y validaciones adicionales según reglas de negocio (e.g., estados válidos para orders, triggers para recalcular total_amount).
- Crear scripts de migración (Flyway/Liquibase) si se requiere control de versiones de esquema.
- Diseñar respaldos periódicos y políticas de retención para audit_logs e información sensible.

Si quieres, puedo:
- Generar un diagrama ER visual (PNG/SVG) y añadirlo al repo.
- Añadir constraints/triggers para mantener total_amount consistente en orders.
- Simplificar o expandir el esquema según módulos que prefieran (finanzas, producción, empleados).

