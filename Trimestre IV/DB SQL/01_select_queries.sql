-- Nombre: 01_select_queries.sql "Por etapas "
-- Autor: @AndresStw - Kevin L..
-- Fecha: 2026-08-20
-- Descripción: Consultas SELECT de solo lectura para análisis de experiencia de cliente. NO modificar datos.
-- Uso: Ejecutar en entorno de solo lectura / exportar resultados.


USE sabor_caleno_sgo; -- "Esto es indispensable para que cargue la DB ojo POR AHORA NO SE CAMBIA"


/* Consultas de todos los integrantes del proyecto */

-- 1. Lista el nombre completo (primerNombre + primerApellido) y el email de todos los usuarios que tienen segundo Nombre

SELECT
    CONCAT (primerNombre, ' ', primerApellido) AS nombre_Completo,-- AS es darle alias a el nuevo rsultado ""
    email 
FROM
    Usuario
WHERE
.3625
    segundoNombre IS NOT NULL
ORDER BY
    primerApellido;

-- 2. Muestra el nombre completo del mesero (primerNombre + primerApellido), su zona_asignada y el número de mesa que atiende.
SELECT
    CONCAT (u.primerNombre, ' ', u.primerApellido) AS Nombre_Completo,
    m.zona_asignada,
    me.numero_mesa
FROM
    Usuario u -- tabla 1
    INNER JOIN -- tabla 2
    Mesero m ON u.idUsuario = m.Usuario_idUsuario
    INNER JOIN -- tabla 3
    Mesa me ON m.id_mesero = me.Mesero_id_mesero;-- Hacer algo con los nombres , estan dificil hacer la consultas Xd

-- 4. Consulta normal — Seguimiento de pedidos (Adaptado)

SELECT
    p.idPedido,
    CONCAT (u.primerNombre, ' ', u.primerApellido) AS cliente,
    ep.nombre_estado AS estado,
    mp.nombreModalidad AS modalidad,
    m.numero_mesa,
    p.fecha_hora,
    p.tiempo_preparacion,
    p.hora_entrega
FROM
    Pedido p
    INNER JOIN Cliente c ON p.Cliente_id_cliente = c.id_cliente
    INNER JOIN Usuario u ON c.Usuario_idUsuario = u.idUsuario
    INNER JOIN modalidadPedido mp ON p.modalidadPedido_id_modalidad = mp.id_modalidad
    INNER JOIN Estado_Pedido ep ON p.Estado_Pedido_idEstado_Pedido = ep.idEstado_Pedido
    LEFT JOIN Mesa m ON p.Mesa_idMesa = m.idMesa;

-- 5. Consulta normal — Detalle de ventas y platos (Adaptado)
SELECT
    v.idventa,
    v.fecha,
    CONCAT (u.primerNombre, ' ', u.primerApellido) AS cliente,
    pl.nombre AS plato,
    dp.cantidad,
    (dp.cantidad * dp.precio_unitario) AS subtotal,
    mp.metodo AS metodo_pago,
    v.total,
    ca.caja_asignada
FROM
    Venta v
    INNER JOIN Pedido p ON v.Pedido_idPedido = p.idPedido
    INNER JOIN Cliente c ON p.Cliente_id_cliente = c.id_cliente
    INNER JOIN Usuario u ON c.Usuario_idUsuario = u.idUsuario
    INNER JOIN Detalle_Pedido dp ON p.idPedido = dp.Pedido_idPedido
    INNER JOIN Plato pl ON dp.Plato_idPlato = pl.idPlato
    INNER JOIN Cajero ca ON v.Cajero_id_cajero = ca.id_cajero
    INNER JOIN MetodoPago mp ON v.Metodo_Pago_idMetodo_Pago = mp.idMetodo_Pago;

-- 6. Subconsulta — Insumos con inventario bajo (Adaptado)
SELECT
    i.idInsumo,
    i.nombre,
    i.unidad_medida,
    inv.stock_actual,
    inv.stock_minimo
FROM
    Insumo i
    INNER JOIN Inventario inv ON i.idInsumo = inv.Insumo_idInsumo
WHERE
    inv.stock_actual < ( -- Corregir 
        SELECT
            AVG(stock_minimo)
        FROM
            Inventario
    );

-- 7. Subconsulta — Platos con precio superior al promedio (Adaptado)
SELECT
    idPlato,
    nombre,
    precio,
    descripcion
FROM
    Plato
WHERE
    precio > (
        SELECT
            AVG(precio)
        FROM
            Plato
    );

/* ------------------------CONSULTAS CON COSAS DE LA REAL LIFE-----------------*/

-- 1. Clientes, meseros y mesas por estado de pedido
-- El administrador del restaurante quiere identificar qué clientes realizaron pedidos,
-- qué mesero los atendió y en qué mesa se realizaron.
-- Además, solo le interesa revisar los pedidos que se encuentren en un determinado estado.

