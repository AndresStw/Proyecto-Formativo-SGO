CREATE DATABASE IF NOT EXISTS sabor_caleno_sgo
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE sabor_caleno_sgo;

-- Tabla anterior de productos
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    precio FLOAT NOT NULL,
    categoria VARCHAR(50),
    disponible BOOLEAN NOT NULL DEFAULT TRUE
);

-- Tabla de categorias
CREATE TABLE IF NOT EXISTS tipo_plato (
    idTipo_Plato INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tipo VARCHAR(45) NOT NULL
);

-- Tabla del menu
CREATE TABLE IF NOT EXISTS plato (
    idPlato INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    disponible BOOLEAN DEFAULT TRUE,
    imagen VARCHAR(255),
    calorias INT,
    rating DECIMAL(2,1),
    tiempo VARCHAR(20),
    Tipo_Plato_idTipo_Plato INT NOT NULL,

    FOREIGN KEY (Tipo_Plato_idTipo_Plato)
    REFERENCES tipo_plato(idTipo_Plato)
);