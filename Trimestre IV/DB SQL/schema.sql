-- schema.sql
-- Esquema para Sabor Caleño SGO (PostgreSQL)

-- Roles y usuarios
CREATE TABLE roles (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(150),
  email VARCHAR(150) UNIQUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE user_roles (
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
  PRIMARY KEY (user_id, role_id)
);

-- Clientes y direcciones
CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  phone VARCHAR(30),
  email VARCHAR(150),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE addresses (
  id SERIAL PRIMARY KEY,
  customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE,
  line1 VARCHAR(255) NOT NULL,
  line2 VARCHAR(255),
  city VARCHAR(100),
  state VARCHAR(100),
  postal_code VARCHAR(30),
  country VARCHAR(100) DEFAULT 'Colombia'
);

-- Productos, proveedores e inventario
CREATE TABLE suppliers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  contact_name VARCHAR(150),
  phone VARCHAR(30),
  email VARCHAR(150)
);

CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  sku VARCHAR(50) UNIQUE,
  name VARCHAR(200) NOT NULL,
  description TEXT,
  price NUMERIC(10,2) NOT NULL DEFAULT 0,
  cost NUMERIC(10,2) DEFAULT 0,
  supplier_id INTEGER REFERENCES suppliers(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE inventory (
  product_id INTEGER PRIMARY KEY REFERENCES products(id) ON DELETE CASCADE,
  quantity INTEGER NOT NULL DEFAULT 0,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Pedidos y detalle de pedidos
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_id INTEGER REFERENCES customers(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  status VARCHAR(50) DEFAULT 'pending',
  total_amount NUMERIC(12,2) DEFAULT 0
);

CREATE TABLE order_items (
  id SERIAL PRIMARY KEY,
  order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
  product_id INTEGER REFERENCES products(id),
  quantity INTEGER NOT NULL DEFAULT 1,
  unit_price NUMERIC(10,2) NOT NULL
);

-- Encuestas y respuestas (para Customer Experience)
CREATE TABLE surveys (
  id SERIAL PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  description TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE survey_questions (
  id SERIAL PRIMARY KEY,
  survey_id INTEGER REFERENCES surveys(id) ON DELETE CASCADE,
  question_text TEXT NOT NULL,
  question_type VARCHAR(50) DEFAULT 'text' -- text, rating, choice
);

CREATE TABLE survey_responses (
  id SERIAL PRIMARY KEY,
  survey_id INTEGER REFERENCES surveys(id) ON DELETE CASCADE,
  customer_id INTEGER REFERENCES customers(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE survey_answers (
  id SERIAL PRIMARY KEY,
  response_id INTEGER REFERENCES survey_responses(id) ON DELETE CASCADE,
  question_id INTEGER REFERENCES survey_questions(id) ON DELETE CASCADE,
  answer_text TEXT
);

-- Procesos y tareas (para BPMN / flujos operativos)
CREATE TABLE process_flows (
  id SERIAL PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  description TEXT
);

CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  process_flow_id INTEGER REFERENCES process_flows(id) ON DELETE SET NULL,
  name VARCHAR(200) NOT NULL,
  assigned_user_id INTEGER REFERENCES users(id),
  status VARCHAR(50) DEFAULT 'todo',
  due_date DATE
);

-- Auditoría básica
CREATE TABLE audit_logs (
  id BIGSERIAL PRIMARY KEY,
  event_time TIMESTAMP WITH TIME ZONE DEFAULT now(),
  actor_id INTEGER REFERENCES users(id),
  action VARCHAR(200),
  details JSONB
);

-- Índices útiles
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_inventory_quantity ON inventory(quantity);
