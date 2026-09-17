CREATE DATABASE  IF NOT EXISTS `sabor_caleno_sgo2` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `sabor_caleno_sgo2`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: sabor_caleno_sgo2
-- ------------------------------------------------------
-- Server version	9.7.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'b87d7c7d-4ec1-11f1-a54a-36ef0a66de29:1-3250';

--
-- Table structure for table `administrador`
--

DROP TABLE IF EXISTS `administrador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administrador` (
  `id_administrador` int NOT NULL AUTO_INCREMENT,
  `Usuario_idUsuario` int NOT NULL,
  `nivel_acceso` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Basico',
  PRIMARY KEY (`id_administrador`),
  KEY `Usuario_idUsuario` (`Usuario_idUsuario`),
  CONSTRAINT `administrador_ibfk_1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `alerta_inventario`
--

DROP TABLE IF EXISTS `alerta_inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alerta_inventario` (
  `idAlerta` int NOT NULL AUTO_INCREMENT,
  `Insumo_idInsumo` int NOT NULL,
  `stock_actual` int NOT NULL,
  `mensaje` text COLLATE utf8mb4_unicode_ci,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idAlerta`),
  KEY `alerta_inventario_ibfk_1` (`Insumo_idInsumo`),
  CONSTRAINT `alerta_inventario_ibfk_1` FOREIGN KEY (`Insumo_idInsumo`) REFERENCES `insumo` (`idInsumo`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auditoria_usuario`
--

DROP TABLE IF EXISTS `auditoria_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auditoria_usuario` (
  `idAuditoria` int NOT NULL AUTO_INCREMENT,
  `Usuario_idUsuario` int NOT NULL,
  `accion` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `detalle` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idAuditoria`),
  KEY `auditoria_usuario_ibfk_1` (`Usuario_idUsuario`),
  CONSTRAINT `auditoria_usuario_ibfk_1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cajero`
--