SELECT
    pe.Cliente_id_cliente AS ID,
    CONCAT (
        usuC.primerNombre,
        ' ',
        IFNULL (usuC.segundoNombre, ''),
        ' ',
        usuC.primerApellido,
        ' ',
        IFNULL (usuC.segundoApellido, '')
    ) AS nombreCliente,
    CONCAT (
        usuM.primerNombre,
        ' ',
        IFNULL (usuM.segundoNombre, ''),
        ' ',
        usuM.primerApellido,
        ' ',
        IFNULL (usuM.segundoApellido, '')
    ) AS nombreMesero,
    me.numero_mesa,
    ep.nombre_estado AS Estado
FROM
    Usuario usuC
    INNER JOIN Cliente cli ON usuC.idUsuario = cli.Usuario_idUsuario
    INNER JOIN Pedido pe ON cli.id_cliente = pe.Cliente_id_cliente
    INNER JOIN Mesero m ON pe.Mesero_id_mesero = m.id_mesero
    INNER JOIN Usuario usuM ON usuM.idUsuario = m.Usuario_idUsuario
    INNER JOIN Mesa me ON m.id_mesero = me.Mesero_id_mesero
    INNER JOIN Estado_Pedido ep ON pe.Estado_Pedido_idEstado_Pedido = ep.idEstado_Pedido
WHERE
    ep.nombre_estado = 'Entregado';

-- 2. Clientes frecuentes vs ocasionales
-- El administrador quiere analizar el comportamiento de los clientes según la cantidad de pedidos que han realizado.
-- Necesita conocer el nombre del cliente, cuántos pedidos ha realizado y clasificarlo mediante una categoría:
-- "Cliente frecuente" si tiene 2 o más pedidos, y "Cliente ocasional" si tiene menos de 2.
-- Solo desea visualizar los clientes que hayan realizado al menos un pedido.
SELECT
    CONCAT (
        usuC.primerNombre,
        ' ',
        IFNULL (usuC.segundoNombre, ''),
        ' ',
        usuC.primerApellido,
        ' ',
        IFNULL (usuC.segundoApellido, '')
    ) AS nombreCliente,
    COUNT(pe.idPedido) AS cantidadPedido,
    CASE
        WHEN COUNT(pe.idPedido) >= 2 THEN 'Cliente Frecuente'
        ELSE 'Cliente Ocasional'
    END AS Categoria
FROM
    Usuario usuC
    INNER JOIN Cliente c ON usuC.idUsuario = c.Usuario_idUsuario
    INNER JOIN Pedido pe ON c.id_cliente = pe.Cliente_id_cliente
GROUP BY
    c.id_cliente,
    usuC.idUsuario
HAVING
    COUNT(pe.idPedido) >= 1
ORDER BY
    cantidadPedido DESC;

-- 3. Pedidos con tiempo de preparación superior al promedio
-- El administrador quiere identificar los pedidos cuyo tiempo de preparación sea superior 
-- al promedio de tiempo de preparación de todos los pedidos.
-- Para cada pedido quiere conocer el cliente, el mesero, la mesa y el tiempo de preparación.
SELECT
    pe.idPedido,
    CONCAT (
        usuC.primerNombre,
        ' ',
        IFNULL (usuC.segundoNombre, ''),
        ' ',
        usuC.primerApellido,
        ' ',
        IFNULL (usuC.segundoApellido, '')
    ) AS nombreCliente,
    CONCAT (
        usuM.primerNombre,
        ' ',
        IFNULL (usuM.segundoNombre, ''),
        ' ',
        usuM.primerApellido,
        ' ',
        IFNULL (usuM.segundoApellido, '')
    ) AS nombreMesero,
    me.numero_mesa,
    pe.tiempo_preparacion
FROM
    Pedido pe
    INNER JOIN Cliente c ON pe.Cliente_id_cliente = c.id_cliente
    INNER JOIN Usuario usuC ON c.Usuario_idUsuario = usuC.idUsuario
    INNER JOIN Mesero m ON pe.Mesero_id_mesero = m.id_mesero
    INNER JOIN Usuario usuM ON m.Usuario_idUsuario = usuM.idUsuario
    INNER JOIN Mesa me ON pe.Mesa_idMesa = me.idMesa
WHERE
    pe.tiempo_preparacion > (
        SELECT
            AVG(tiempo_preparacion)
        FROM
            Pedido
        WHERE
            tiempo_preparacion IS NOT NULL
    )
ORDER BY
    pe.tiempo_preparacion DESC;

-- 4. Platos con precio superior al promedio y su clasificación
SELECT
    pla.nombre AS nombrePlato,
    pla.precio,
    COUNT(dp.idDetalle_Pedido) AS vecesSolicitado,
    CASE
        WHEN pla.precio > (
            SELECT
                AVG(precio)
            FROM
                Plato
        ) THEN 'Plato costoso'
        ELSE 'Plato económico'
    END AS categoria
FROM
    Plato pla
    INNER JOIN Detalle_Pedido dp ON pla.idPlato = dp.Plato_idPlato
    INNER JOIN Pedido pe ON dp.Pedido_idPedido = pe.idPedido
WHERE
    pla.precio > (
        SELECT
            AVG(precio)
        FROM
            Plato
    )
GROUP BY
    pla.idPlato,
    pla.nombre,
    pla.precio
ORDER BY
    pla.precio DESC;
    
    --  Insumos con mayor consumo 
    -- isumos con mayor desperdicio 
    -- 
    
    
    
    