-- seed.sql
-- Datos de ejemplo para pruebas y consultas

-- Roles
INSERT INTO roles (name) VALUES ('admin'), ('manager'), ('clerk') ON CONFLICT DO NOTHING;

-- Usuarios (passwords are example hashes; replace before production)
INSERT INTO users (username, password_hash, full_name, email) VALUES
('admin','$2y$12$ExampleHashForAdmin','Administrador SGO','admin@saborcaleño.test'),
('jdoe','$2y$12$ExampleHashJdoe','Juan Doe','jdoe@saborcaleño.test')
ON CONFLICT DO NOTHING;

-- Asignar roles
INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id FROM users u, roles r WHERE u.username='admin' AND r.name='admin'
ON CONFLICT DO NOTHING;

-- Proveedores
INSERT INTO suppliers (name, contact_name, phone, email) VALUES
('Distribuciones Caleñas','Luisa Perez','+57 3000000000','luisa@distribucion.test')
ON CONFLICT DO NOTHING;

-- Productos
INSERT INTO products (sku, name, description, price, cost, supplier_id) VALUES
('PROD-CAF-001','Café Sabor Caleño 250g','Café tostado molido, origen Valle','12.50','6.50',1),
('PROD-ARE-001','Arepa Tradicional','Arepa de maíz blanco','1.20','0.50',1)
ON CONFLICT DO NOTHING;

-- Inventario
INSERT INTO inventory (product_id, quantity) VALUES
(1, 120),
(2, 500)
ON CONFLICT (product_id) DO UPDATE SET quantity = EXCLUDED.quantity;

-- Clientes
INSERT INTO customers (name, phone, email) VALUES
('Restaurante El Sabor','+57 3120000000','restaurante@sabor.test'),
('Cliente Casa','+57 3100000000','cliente1@casa.test')
ON CONFLICT DO NOTHING;

-- Direcciones
INSERT INTO addresses (customer_id, line1, city, state, postal_code) VALUES
(1,'Calle 10 # 5-20','Cali','Valle del Cauca','760001'),
(2,'Carrera 7 # 12-34','Cali','Valle del Cauca','760002')
ON CONFLICT DO NOTHING;

-- Pedidos y detalles
INSERT INTO orders (customer_id, status, total_amount) VALUES
(1,'completed',50.00),
(2,'pending',3.60)
RETURNING id;

-- Para simplificar, asumimos ordenes 1 y 2 existen
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1,1,3,12.50), -- 3 x Café = 37.50
(1,2,10,1.20), -- 10 x Arepa = 12.00
(2,2,3,1.20)
ON CONFLICT DO NOTHING;

-- Encuesta ejemplo
INSERT INTO surveys (name, description) VALUES ('Encuesta de Satisfacción','Encuesta posventa') ON CONFLICT DO NOTHING;
INSERT INTO survey_questions (survey_id, question_text, question_type) VALUES
(1,'¿Cómo calificaría la calidad del producto?','rating'),
(1,'¿Recomendaría nuestros productos?','choice')
ON CONFLICT DO NOTHING;

-- Respuestas ejemplo
INSERT INTO survey_responses (survey_id, customer_id) VALUES (1,1) RETURNING id;
-- Asumimos response id 1
INSERT INTO survey_answers (response_id, question_id, answer_text) VALUES
(1,1,'5'),
(1,2,'Sí')
ON CONFLICT DO NOTHING;

-- Procesos y tareas
INSERT INTO process_flows (name, description) VALUES ('Pedido a entrega','Flujo desde orden hasta entrega') ON CONFLICT DO NOTHING;
INSERT INTO tasks (process_flow_id, name, assigned_user_id, status) VALUES (1,'Preparar pedido',2,'todo') ON CONFLICT DO NOTHING;

-- Ejemplo de audit log
INSERT INTO audit_logs (actor_id, action, details) VALUES (1,'seed_data','Inserción inicial de datos de ejemplo');