DROP TABLE IF EXISTS `cajero`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cajero` (
  `id_cajero` int NOT NULL AUTO_INCREMENT,
  `Usuario_idUsuario` int NOT NULL,
  `caja_asignada` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_cajero`),
  KEY `Usuario_idUsuario` (`Usuario_idUsuario`),
  CONSTRAINT `cajero_ibfk_1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `id_cliente` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Usuario_idUsuario` int NOT NULL,
  `nivelCliente` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Estandar',
  `estadoMembresia` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Activa',
  PRIMARY KEY (`id_cliente`),
  KEY `Usuario_idUsuario` (`Usuario_idUsuario`),
  CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cocinero`
--

DROP TABLE IF EXISTS `cocinero`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cocinero` (
  `id_cocinero` int NOT NULL AUTO_INCREMENT,
  `Usuario_idUsuario` int NOT NULL,
  `especialidad` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `turno` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_cocinero`),
  KEY `Usuario_idUsuario` (`Usuario_idUsuario`),
  CONSTRAINT `cocinero_ibfk_1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `detalle_pedido`
--

DROP TABLE IF EXISTS `detalle_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_pedido` (
  `idDetalle_Pedido` int NOT NULL AUTO_INCREMENT,
  `Pedido_idPedido` int NOT NULL,
  `Plato_idPlato` int NOT NULL,
  `cantidad` int NOT NULL DEFAULT '1',
  `precio_unitario` decimal(10,2) NOT NULL,
  `Observaciones` text COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`idDetalle_Pedido`),
  KEY `Plato_idPlato` (`Plato_idPlato`),
  KEY `idx_detalle_pedido` (`Pedido_idPedido`),
  CONSTRAINT `detalle_pedido_ibfk_1` FOREIGN KEY (`Pedido_idPedido`) REFERENCES `pedido` (`idPedido`) ON DELETE CASCADE,
  CONSTRAINT `detalle_pedido_ibfk_2` FOREIGN KEY (`Plato_idPlato`) REFERENCES `plato` (`idPlato`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `detalle_receta`
--

DROP TABLE IF EXISTS `detalle_receta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_receta` (
  `idDetalle_Receta` int NOT NULL AUTO_INCREMENT,
  `Receta_idReceta` int NOT NULL,
  `Insumo_idInsumo` int NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  PRIMARY KEY (`idDetalle_Receta`),
  KEY `Receta_idReceta` (`Receta_idReceta`),
  KEY `Insumo_idInsumo` (`Insumo_idInsumo`),
  CONSTRAINT `detalle_receta_ibfk_1` FOREIGN KEY (`Receta_idReceta`) REFERENCES `receta` (`idReceta`) ON DELETE CASCADE,
  CONSTRAINT `detalle_receta_ibfk_2` FOREIGN KEY (`Insumo_idInsumo`) REFERENCES `insumo` (`idInsumo`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `direccion`
--

DROP TABLE IF EXISTS `direccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `direccion` (
  `idDireccion` int NOT NULL AUTO_INCREMENT,
  `Usuario_idUsuario` int NOT NULL,
  `ciudad` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `calle` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `barrio` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`idDireccion`),
  KEY `Usuario_idUsuario` (`Usuario_idUsuario`),
  CONSTRAINT `direccion_ibfk_1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estado_pedido`
--

DROP TABLE IF EXISTS `estado_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estado_pedido` (
  `idEstado_Pedido` int NOT NULL AUTO_INCREMENT,
  `nombre_estado` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`idEstado_Pedido`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `insumo`
--

DROP TABLE IF EXISTS `insumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insumo` (
  `idInsumo` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `unidad_medida` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`idInsumo`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inventario`
--

DROP TABLE IF EXISTS `inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario` (
  `idInventario` int NOT NULL AUTO_INCREMENT,
  `Insumo_idInsumo` int NOT NULL,
  `stock_actual` int NOT NULL DEFAULT '0',
  `stock_minimo` int NOT NULL DEFAULT '5',
  `Administrador_id_administrador` int NOT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idInventario`),
  KEY `Administrador_id_administrador` (`Administrador_id_administrador`),
  KEY `idx_inventario_insumo` (`Insumo_idInsumo`),
  CONSTRAINT `inventario_ibfk_1` FOREIGN KEY (`Insumo_idInsumo`) REFERENCES `insumo` (`idInsumo`) ON DELETE CASCADE,
  CONSTRAINT `inventario_ibfk_2` FOREIGN KEY (`Administrador_id_administrador`) REFERENCES `administrador` (`id_administrador`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mesa`
--

DROP TABLE IF EXISTS `mesa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mesa` (
  `idMesa` int NOT NULL AUTO_INCREMENT,
  `capacidad` int NOT NULL,
  `numero_mesa` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Mesero_id_mesero` int NOT NULL,
  PRIMARY KEY (`idMesa`),
  UNIQUE KEY `numero_mesa` (`numero_mesa`),
  KEY `Mesero_id_mesero` (`Mesero_id_mesero`),
  CONSTRAINT `mesa_ibfk_1` FOREIGN KEY (`Mesero_id_mesero`) REFERENCES `mesero` (`id_mesero`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mesero`
--

DROP TABLE IF EXISTS `mesero`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mesero` (
  `id_mesero` int NOT NULL AUTO_INCREMENT,
  `Usuario_idUsuario` int NOT NULL,
  `zona_asignada` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_mesero`),
  KEY `Usuario_idUsuario` (`Usuario_idUsuario`),
  CONSTRAINT `mesero_ibfk_1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `metodopago`
--

DROP TABLE IF EXISTS `metodopago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metodopago` (
  `idMetodo_Pago` int NOT NULL AUTO_INCREMENT,
  `metodo` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`idMetodo_Pago`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `modalidadpedido`
--

DROP TABLE IF EXISTS `modalidadpedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `modalidadpedido` (
  `id_modalidad` int NOT NULL,
  `nombreModalidad` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_modalidad`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `idPedido` int NOT NULL AUTO_INCREMENT,
  `fecha_hora` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tiempo_preparacion` int NOT NULL COMMENT 'Tiempo en minutos',
  `hora_entrega` datetime NOT NULL,
  `Mesero_id_mesero` int NOT NULL,
  `Mesa_idMesa` int DEFAULT NULL,
  `modalidadPedido_id_modalidad` int NOT NULL,
  `Estado_Pedido_idEstado_Pedido` int NOT NULL,
  `cliente_id_cliente` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`idPedido`),
  KEY `Mesa_idMesa` (`Mesa_idMesa`),
  KEY `modalidadPedido_id_modalidad` (`modalidadPedido_id_modalidad`),
  KEY `idx_pedido_estado` (`Estado_Pedido_idEstado_Pedido`),
  KEY `idx_pedido_mesero` (`Mesero_id_mesero`),
  KEY `fk_pedido_cliente1_idx` (`cliente_id_cliente`),
  CONSTRAINT `fk_pedido_cliente1` FOREIGN KEY (`cliente_id_cliente`) REFERENCES `cliente` (`id_cliente`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`Mesero_id_mesero`) REFERENCES `mesero` (`id_mesero`),
  CONSTRAINT `pedido_ibfk_2` FOREIGN KEY (`Mesa_idMesa`) REFERENCES `mesa` (`idMesa`) ON DELETE SET NULL,
  CONSTRAINT `pedido_ibfk_4` FOREIGN KEY (`modalidadPedido_id_modalidad`) REFERENCES `modalidadpedido` (`id_modalidad`),
  CONSTRAINT `pedido_ibfk_5` FOREIGN KEY (`Estado_Pedido_idEstado_Pedido`) REFERENCES `estado_pedido` (`idEstado_Pedido`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `plato`
--

DROP TABLE IF EXISTS `plato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plato` (
  `idPlato` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `precio` decimal(10,2) NOT NULL DEFAULT '0.00',
  `disponible` tinyint(1) NOT NULL DEFAULT '1',
  `Tipo_Plato_idTipo_Plato` int NOT NULL,
  PRIMARY KEY (`idPlato`),
  KEY `Tipo_Plato_idTipo_Plato` (`Tipo_Plato_idTipo_Plato`),
  CONSTRAINT `plato_ibfk_1` FOREIGN KEY (`Tipo_Plato_idTipo_Plato`) REFERENCES `tipo_plato` (`idTipo_Plato`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `receta`
--

DROP TABLE IF EXISTS `receta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receta` (
  `idReceta` int NOT NULL AUTO_INCREMENT,
  `Plato_idPlato` int NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`idReceta`),
  KEY `idx_receta_plato` (`Plato_idPlato`),
  CONSTRAINT `receta_ibfk_1` FOREIGN KEY (`Plato_idPlato`) REFERENCES `plato` (`idPlato`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `telefono`
--

DROP TABLE IF EXISTS `telefono`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `telefono` (
  `idTelefono` int NOT NULL AUTO_INCREMENT,
  `Usuario_idUsuario` int NOT NULL,
  `telefono` char(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `operador` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`idTelefono`),
  UNIQUE KEY `uq_telefono` (`telefono`),
  KEY `Usuario_idUsuario` (`Usuario_idUsuario`),
  CONSTRAINT `telefono_ibfk_1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_plato`
--

DROP TABLE IF EXISTS `tipo_plato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_plato` (
  `idTipo_Plato` int NOT NULL AUTO_INCREMENT,
  `nombre_tipo` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`idTipo_Plato`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `idUsuario` int NOT NULL AUTO_INCREMENT,
  `primerNombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `segundoNombre` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `primerApellido` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `segundoApellido` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_salt` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idUsuario`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_usuario_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `venta`
--

DROP TABLE IF EXISTS `venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta` (
  `idventa` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `total` decimal(12,2) NOT NULL DEFAULT '0.00',
  `Pedido_idPedido` int NOT NULL,
  `Metodo_Pago_idMetodo_Pago` int NOT NULL,
  `Cajero_id_cajero` int NOT NULL,
  PRIMARY KEY (`idventa`),
  KEY `Pedido_idPedido` (`Pedido_idPedido`),
  KEY `Metodo_Pago_idMetodo_Pago` (`Metodo_Pago_idMetodo_Pago`),
  KEY `Cajero_id_cajero` (`Cajero_id_cajero`),
  KEY `idx_venta_fecha` (`fecha`),
  CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`Pedido_idPedido`) REFERENCES `pedido` (`idPedido`),
  CONSTRAINT `venta_ibfk_2` FOREIGN KEY (`Metodo_Pago_idMetodo_Pago`) REFERENCES `metodopago` (`idMetodo_Pago`),
  CONSTRAINT `venta_ibfk_3` FOREIGN KEY (`Cajero_id_cajero`) REFERENCES `cajero` (`id_cajero`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-17  7:17:08
