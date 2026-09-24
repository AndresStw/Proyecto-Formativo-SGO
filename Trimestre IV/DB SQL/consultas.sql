-- consulta 1
-- total vendido por método de pago
select mp.metodo as metodo_pago, count(v.idventa) as num_ventas, sum(v.total) as total_recaudado
from venta v
inner join metodopago mp 
on v.metodo_pago_idmetodo_pago = mp.idmetodo_pago
inner join pedido p      
on v.pedido_idpedido = p.idpedido
inner join estado_pedido ep 
on p.estado_pedido_idestado_pedido = ep.idestado_pedido
group by mp.metodo
order by total_recaudado desc;
-- - -- - - -- - -- - - -- - -- - -- --- -- - - - -- - - ---- -- - -
-- consulta 2
-- platos más vendidos
select pl.idplato,pl.nombre as plato,tp.nombre_tipo as tipo,sum(dp.cantidad) as unidades_vendidas,
sum(dp.cantidad * dp.precio_unitario) as ingresos_totales
from detalle_pedido dp
inner join plato pl       
on dp.plato_idplato = pl.idplato
inner join tipo_plato tp  
on pl.tipo_plato_idtipo_plato = tp.idtipo_plato
inner join pedido p      
on dp.pedido_idpedido = p.idpedido
group by pl.idplato, pl.nombre, tp.nombre_tipo
order by unidades_vendidas desc;
-- - -- - - -- - -- - - -- - -- - -- --- -- - - - -- - - ---- -- - -
-- consulta 3
-- insumos con su inventario y administrador responsable
select i.idinsumo, i.nombre as insumo, i.unidad_medida, inv.stock_actual, inv.stock_minimo, 
concat(u.primernombre, ' ', u.primerapellido) as administrador,
case 
when inv.stock_actual <= inv.stock_minimo then 'reponer'
else 'ok'
end as estado_stock
from inventario inv
inner join insumo i        
on inv.insumo_idinsumo = i.idinsumo
inner join administrador a 
on inv.administrador_id_administrador = a.id_administrador
inner join usuario u       
on a.usuario_idusuario = u.idusuario
order by estado_stock desc, inv.stock_actual asc;
-- - -- - - -- - -- - - -- - -- - -- --- -- - - - -- - - ---- -- - -
-- consulta 4
-- clientes y sus direcciones/teléfonos
select c.id_cliente, concat(u.primernombre, ' ', u.primerapellido) as cliente, c.nivelcliente, c.estadomembresia, d.ciudad, d.calle,
t.telefono
from cliente c
inner join usuario u   
on c.usuario_idusuario = u.idusuario
left join direccion d  
on d.usuario_idusuario = u.idusuario
left join telefono t   
on t.usuario_idusuario = u.idusuario
order by c.id_cliente;

-- - -- - - -- - -- - - -- - -- - -- --- -- - - - -- - - ---- -- - -
-- consulta 5
-- insumos por debajo del stock mínimo
select i.nombre, inv.stock_actual, inv.stock_minimo, (inv.stock_minimo - inv.stock_actual) as deficit
from inventario inv
inner join insumo i 
on i.idinsumo = inv.insumo_idinsumo
where inv.stock_actual <= inv.stock_minimo
order by deficit desc;

-- Consulta 6

-- conocer cuánto ha comprado cada cliente, cuántas compras ha realizado y cuál ha sido su gasto promedio, discriminando el método de pago.
SELECT CONCAT(u.primerNombre, ' ', COALESCE( u.segundoNombre,''),' ', u.primerApellido, ' ', 
		COALESCE( u.segundoApellido, '')) AS nombreCliente,
		COUNT(p.Cliente_id_cliente) AS cantidadCompras, mp.metodo,
        SUM(v.total) AS totalGastado,
		AVG(v.total) AS promedio
        FROM usuario u INNER JOIN cliente c
        ON u.idUsuario = c.Usuario_idUsuario
        INNER JOIN pedido p
        ON c.id_cliente = p.Cliente_id_cliente
        INNER JOIN venta v
        ON v.Pedido_idPedido= p.idPedido
        INNER JOIN metodopago mp
		ON mp.idMetodo_Pago = v.Metodo_Pago_idMetodo_Pago
        GROUP BY u.idusuario, mp.metodo;
        
        
-- Consulta 7

