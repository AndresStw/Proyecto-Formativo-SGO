-- =====================================================
-- QUERIES ÚTILES - Sabor Caleño SGO
-- =====================================================
-- Fecha: 2026-08-20
-- Descripción: Consultas comunes para el sistema
-- =====================================================

USE sabor_caleno_sgo;

-- =====================================================
-- 1. CONSULTAS DE ÓRDENES
-- =====================================================

-- Ver todas las órdenes con información del cliente y usuario
SELECT 
    o.id_orden,
    o.numero_orden,
    o.fecha_orden,
    CONCAT(c.nombre, ' ', COALESCE(c.apellido, '')) AS cliente,
    CONCAT(u.nombre, ' ', u.apellido) AS usuario,
    o.total,
    o.estado,
    o.tipo_pedido
FROM ordenes o
LEFT JOIN clientes c ON o.id_cliente = c.id_cliente
LEFT JOIN usuarios u ON o.id_usuario = u.id_usuario
ORDER BY o.fecha_orden DESC;

-- Órdenes pendientes
SELECT 
    numero_orden,
    fecha_orden,
    CONCAT(c.nombre, ' ', COALESCE(c.apellido, '')) AS cliente,
    total,
    tipo_pedido
FROM ordenes o
LEFT JOIN clientes c ON o.id_cliente = c.id_cliente
WHERE o.estado = 'pendiente'
ORDER BY fecha_orden ASC;

-- Órdenes en preparación
SELECT 
    numero_orden,
    CONCAT(u.nombre, ' ', u.apellido) AS cocinero,
    DATE_FORMAT(fecha_orden, '%Y-%m-%d %H:%i') AS fecha_orden,
    total
FROM ordenes o
LEFT JOIN usuarios u ON o.id_usuario = u.id_usuario
WHERE o.estado = 'en_preparacion'
ORDER BY fecha_orden ASC;

-- Ventas por día
SELECT 
    DATE(fecha_orden) AS fecha,
    COUNT(id_orden) AS total_ordenes,
    SUM(total) AS ingresos_totales,
    AVG(total) AS promedio_orden
FROM ordenes
WHERE estado IN ('completada', 'entregada')
GROUP BY DATE(fecha_orden)
ORDER BY fecha DESC;

-- =====================================================
-- 2. CONSULTAS DE PRODUCTOS Y VENTAS
-- =====================================================

-- Productos más vendidos
SELECT 
    p.id_producto,
    p.nombre,
    c.nombre AS categoria,
    SUM(do.cantidad) AS cantidad_vendida,
    SUM(do.subtotal) AS total_vendido
FROM detalles_orden do
JOIN productos p ON do.id_producto = p.id_producto
JOIN categorias c ON p.id_categoria = c.id_categoria
GROUP BY p.id_producto, p.nombre, c.nombre
ORDER BY cantidad_vendida DESC
LIMIT 10;

-- Productos por categoría con precios
SELECT 
    c.nombre AS categoria,
    p.nombre AS producto,
    p.precio_unitario,
    p.cantidad_stock,
    p.estado
FROM productos p
JOIN categorias c ON p.id_categoria = c.id_categoria
ORDER BY c.nombre, p.nombre;

-- Productos con bajo inventario (por debajo del mínimo)
SELECT 
    p.nombre,
    c.nombre AS categoria,
    i.cantidad_actual,
    i.cantidad_minima,
    i.proveedor,
    (i.cantidad_minima - i.cantidad_actual) AS cantidad_a_pedir
FROM inventario i
JOIN productos p ON i.id_producto = p.id_producto
JOIN categorias c ON p.id_categoria = c.id_categoria
WHERE i.cantidad_actual <= i.cantidad_minima
ORDER BY i.cantidad_actual ASC;

-- =====================================================
-- 3. CONSULTAS DE CLIENTES
-- =====================================================

-- Clientes más frecuentes
SELECT 
    c.id_cliente,
    CONCAT(c.nombre, ' ', COALESCE(c.apellido, '')) AS cliente,
    c.tipo_cliente,
    COUNT(o.id_orden) AS cantidad_ordenes,
    SUM(o.total) AS total_gastado,
    c.fecha_registro
FROM clientes c
LEFT JOIN ordenes o ON c.id_cliente = o.id_cliente
GROUP BY c.id_cliente, c.nombre, c.apellido, c.tipo_cliente, c.fecha_registro
ORDER BY total_gastado DESC;

-- Clientes VIP
SELECT 
    CONCAT(nombre, ' ', COALESCE(apellido, '')) AS cliente,
    email,
    telefono,
    total_compras,
    fecha_registro
FROM clientes
WHERE tipo_cliente = 'vip'
ORDER BY total_compras DESC;

-- Clientes registrados en el mes actual
SELECT 
    CONCAT(nombre, ' ', COALESCE(apellido, '')) AS cliente,
    email,
    telefono,
    tipo_cliente,
    fecha_registro
FROM clientes
WHERE MONTH(fecha_registro) = MONTH(CURDATE())
  AND YEAR(fecha_registro) = YEAR(CURDATE())
ORDER BY fecha_registro DESC;

-- =====================================================
-- 4. CONSULTAS DE PERSONAL (USUARIOS)
-- =====================================================

