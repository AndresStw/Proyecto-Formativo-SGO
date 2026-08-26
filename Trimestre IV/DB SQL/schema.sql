-- schema.sql
-- Esquema para Sabor Caleno SGO (MariaDB)
-- Generado a partir del MER del restaurante Tiene las correciones de ambiegudas 


CREATE DATABASE IF NOT EXISTS sabor_caleno_sgo DEFAULT CHARACTER

SET
  utf8mb4 -- No eliminar Hasta que corrijamos el error de carachteres
  DEFAULT COLLATE utf8mb4_unicode_ci;


USE sabor_caleno_sgo; -- No eliminaaaaaaaaaaar

-- TABLAS DE USUARIOS Y PERSONAS

-- Usuario base (persona)
CREATE TABLE
  Usuario (
    idUsuario INT PRIMARY KEY AUTO_INCREMENT,
    primerNombre VARCHAR(45) NOT NULL,
    segundoNombre VARCHAR(45),
    primerApellido VARCHAR(45) NOT NULL,
    segundoApellido VARCHAR(45),
    email VARCHAR(150) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

-- Direcciones
CREATE TABLE
  Direccion (
    idDireccion INT PRIMARY KEY AUTO_INCREMENT,
    Usuario_idUsuario INT NOT NULL,
    ciudad VARCHAR(45) NOT NULL,
    calle VARCHAR(45) NOT NULL,
    barrio VARCHAR(45) NOT NULL,
    FOREIGN KEY (Usuario_idUsuario) REFERENCES Usuario (idUsuario) ON DELETE CASCADE
  );

-- Telefonos
CREATE TABLE
  Telefono (
    idTelefono INT PRIMARY KEY AUTO_INCREMENT,
    Usuario_idUsuario INT NOT NULL,
    telefono CHAR(15) NOT NULL,
    operador VARCHAR(45) NOT NULL,
    FOREIGN KEY (Usuario_idUsuario) REFERENCES Usuario (idUsuario) ON DELETE CASCADE
  );

-- ROLES DE USUARIOS (HERENCIA)

-- Cliente
CREATE TABLE
  Cliente (
    id_cliente VARCHAR(45) PRIMARY KEY,
    Usuario_idUsuario INT NOT NULL,
    nivelCliente VARCHAR(45) NOT NULL DEFAULT 'Estandar',
    estadoMembresia VARCHAR(45) NOT NULL DEFAULT 'Activa',
    FOREIGN KEY (Usuario_idUsuario) REFERENCES Usuario (idUsuario) ON DELETE CASCADE
  );

-- Cajero
CREATE TABLE
  Cajero (
    id_cajero INT PRIMARY KEY AUTO_INCREMENT,
    Usuario_idUsuario INT NOT NULL,
    caja_asignada VARCHAR(45) NOT NULL,
    FOREIGN KEY (Usuario_idUsuario) REFERENCES Usuario (idUsuario) ON DELETE CASCADE
  );

-- Administrador
CREATE TABLE
  Administrador (
    id_administrador INT PRIMARY KEY AUTO_INCREMENT,
    Usuario_idUsuario INT NOT NULL,
    nivel_acceso VARCHAR(45) NOT NULL DEFAULT 'Basico',
    FOREIGN KEY (Usuario_idUsuario) REFERENCES Usuario (idUsuario) ON DELETE CASCADE
  );

-- Cocinero
CREATE TABLE
  Cocinero (
    id_cocinero INT PRIMARY KEY AUTO_INCREMENT,
    Usuario_idUsuario INT NOT NULL,
    especialidad VARCHAR(45) NOT NULL,
    turno VARCHAR(45) NOT NULL,
    FOREIGN KEY (Usuario_idUsuario) REFERENCES Usuario (idUsuario) ON DELETE CASCADE
  );

-- Mesero
CREATE TABLE
  Mesero (
    id_mesero INT PRIMARY KEY AUTO_INCREMENT,
    Usuario_idUsuario INT NOT NULL,
    zona_asignada VARCHAR(45) NOT NULL,
    FOREIGN KEY (Usuario_idUsuario) REFERENCES Usuario (idUsuario) ON DELETE CASCADE
  );

-- MESAS
CREATE TABLE
  Mesa (
    idMesa INT PRIMARY KEY AUTO_INCREMENT,
    capacidad INT NOT NULL,
    numero_mesa VARCHAR(10) NOT NULL UNIQUE, -- Foranea 
    Mesero_id_mesero INT NOT NULL,
    FOREIGN KEY (Mesero_id_mesero) REFERENCES Mesero (id_mesero)
  );

-- CATALOGOS (TABLAS MAESTRAS)

-- Modalidad de pedido
CREATE TABLE
  modalidadPedido (
    id_modalidad INT PRIMARY KEY AUTO_INCREMENT,
    nombreModalidad VARCHAR(45) NOT NULL,
    descripcion VARCHAR(45)
  );

-- Estado del pedido
CREATE TABLE
  Estado_Pedido (
    idEstado_Pedido INT PRIMARY KEY AUTO_INCREMENT,
    nombre_estado VARCHAR(45) NOT NULL
  );

-- Tipo de plato
CREATE TABLE
  Tipo_Plato (
    idTipo_Plato INT PRIMARY KEY AUTO_INCREMENT,
    nombre_tipo VARCHAR(45) NOT NULL
  );

-- Metodo de pago
CREATE TABLE
  MetodoPago (
    idMetodo_Pago INT PRIMARY KEY AUTO_INCREMENT,
    metodo VARCHAR(45) NOT NULL
  );

-- PLATOS
CREATE TABLE
  Plato (
    idPlato INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(45) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL DEFAULT 0,
    disponible BOOLEAN DEFAULT TRUE,
    Tipo_Plato_idTipo_Plato INT NOT NULL,-- resumir
    FOREIGN KEY (Tipo_Plato_idTipo_Plato) REFERENCES Tipo_Plato (idTipo_Plato) -- Esta esta super dificil de entender
  );

-- PEDIDOS

CREATE TABLE
  Pedido (
    idPedido INT PRIMARY KEY AUTO_INCREMENT,
    fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tiempo_preparacion INT COMMENT 'Tiempo en minutos', -- Cambiarlo a int
    hora_entrega DATETIME,
    Mesero_id_mesero INT NOT NULL,
    Mesa_idMesa INT,
    Cliente_id_cliente VARCHAR(45) NOT NULL,-- Abreviar
    modalidadPedido_id_modalidad INT NOT NULL,
    Estado_Pedido_idEstado_Pedido INT NOT NULL,
    FOREIGN KEY (Mesero_id_mesero) REFERENCES Mesero (id_mesero),
    FOREIGN KEY (Mesa_idMesa) REFERENCES Mesa (idMesa) ON DELETE SET NULL,
    FOREIGN KEY (Cliente_id_cliente) REFERENCES Cliente (id_cliente),
    FOREIGN KEY (modalidadPedido_id_modalidad) REFERENCES modalidadPedido (id_modalidad),
    FOREIGN KEY (Estado_Pedido_idEstado_Pedido) REFERENCES Estado_Pedido (idEstado_Pedido)
  );

-- Detalle del pedido
CREATE TABLE
  Detalle_Pedido (
    idDetalle_Pedido INT PRIMARY KEY AUTO_INCREMENT,
    Pedido_idPedido INT NOT NULL,
    Plato_idPlato INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    Observaciones TEXT,
    FOREIGN KEY (Pedido_idPedido) REFERENCES Pedido (idPedido) ON DELETE CASCADE,
    FOREIGN KEY (Plato_idPlato) REFERENCES Plato (idPlato)
  );


-- INSUMOS E INVENTARIO

CREATE TABLE
  Insumo (
    idInsumo INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(45) NOT NULL,
    unidad_medida VARCHAR(45) NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL DEFAULT 0
  );

CREATE TABLE
  Inventario (
    idInventario INT PRIMARY KEY AUTO_INCREMENT,
    Insumo_idInsumo INT NOT NULL,
    stock_actual INT NOT NULL DEFAULT 0,
    stock_minimo INT NOT NULL DEFAULT 5,
    Administrador_id_administrador INT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (Insumo_idInsumo) REFERENCES Insumo (idInsumo) ON DELETE CASCADE,
    FOREIGN KEY (Administrador_id_administrador) REFERENCES Administrador (id_administrador)
  );

-- RECETAS
CREATE TABLE
  Receta (
    idReceta INT PRIMARY KEY AUTO_INCREMENT,
    Plato_idPlato INT NOT NULL,
    descripcion TEXT,
    FOREIGN KEY (Plato_idPlato) REFERENCES Plato (idPlato) ON DELETE CASCADE
  );

CREATE TABLE
  Detalle_Receta (
    idDetalle_Receta INT PRIMARY KEY AUTO_INCREMENT,
    Receta_idReceta INT NOT NULL,
    Insumo_idInsumo INT NOT NULL,
    cantidad DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (Receta_idReceta) REFERENCES Receta (idReceta) ON DELETE CASCADE,
    FOREIGN KEY (Insumo_idInsumo) REFERENCES Insumo (idInsumo)
  );

-- VENTAS
CREATE TABLE
  Venta (
    idventa INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(12, 2) NOT NULL DEFAULT 0,
    Pedido_idPedido INT NOT NULL,
    Metodo_Pago_idMetodo_Pago INT NOT NULL,
    Cajero_id_cajero INT NOT NULL,
    FOREIGN KEY (Pedido_idPedido) REFERENCES Pedido (idPedido),
    FOREIGN KEY (Metodo_Pago_idMetodo_Pago) REFERENCES MetodoPago (idMetodo_Pago),
    FOREIGN KEY (Cajero_id_cajero) REFERENCES Cajero (id_cajero)
  );

-- INDICES
CREATE INDEX idx_usuario_email ON Usuario (email);

CREATE INDEX idx_pedido_cliente ON Pedido (Cliente_id_cliente);

CREATE INDEX idx_pedido_estado ON Pedido (Estado_Pedido_idEstado_Pedido);

CREATE INDEX idx_pedido_mesero ON Pedido (Mesero_id_mesero);

CREATE INDEX idx_detalle_pedido ON Detalle_Pedido (Pedido_idPedido);

CREATE INDEX idx_inventario_insumo ON Inventario (Insumo_idInsumo);

CREATE INDEX idx_receta_plato ON Receta (Plato_idPlato);

CREATE INDEX idx_venta_fecha ON Venta (fecha);