-- Identificar qué platos tienen mayor demanda y cuánto dinero generan.
SELECT
    tp.nombre_tipo AS categoria,
    pl.nombre AS plato,
    COUNT(DISTINCT p.idPedido) AS pedidos_realizados,
    SUM(dp.cantidad) AS unidades_vendidas,
    SUM(dp.cantidad * dp.precio_unitario) AS ingresos_generados,
    AVG(dp.precio_unitario) AS precio_promedio,
    CASE
        WHEN SUM(dp.cantidad) >= 50 THEN 'Alta demanda'
        WHEN SUM(dp.cantidad) >= 20 THEN 'Demanda media'
        ELSE 'Baja demanda'
    END AS nivel_demanda
FROM detalle_pedido dp
INNER JOIN plato pl ON dp.Plato_idPlato = pl.idPlato
INNER JOIN tipo_plato tp ON pl.Tipo_Plato_idTipo_Plato = tp.idTipo_Plato
INNER JOIN pedido p ON dp.Pedido_idPedido = p.idPedido
INNER JOIN estado_pedido ep ON p.Estado_Pedido_idEstado_Pedido = ep.idEstado_Pedido
WHERE p.fecha_hora >= '2026-01-01'
  AND ep.nombre_estado IN ('Entregado', 'Completado')
GROUP BY pl.idPlato, pl.nombre, tp.nombre_tipo
HAVING SUM(dp.cantidad) >= 10
ORDER BY unidades_vendidas DESC;


-- Consulta 8
-- Cliente con 3 pedidos  o mas y su total
	SELECT CONCAT(u.primerNombre, ' ', COALESCE( u.segundoNombre,''),' ', u.primerApellido, ' ', 
		COALESCE( u.segundoApellido, '')) AS nombreCliente, COUNT(p.idPedido) AS cantidad_pedidos,
    SUM(v.total) AS total_gastado, MAX(v.fecha) AS ultima_compra
FROM cliente c INNER JOIN usuario u ON c.Usuario_idUsuario = u.idUsuario
INNER JOIN pedido p ON c.id_cliente = p.Cliente_id_cliente
INNER JOIN venta v ON p.idPedido = v.Pedido_idPedido
GROUP BY c.id_cliente, u.primerNombre, u.segundoNombre, u.primerApellido
HAVING COUNT(p.idPedido) >= 3
ORDER BY cantidad_pedidos DESC;
        
        
-- Consulta 9
-- Identificar el estado de los insumos para verificar los que estan pronto a agotarse o que se llegaron agotar.
SELECT
    i.nombre AS Insumo, i.unidad_medida, inv.stock_actual,inv.stock_minimo,
    CASE
        WHEN inv.stock_actual = 0 THEN 'AGOTADO'
        WHEN inv.stock_actual < inv.stock_minimo THEN 'CRITICO'
        ELSE 'NORMAL'
    END AS estado_stock,

    COUNT(ai.idAlerta) AS cantidad_alertas, MAX(ai.fecha) AS ultima_alerta, CONCAT(u.primerNombre, ' ', u.primerApellido) AS administrador

FROM inventario inv INNER JOIN insumo i ON inv.Insumo_idInsumo = i.idInsumo
	LEFT JOIN alerta_inventario ai ON i.idInsumo = ai.Insumo_idInsumo
INNER JOIN administrador a ON inv.Administrador_id_administrador = a.id_administrador
INNER JOIN usuario u ON a.Usuario_idUsuario = u.idUsuario

GROUP BY i.idInsumo, i.nombre, i.unidad_medida, inv.stock_actual, inv.stock_minimo, u.primerNombre, u.primerApellido

ORDER BY inv.stock_actual ASC;


-- Consulta 10

-- Saber cuantos pedidos se han hecho segun la modalidadPedido
SELECT
    mp.nombreModalidad AS modalidad,
    COUNT(p.idPedido) AS cantidad_pedidos,
    SUM(v.total) AS total_ventas,
    AVG(v.total) AS promedio_venta
FROM pedido p
INNER JOIN venta v
    ON p.idPedido = v.Pedido_idPedido
INNER JOIN modalidadpedido mp
    ON p.modalidadPedido_id_modalidad = mp.id_modalidad
INNER JOIN cliente c
    ON p.Cliente_id_cliente = c.id_cliente
GROUP BY mp.nombreModalidad
ORDER BY total_ventas DESC;
-- - -- - - -- - -- - - -- - -- - -- --- -- - - - -- - - ---- -- - -
-- - -- - - -- - -- - - -- - -- - -- --- -- - - - -- - - ---- -- - -

