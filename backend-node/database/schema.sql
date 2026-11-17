
-- Proyecto Sabor Caleño SGO
-- Modulo: Menu y Catalogo
-- Base de datos MySQL

CREATE DATABASE IF NOT EXISTS sabor_caleno_sgo
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE sabor_caleno_sgo;

CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    precio FLOAT NOT NULL,
    categoria VARCHAR(50),
    disponible BOOLEAN NOT NULL DEFAULT TRUE
);