-- Empleados activos por rol
SELECT 
    rol,
    COUNT(id_usuario) AS cantidad,
    GROUP_CONCAT(CONCAT(nombre, ' ', apellido) SEPARATOR ', ') AS empleados
FROM usuarios
WHERE estado = 'activo'
GROUP BY rol;

-- Rendimiento de empleados (órdenes procesadas)
SELECT 
    u.id_usuario,
    CONCAT(u.nombre, ' ', u.apellido) AS empleado,
    u.rol,
    COUNT(o.id_orden) AS ordenes_procesadas,
    SUM(o.total) AS total_venta,
    AVG(o.total) AS promedio_orden
FROM usuarios u
LEFT JOIN ordenes o ON u.id_usuario = o.id_usuario
WHERE u.estado = 'activo'
GROUP BY u.id_usuario, u.nombre, u.apellido, u.rol
ORDER BY ordenes_procesadas DESC;

-- =====================================================
-- 5. CONSULTAS DE INVENTARIO
-- =====================================================

-- Estado general del inventario
SELECT 
    p.nombre AS producto,
    c.nombre AS categoria,
    i.cantidad_actual,
    i.cantidad_minima,
    i.cantidad_maxima,
    CASE 
        WHEN i.cantidad_actual <= i.cantidad_minima THEN 'CRÍTICO'
        WHEN i.cantidad_actual < (i.cantidad_minima * 1.5) THEN 'BAJO'
        ELSE 'NORMAL'
    END AS estado_stock,
    i.unidad_medida,
    i.proveedor
FROM inventario i
JOIN productos p ON i.id_producto = p.id_producto
JOIN categorias c ON p.id_categoria = c.id_categoria
ORDER BY i.cantidad_actual ASC;

-- Valor total del inventario
SELECT 
    SUM(i.cantidad_actual * i.costo_promedio) AS valor_total_inventario,
    COUNT(DISTINCT i.id_producto) AS total_productos
FROM inventario i;

-- Movimientos de inventario por producto
SELECT 
    p.nombre,
    SUM(CASE WHEN m.tipo_movimiento = 'entrada' THEN m.cantidad ELSE 0 END) AS entradas,
    SUM(CASE WHEN m.tipo_movimiento = 'salida' THEN m.cantidad ELSE 0 END) AS salidas,
    SUM(CASE WHEN m.tipo_movimiento = 'ajuste' THEN m.cantidad ELSE 0 END) AS ajustes
FROM movimientos_inventario m
JOIN productos p ON m.id_producto = p.id_producto
GROUP BY p.nombre
ORDER BY p.nombre;

-- =====================================================
-- 6. CONSULTAS DE ANÁLISIS Y REPORTES
-- =====================================================

-- Resumen de ingresos por tipo de pedido
SELECT 
    tipo_pedido,
    COUNT(id_orden) AS cantidad_ordenes,
    SUM(total) AS ingresos_totales,
    AVG(total) AS promedio_orden,
    MAX(total) AS orden_maxima,
    MIN(total) AS orden_minima
FROM ordenes
WHERE estado IN ('completada', 'entregada')
GROUP BY tipo_pedido;

-- Ingresos por método de pago
SELECT 
    metodo_pago,
    COUNT(id_orden) AS cantidad_ordenes,
    SUM(total) AS total_ingresos
FROM ordenes
WHERE estado IN ('completada', 'entregada')
GROUP BY metodo_pago
ORDER BY total_ingresos DESC;

-- Desempeño de categorías de productos
SELECT 
    c.nombre AS categoria,
    COUNT(do.id_detalle) AS items_vendidos,
    SUM(do.cantidad) AS cantidad_total,
    SUM(do.subtotal) AS ingresos_categoria,
    AVG(p.precio_unitario) AS precio_promedio
FROM categorias c
JOIN productos p ON c.id_categoria = p.id_categoria
LEFT JOIN detalles_orden do ON p.id_producto = do.id_producto
GROUP BY c.nombre
ORDER BY ingresos_categoria DESC;

-- Resumen de estado de órdenes
SELECT 
    estado,
    COUNT(id_orden) AS cantidad,
    SUM(total) AS total
FROM ordenes
GROUP BY estado
ORDER BY cantidad DESC;

-- =====================================================
-- 7. CONSULTAS DE AUDITORÍA
-- =====================================================

-- Últimos cambios en el sistema
SELECT 
    CONCAT(u.nombre, ' ', u.apellido) AS usuario,
    u.rol,
    ra.accion,
    ra.tabla_afectada,
    ra.detalles,
    ra.fecha_acceso,
    ra.ip_acceso
FROM registro_acceso ra
JOIN usuarios u ON ra.id_usuario = u.id_usuario
ORDER BY ra.fecha_acceso DESC
LIMIT 20;

-- Actividad por usuario
SELECT 
    u.id_usuario,
    CONCAT(u.nombre, ' ', u.apellido) AS usuario,
    COUNT(ra.id_registro) AS total_acciones,
    MAX(ra.fecha_acceso) AS ultimo_acceso
FROM usuarios u
LEFT JOIN registro_acceso ra ON u.id_usuario = ra.id_usuario
WHERE u.estado = 'activo'
GROUP BY u.id_usuario, u.nombre, u.apellido
ORDER BY total_acciones DESC;

-- =====================================================
-- FIN DE QUERIES ÚTILES
-- =====================================================
