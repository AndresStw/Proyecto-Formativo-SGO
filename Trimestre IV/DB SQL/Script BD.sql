CREATE DATABASE  IF NOT EXISTS `sabor_caleno_sgo` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `sabor_caleno_sgo`;
-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: sabor_caleno_sgo
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

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

--
-- Table structure for table `administrador`
--

DROP TABLE IF EXISTS `administrador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administrador` (
  `id_administrador` int(11) NOT NULL AUTO_INCREMENT,
  `Usuario_idUsuario` int(11) NOT NULL,
  `nivel_acceso` varchar(45) NOT NULL DEFAULT 'Basico',
  PRIMARY KEY (`id_administrador`),
  KEY `Usuario_idUsuario` (`Usuario_idUsuario`),
  CONSTRAINT `administrador_ibfk_1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrador`
--

LOCK TABLES `administrador` WRITE;
/*!40000 ALTER TABLE `administrador` DISABLE KEYS */;
INSERT INTO `administrador` VALUES (1,1,'Total');
/*!40000 ALTER TABLE `administrador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alerta_inventario`
--

DROP TABLE IF EXISTS `alerta_inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alerta_inventario` (
  `idAlerta` int(11) NOT NULL AUTO_INCREMENT,
  `Insumo_idInsumo` int(11) NOT NULL,
  `stock_actual` int(11) NOT NULL,
  `mensaje` varchar(255) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`idAlerta`),
  KEY `alerta_inventario_ibfk_1` (`Insumo_idInsumo`),
  CONSTRAINT `alerta_inventario_ibfk_1` FOREIGN KEY (`Insumo_idInsumo`) REFERENCES `insumo` (`idInsumo`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alerta_inventario`
--

LOCK TABLES `alerta_inventario` WRITE;
/*!40000 ALTER TABLE `alerta_inventario` DISABLE KEYS */;
/*!40000 ALTER TABLE `alerta_inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auditoria_usuario`
--

DROP TABLE IF EXISTS `auditoria_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auditoria_usuario` (
  `idAuditoria` int(11) NOT NULL AUTO_INCREMENT,
  `Usuario_idUsuario` int(11) NOT NULL,
  `accion` varchar(45) NOT NULL,
  `detalle` varchar(255) DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`idAuditoria`),
  KEY `auditoria_usuario_ibfk_1` (`Usuario_idUsuario`),
  CONSTRAINT `auditoria_usuario_ibfk_1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auditoria_usuario`
--

LOCK TABLES `auditoria_usuario` WRITE;
/*!40000 ALTER TABLE `auditoria_usuario` DISABLE KEYS */;
/*!40000 ALTER TABLE `auditoria_usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cajero`
--

DROP TABLE IF EXISTS `cajero`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cajero` (
  `id_cajero` int(11) NOT NULL AUTO_INCREMENT,
  `Usuario_idUsuario` int(11) NOT NULL,
  `caja_asignada` varchar(45) NOT NULL,
  PRIMARY KEY (`id_cajero`),
  KEY `Usuario_idUsuario` (`Usuario_idUsuario`),
  CONSTRAINT `cajero_ibfk_1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cajero`
--

LOCK TABLES `cajero` WRITE;
/*!40000 ALTER TABLE `cajero` DISABLE KEYS */;
INSERT INTO `cajero` VALUES (1,2,'Caja 1');
/*!40000 ALTER TABLE `cajero` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `id_cliente` varchar(45) NOT NULL,
  `Usuario_idUsuario` int(11) NOT NULL,
  `nivelCliente` varchar(45) NOT NULL DEFAULT 'Estandar',
  `estadoMembresia` varchar(45) NOT NULL DEFAULT 'Activa',
  PRIMARY KEY (`id_cliente`),
  KEY `Usuario_idUsuario` (`Usuario_idUsuario`),
  CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES ('CLI-001',6,'Oro','Activa'),('CLI-002',7,'Plata','Activa'),('CLI-003',8,'Estandar','Activa'),('CLI-004',9,'Oro','Activa'),('CLI-005',10,'Plata','Activa'),('CLI-006',11,'Estandar','Activa'),('CLI-007',12,'Oro','Activa'),('CLI-008',13,'Plata','Activa'),('CLI-009',14,'Estandar','Inactiva'),('CLI-010',15,'Oro','Activa');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cocinero`
--

DROP TABLE IF EXISTS `cocinero`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cocinero` (
  `id_cocinero` int(11) NOT NULL AUTO_INCREMENT,
  `Usuario_idUsuario` int(11) NOT NULL,
  `especialidad` varchar(45) NOT NULL,
  `turno` varchar(45) NOT NULL,
  PRIMARY KEY (`id_cocinero`),
  KEY `Usuario_idUsuario` (`Usuario_idUsuario`),
  CONSTRAINT `cocinero_ibfk_1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cocinero`
--

LOCK TABLES `cocinero` WRITE;
/*!40000 ALTER TABLE `cocinero` DISABLE KEYS */;
INSERT INTO `cocinero` VALUES (1,3,'Carnes','Mañana'),(2,4,'Postres','Tarde');
/*!40000 ALTER TABLE `cocinero` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_pedido`
--

DROP TABLE IF EXISTS `detalle_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_pedido` (
  `idDetalle_Pedido` int(11) NOT NULL AUTO_INCREMENT,
  `Pedido_idPedido` int(11) NOT NULL,
  `Plato_idPlato` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL DEFAULT 1,
  `precio_unitario` decimal(10,2) NOT NULL,
  `Observaciones` text DEFAULT 'N/A',
  PRIMARY KEY (`idDetalle_Pedido`),
  KEY `Plato_idPlato` (`Plato_idPlato`),
  KEY `idx_detalle_pedido` (`Pedido_idPedido`),
  CONSTRAINT `detalle_pedido_ibfk_1` FOREIGN KEY (`Pedido_idPedido`) REFERENCES `pedido` (`idPedido`) ON DELETE CASCADE,
  CONSTRAINT `detalle_pedido_ibfk_2` FOREIGN KEY (`Plato_idPlato`) REFERENCES `plato` (`idPlato`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_pedido`
--

LOCK TABLES `detalle_pedido` WRITE;
/*!40000 ALTER TABLE `detalle_pedido` DISABLE KEYS */;
INSERT INTO `detalle_pedido` VALUES (1,1,1,2,25000.00,'Sin chicharron'),(2,1,4,2,6000.00,'Con hielo'),(3,2,2,1,22000.00,'Sin yuca'),(4,2,5,2,10000.00,NULL),(5,2,8,2,7000.00,NULL),(6,3,7,2,35000.00,'Termino medio'),(7,3,3,3,8000.00,NULL),(8,3,9,1,9000.00,NULL),(9,4,6,1,32000.00,NULL),(10,4,10,1,28000.00,NULL),(11,4,4,2,6000.00,NULL),(12,5,3,4,8000.00,'Queso extra'),(13,5,4,2,6000.00,NULL),(14,6,6,2,32000.00,NULL),(15,6,7,1,35000.00,NULL),(16,6,8,3,7000.00,'Sin hielo'),(17,7,1,1,25000.00,NULL),(18,7,2,1,22000.00,NULL),(19,7,5,2,10000.00,NULL),(20,8,10,2,28000.00,NULL),(21,8,3,2,8000.00,NULL),(22,8,4,3,6000.00,NULL),(23,9,7,1,35000.00,NULL),(24,9,6,1,32000.00,NULL),(25,9,9,2,9000.00,NULL),(26,10,1,2,25000.00,NULL),(27,10,10,1,28000.00,NULL),(28,10,8,2,7000.00,NULL),(29,11,2,2,22000.00,NULL),(30,11,3,2,8000.00,NULL),(31,11,4,2,6000.00,NULL),(32,12,6,1,32000.00,NULL),(33,12,7,2,35000.00,NULL),(34,12,5,3,10000.00,NULL),(35,13,1,1,25000.00,NULL),(36,13,4,1,6000.00,NULL),(37,14,10,1,28000.00,NULL),(38,14,8,2,7000.00,NULL),(39,15,2,1,22000.00,NULL),(40,15,9,2,9000.00,NULL),(41,15,4,1,6000.00,NULL);
/*!40000 ALTER TABLE `detalle_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_receta`
--

DROP TABLE IF EXISTS `detalle_receta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_receta` (
  `idDetalle_Receta` int(11) NOT NULL AUTO_INCREMENT,
  `Receta_idReceta` int(11) NOT NULL,
  `Insumo_idInsumo` int(11) NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  PRIMARY KEY (`idDetalle_Receta`),
  KEY `Receta_idReceta` (`Receta_idReceta`),
  KEY `Insumo_idInsumo` (`Insumo_idInsumo`),
  CONSTRAINT `detalle_receta_ibfk_1` FOREIGN KEY (`Receta_idReceta`) REFERENCES `receta` (`idReceta`) ON DELETE CASCADE,
  CONSTRAINT `detalle_receta_ibfk_2` FOREIGN KEY (`Insumo_idInsumo`) REFERENCES `insumo` (`idInsumo`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_receta`
--

LOCK TABLES `detalle_receta` WRITE;
/*!40000 ALTER TABLE `detalle_receta` DISABLE KEYS */;
INSERT INTO `detalle_receta` VALUES (1,1,1,0.50),(2,1,2,0.50),(3,1,3,0.30),(4,1,4,0.20),(5,1,5,1.00),(6,1,6,1.00),(7,1,7,1.00);
/*!40000 ALTER TABLE `detalle_receta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `direccion`
--

DROP TABLE IF EXISTS `direccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `direccion` (
  `idDireccion` int(11) NOT NULL AUTO_INCREMENT,
  `Usuario_idUsuario` int(11) NOT NULL,
  `ciudad` varchar(45) NOT NULL,
  `calle` varchar(45) NOT NULL,
  `barrio` varchar(45) NOT NULL,
  PRIMARY KEY (`idDireccion`),
  KEY `Usuario_idUsuario` (`Usuario_idUsuario`),
  CONSTRAINT `direccion_ibfk_1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `direccion`
--

LOCK TABLES `direccion` WRITE;
/*!40000 ALTER TABLE `direccion` DISABLE KEYS */;
INSERT INTO `direccion` VALUES (1,6,'Cali','Calle 10 # 5-20','San Fernando'),(2,7,'Cali','Carrera 25 # 10-30','El Prado'),(3,8,'Cali','Avenida 6 # 15-45','Granada'),(4,9,'Cali','Calle 44 # 8-12','San Antonio'),(5,10,'Cali','Carrera 15 # 30-25','Ciudad Jardín'),(6,11,'Cali','Calle 32 # 20-15','El Ingenio'),(7,12,'Cali','Avenida 3 # 12-08','Santa Monica'),(8,13,'Cali','Carrera 8 # 25-30','Los Andes'),(9,14,'Cali','Calle 70 # 5-15','El Limonar'),(10,15,'Cali','Carrera 20 # 40-35','Vipasa');
/*!40000 ALTER TABLE `direccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estado_pedido`
--

DROP TABLE IF EXISTS `estado_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estado_pedido` (
  `idEstado_Pedido` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_estado` varchar(45) NOT NULL,
  PRIMARY KEY (`idEstado_Pedido`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estado_pedido`
--

LOCK TABLES `estado_pedido` WRITE;
/*!40000 ALTER TABLE `estado_pedido` DISABLE KEYS */;
INSERT INTO `estado_pedido` VALUES (1,'Pendiente'),(2,'En Preparacion'),(3,'Listo'),(4,'Entregado'),(5,'Cancelado');
/*!40000 ALTER TABLE `estado_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `insumo`
--

DROP TABLE IF EXISTS `insumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insumo` (
  `idInsumo` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `unidad_medida` varchar(45) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`idInsumo`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insumo`
--

LOCK TABLES `insumo` WRITE;
/*!40000 ALTER TABLE `insumo` DISABLE KEYS */;
INSERT INTO `insumo` VALUES (1,'Arroz','kg',4000.00),(2,'Frijoles','kg',5000.00),(3,'Carne Molida','kg',15000.00),(4,'Chicharron','kg',18000.00),(5,'Huevo','unidad',800.00),(6,'Platano','unidad',500.00),(7,'Arepa','unidad',1500.00),(8,'Queso Costeno','kg',12000.00),(9,'Gallina','kg',14000.00),(10,'Yuca','kg',3000.00),(11,'Limon','kg',4000.00),(12,'Hierbabuena','kg',6000.00),(13,'Leche','litro',4000.00),(14,'Azucar','kg',3000.00);
/*!40000 ALTER TABLE `insumo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario`
--

DROP TABLE IF EXISTS `inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario` (
  `idInventario` int(11) NOT NULL AUTO_INCREMENT,
  `Insumo_idInsumo` int(11) NOT NULL,
  `stock_actual` int(11) NOT NULL DEFAULT 0,
  `stock_minimo` int(11) NOT NULL DEFAULT 5,
  `Administrador_id_administrador` int(11) NOT NULL,
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`idInventario`),
  KEY `Administrador_id_administrador` (`Administrador_id_administrador`),
  KEY `idx_inventario_insumo` (`Insumo_idInsumo`),
  CONSTRAINT `inventario_ibfk_1` FOREIGN KEY (`Insumo_idInsumo`) REFERENCES `insumo` (`idInsumo`) ON DELETE CASCADE,
  CONSTRAINT `inventario_ibfk_2` FOREIGN KEY (`Administrador_id_administrador`) REFERENCES `administrador` (`id_administrador`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario`
--

LOCK TABLES `inventario` WRITE;
/*!40000 ALTER TABLE `inventario` DISABLE KEYS */;
INSERT INTO `inventario` VALUES (1,1,50,10,1,'2026-09-16 20:56:25'),(2,2,30,8,1,'2026-09-16 20:56:25'),(3,3,20,5,1,'2026-09-16 20:56:25'),(4,4,15,3,1,'2026-09-16 20:56:25'),(5,5,100,20,1,'2026-09-16 20:56:25'),(6,6,80,15,1,'2026-09-16 20:56:25'),(7,7,60,10,1,'2026-09-16 20:56:25'),(8,8,25,5,1,'2026-09-16 20:56:25'),(9,9,10,2,1,'2026-09-16 20:56:25'),(10,10,40,10,1,'2026-09-16 20:56:25');
/*!40000 ALTER TABLE `inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mesa`
--

DROP TABLE IF EXISTS `mesa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mesa` (
  `idMesa` int(11) NOT NULL AUTO_INCREMENT,
  `capacidad` int(11) NOT NULL,
  `numero_mesa` varchar(10) NOT NULL,
  `Mesero_id_mesero` int(11) NOT NULL,
  PRIMARY KEY (`idMesa`),
  UNIQUE KEY `numero_mesa` (`numero_mesa`),
  KEY `Mesero_id_mesero` (`Mesero_id_mesero`),
  CONSTRAINT `mesa_ibfk_1` FOREIGN KEY (`Mesero_id_mesero`) REFERENCES `mesero` (`id_mesero`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mesa`
--

LOCK TABLES `mesa` WRITE;
/*!40000 ALTER TABLE `mesa` DISABLE KEYS */;
INSERT INTO `mesa` VALUES (1,2,'Mesa 1',1),(2,4,'Mesa 2',1),(3,6,'Mesa 3',1),(4,8,'Mesa 4',1);
/*!40000 ALTER TABLE `mesa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mesero`
--

DROP TABLE IF EXISTS `mesero`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mesero` (
  `id_mesero` int(11) NOT NULL AUTO_INCREMENT,
  `Usuario_idUsuario` int(11) NOT NULL,
  `zona_asignada` varchar(45) NOT NULL,
  PRIMARY KEY (`id_mesero`),
  KEY `Usuario_idUsuario` (`Usuario_idUsuario`),
  CONSTRAINT `mesero_ibfk_1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mesero`
--

LOCK TABLES `mesero` WRITE;
/*!40000 ALTER TABLE `mesero` DISABLE KEYS */;
INSERT INTO `mesero` VALUES (1,5,'Zona Norte');
/*!40000 ALTER TABLE `mesero` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metodopago`
--

DROP TABLE IF EXISTS `metodopago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metodopago` (
  `idMetodo_Pago` int(11) NOT NULL AUTO_INCREMENT,
  `metodo` varchar(45) NOT NULL,
  PRIMARY KEY (`idMetodo_Pago`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metodopago`
--

LOCK TABLES `metodopago` WRITE;
/*!40000 ALTER TABLE `metodopago` DISABLE KEYS */;
INSERT INTO `metodopago` VALUES (1,'Efectivo'),(2,'Tarjeta Credito'),(3,'Tarjeta Debito'),(4,'Transferencia'),(5,'QR');
/*!40000 ALTER TABLE `metodopago` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `modalidadpedido`
--

DROP TABLE IF EXISTS `modalidadpedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `modalidadpedido` (
  `id_modalidad` int(11) NOT NULL AUTO_INCREMENT,
  `nombreModalidad` varchar(45) NOT NULL,
  `descripcion` text DEFAULT 'N/A',
  PRIMARY KEY (`id_modalidad`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modalidadpedido`
--

LOCK TABLES `modalidadpedido` WRITE;
/*!40000 ALTER TABLE `modalidadpedido` DISABLE KEYS */;
INSERT INTO `modalidadpedido` VALUES (1,'En Mesa','Pedido para consumir en el restaurante'),(2,'Para Llevar','Pedido para llevar'),(3,'Domicilio','Pedido a domicilio');
/*!40000 ALTER TABLE `modalidadpedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `idPedido` int(11) NOT NULL AUTO_INCREMENT,
  `fecha_hora` datetime NOT NULL DEFAULT current_timestamp(),
  `tiempo_preparacion` int(11) DEFAULT NULL COMMENT 'Tiempo en minutos',
  `hora_entrega` datetime DEFAULT NULL,
  `Mesero_id_mesero` int(11) NOT NULL,
  `Mesa_idMesa` int(11) DEFAULT NULL,
  `Cliente_id_cliente` varchar(45) NOT NULL,
  `modalidadPedido_id_modalidad` int(11) NOT NULL,
  `Estado_Pedido_idEstado_Pedido` int(11) NOT NULL,
  PRIMARY KEY (`idPedido`),
  KEY `Mesa_idMesa` (`Mesa_idMesa`),
  KEY `modalidadPedido_id_modalidad` (`modalidadPedido_id_modalidad`),
  KEY `idx_pedido_cliente` (`Cliente_id_cliente`),
  KEY `idx_pedido_estado` (`Estado_Pedido_idEstado_Pedido`),
  KEY `idx_pedido_mesero` (`Mesero_id_mesero`),
  KEY `fk_pedido_cliente1_idx` (`Cliente_id_cliente`),
  CONSTRAINT `fk_pedido_cliente1` FOREIGN KEY (`cliente_id_cliente`) REFERENCES `cliente` (`id_cliente`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`Mesero_id_mesero`) REFERENCES `mesero` (`id_mesero`),
  CONSTRAINT `pedido_ibfk_2` FOREIGN KEY (`Mesa_idMesa`) REFERENCES `mesa` (`idMesa`) ON DELETE SET NULL,
  CONSTRAINT `pedido_ibfk_4` FOREIGN KEY (`modalidadPedido_id_modalidad`) REFERENCES `modalidadpedido` (`id_modalidad`),
  CONSTRAINT `pedido_ibfk_5` FOREIGN KEY (`Estado_Pedido_idEstado_Pedido`) REFERENCES `estado_pedido` (`idEstado_Pedido`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES (1,'2026-09-16 14:23:48',25,'2026-09-16 14:48:48',1,1,'CLI-001',1,4),(2,'2026-09-16 13:23:48',30,'2026-09-16 13:53:48',1,2,'CLI-002',1,4),(3,'2026-09-16 12:23:48',45,'2026-09-16 13:08:48',1,NULL,'CLI-003',3,4),(4,'2026-09-16 11:23:48',15,'2026-09-16 11:38:48',1,3,'CLI-004',1,4),(5,'2026-09-16 10:23:48',20,'2026-09-16 10:43:48',1,NULL,'CLI-005',2,4),(6,'2026-09-16 09:23:48',55,'2026-09-16 10:18:48',1,4,'CLI-006',1,4),(7,'2026-09-16 08:23:48',35,'2026-09-16 08:58:48',1,1,'CLI-007',1,4),(8,'2026-09-16 07:23:48',40,'2026-09-16 08:03:48',1,NULL,'CLI-008',3,4),(9,'2026-09-16 06:23:48',10,'2026-09-16 06:33:48',1,2,'CLI-009',1,4),(10,'2026-09-16 05:23:48',50,'2026-09-16 06:13:48',1,3,'CLI-010',1,4),(11,'2026-09-16 04:23:48',28,'2026-09-16 04:51:48',1,NULL,'CLI-001',2,4),(12,'2026-09-16 03:23:48',32,'2026-09-16 03:55:48',1,4,'CLI-002',1,4),(13,'2026-09-16 15:53:48',NULL,NULL,1,1,'CLI-003',1,2),(14,'2026-09-16 14:25:20',25,'2026-09-16 14:50:20',1,1,'CLI-001',1,4),(15,'2026-09-16 13:25:20',30,'2026-09-16 13:55:20',1,2,'CLI-002',1,4),(16,'2026-09-16 12:25:20',45,'2026-09-16 13:10:20',1,NULL,'CLI-003',3,4),(17,'2026-09-16 11:25:20',15,'2026-09-16 11:40:20',1,3,'CLI-004',1,4),(18,'2026-09-16 10:25:20',20,'2026-09-16 10:45:20',1,NULL,'CLI-005',2,4),(19,'2026-09-16 09:25:20',55,'2026-09-16 10:20:20',1,4,'CLI-006',1,4),(20,'2026-09-16 08:25:20',35,'2026-09-16 09:00:20',1,1,'CLI-007',1,4),(21,'2026-09-16 07:25:20',40,'2026-09-16 08:05:20',1,NULL,'CLI-008',3,4),(22,'2026-09-16 06:25:20',10,'2026-09-16 06:35:20',1,2,'CLI-009',1,4),(23,'2026-09-16 05:25:20',50,'2026-09-16 06:15:20',1,3,'CLI-010',1,4),(24,'2026-09-16 04:25:20',28,'2026-09-16 04:53:20',1,NULL,'CLI-001',2,4),(25,'2026-09-16 03:25:20',32,'2026-09-16 03:57:20',1,4,'CLI-002',1,4),(26,'2026-09-16 15:55:20',NULL,NULL,1,1,'CLI-003',1,2),(27,'2026-09-16 16:25:20',NULL,NULL,1,2,'CLI-004',1,1),(28,'2026-09-16 02:25:20',42,'2026-09-16 03:07:20',1,NULL,'CLI-005',3,4);
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plato`
--

DROP TABLE IF EXISTS `plato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plato` (
  `idPlato` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL DEFAULT 0.00,
  `disponible` tinyint(1) DEFAULT 1,
  `Tipo_Plato_idTipo_Plato` int(11) NOT NULL,
  PRIMARY KEY (`idPlato`),
  KEY `Tipo_Plato_idTipo_Plato` (`Tipo_Plato_idTipo_Plato`),
  CONSTRAINT `plato_ibfk_1` FOREIGN KEY (`Tipo_Plato_idTipo_Plato`) REFERENCES `tipo_plato` (`idTipo_Plato`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plato`
--

LOCK TABLES `plato` WRITE;
/*!40000 ALTER TABLE `plato` DISABLE KEYS */;
INSERT INTO `plato` VALUES (1,'Bandeja Paisa','Arroz, frijoles, carne molida, chicharron, huevo, platano, arepa',25000.00,1,2),(2,'Sancocho de Gallina','Sopa tradicional con gallina, yuca, platano, papa',22000.00,1,2),(3,'Arepa con Queso','Arepa de maiz blanco con queso costeno',8000.00,1,1),(4,'Limonada','Limonada natural con hierbabuena',6000.00,1,4),(5,'Tres Leches','Postre de tres leches con merengue',10000.00,1,3),(6,'Cazuela de Mariscos','Sopa de mariscos con arroz y patacones',32000.00,1,2),(7,'Churrasco','Carne de res a la parrilla con papas y ensalada',35000.00,1,2),(8,'Jugo de Lulo','Jugo natural de lulo',7000.00,1,4),(9,'Flan de Caramelo','Flan casero con caramelo',9000.00,1,3),(10,'Pescado Frito','Pescado frito con arroz y ensalada',28000.00,1,2);
/*!40000 ALTER TABLE `plato` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receta`
--

DROP TABLE IF EXISTS `receta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receta` (
  `idReceta` int(11) NOT NULL AUTO_INCREMENT,
  `Plato_idPlato` int(11) NOT NULL,
  `descripcion` text DEFAULT NULL,
  PRIMARY KEY (`idReceta`),
  KEY `idx_receta_plato` (`Plato_idPlato`),
  CONSTRAINT `receta_ibfk_1` FOREIGN KEY (`Plato_idPlato`) REFERENCES `plato` (`idPlato`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receta`
--

LOCK TABLES `receta` WRITE;
/*!40000 ALTER TABLE `receta` DISABLE KEYS */;
INSERT INTO `receta` VALUES (1,1,'Receta tradicional bandeja paisa');
/*!40000 ALTER TABLE `receta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `telefono`
--

DROP TABLE IF EXISTS `telefono`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `telefono` (
  `idTelefono` int(11) NOT NULL AUTO_INCREMENT,
  `Usuario_idUsuario` int(11) NOT NULL,
  `telefono` char(15) NOT NULL,
  `operador` varchar(45) NOT NULL,
  PRIMARY KEY (`idTelefono`),
  UNIQUE KEY `uq_telefono` (`telefono`),
  KEY `Usuario_idUsuario` (`Usuario_idUsuario`),
  CONSTRAINT `telefono_ibfk_1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `telefono`
--

LOCK TABLES `telefono` WRITE;
/*!40000 ALTER TABLE `telefono` DISABLE KEYS */;
INSERT INTO `telefono` VALUES (1,6,'+573001234567','Claro'),(2,7,'+573102345678','Movistar'),(3,8,'+573203456789','Claro'),(4,9,'+573304567890','Tigo'),(5,10,'+573405678901','Movistar'),(6,11,'+573506789012','Claro'),(7,12,'+573607890123','Tigo'),(8,13,'+573708901234','Movistar'),(9,14,'+573809012345','Claro'),(10,15,'+573901234567','Tigo');
/*!40000 ALTER TABLE `telefono` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_plato`
--

DROP TABLE IF EXISTS `tipo_plato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_plato` (
  `idTipo_Plato` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_tipo` varchar(45) NOT NULL,
  PRIMARY KEY (`idTipo_Plato`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_plato`
--

LOCK TABLES `tipo_plato` WRITE;
/*!40000 ALTER TABLE `tipo_plato` DISABLE KEYS */;
INSERT INTO `tipo_plato` VALUES (1,'Entrada'),(2,'Plato Principal'),(3,'Postre'),(4,'Bebida'),(5,'Guarnicion');
/*!40000 ALTER TABLE `tipo_plato` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `idUsuario` int(11) NOT NULL AUTO_INCREMENT,
  `primerNombre` varchar(100) NOT NULL,
  `segundoNombre` varchar(100) DEFAULT NULL,
  `primerApellido` varchar(100) NOT NULL,
  `segundoApellido` varchar(500) DEFAULT NULL,
  `email` varchar(150) NOT NULL,
  `password_hash` varchar(500) NOT NULL,
  `password_salt` varchar(500) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`idUsuario`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_usuario_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'Juan','Carlos','Perez','Gomez','juan.perez@restaurante.com','$2y$12$ExampleHash',NULL,'2026-09-16 20:56:25'),(2,'Maria','Luisa','Rodriguez','Martinez','maria.r@restaurante.com','$2y$12$ExampleHash',NULL,'2026-09-16 20:56:25'),(3,'Carlos','Andres','Lopez','Diaz','carlos.l@restaurante.com','$2y$12$ExampleHash',NULL,'2026-09-16 20:56:25'),(4,'Ana','Maria','Torres','Garcia','ana.t@restaurante.com','$2y$12$ExampleHash',NULL,'2026-09-16 20:56:25'),(5,'Pedro',NULL,'Ramirez','Cruz','pedro.r@restaurante.com','$2y$12$ExampleHash',NULL,'2026-09-16 20:56:25'),(6,'Laura','Fernanda','Sanchez','Ortiz','laura.s@restaurante.com','$2y$12$ExampleHash',NULL,'2026-09-16 20:56:25'),(7,'Miguel','Angel','Gonzalez','Ruiz','miguel.g@restaurante.com','$2y$12$ExampleHash',NULL,'2026-09-16 20:56:25'),(8,'Sofia',NULL,'Martinez','Lopez','sofia.m@restaurante.com','$2y$12$ExampleHash',NULL,'2026-09-16 20:56:25'),(9,'David','Alberto','Ramirez','Castro','david.r@restaurante.com','$2y$12$ExampleHash',NULL,'2026-09-16 20:56:25'),(10,'Valentina','Isabel','Ortiz','Mora','valentina.o@restaurante.com','$2y$12$ExampleHash',NULL,'2026-09-16 20:56:25'),(11,'Andres','Felipe','Mora','Sanchez','andres.m@restaurante.com','$2y$12$ExampleHash',NULL,'2026-09-16 20:56:25'),(12,'Camila',NULL,'Rojas','Diaz','camila.r@restaurante.com','$2y$12$ExampleHash',NULL,'2026-09-16 20:56:25'),(13,'Jorge','Enrique','Pineda','Orozco','jorge.p@restaurante.com','$2y$12$ExampleHash',NULL,'2026-09-16 20:56:25'),(14,'Natalia','Jimena','Garcia','Perez','natalia.g@restaurante.com','$2y$12$ExampleHash',NULL,'2026-09-16 20:56:25'),(15,'Luis','Fernando','Mejia','Vargas','luis.m@restaurante.com','$2y$12$ExampleHash',NULL,'2026-09-16 20:56:25');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venta`
--

DROP TABLE IF EXISTS `venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta` (
  `idventa` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL DEFAULT current_timestamp(),
  `total` decimal(12,2) NOT NULL DEFAULT 0.00,
  `Pedido_idPedido` int(11) NOT NULL,
  `Metodo_Pago_idMetodo_Pago` int(11) NOT NULL,
  `Cajero_id_cajero` int(11) NOT NULL,
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

--
-- Dumping data for table `venta`
--

LOCK TABLES `venta` WRITE;
/*!40000 ALTER TABLE `venta` DISABLE KEYS */;
INSERT INTO `venta` VALUES (1,'2026-09-16 14:25:20',62000.00,1,1,1),(2,'2026-09-16 13:25:20',56000.00,2,2,1),(3,'2026-09-16 12:25:20',103000.00,3,1,1),(4,'2026-09-16 11:25:20',72000.00,4,3,1),(5,'2026-09-16 10:25:20',44000.00,5,4,1),(6,'2026-09-16 09:25:20',120000.00,6,2,1),(7,'2026-09-16 08:25:20',67000.00,7,5,1),(8,'2026-09-16 07:25:20',90000.00,8,1,1),(9,'2026-09-16 06:25:20',85000.00,9,2,1),(10,'2026-09-16 05:25:20',92000.00,10,3,1),(11,'2026-09-16 04:25:20',72000.00,11,4,1),(12,'2026-09-16 03:25:20',132000.00,12,5,1),(13,'2026-09-16 02:25:20',46000.00,15,1,1);
/*!40000 ALTER TABLE `venta` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-16 21:13:55
