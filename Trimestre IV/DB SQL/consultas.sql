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

#subconsulta 1
-- clientes que han gastado más que el promedio 
select  c.id_cliente, concat(u.primernombre, ' ', u.primerapellido) as cliente, sum(v.total) as total_gastado
from cliente c
inner join usuario u 
on c.usuario_idusuario = u.idusuario
inner join pedido p  
on p.cliente_id_cliente = c.id_cliente
inner join venta v   
on v.pedido_idpedido = p.idpedido
group by c.id_cliente, cliente
having sum(v.total) > (select avg(total) from venta
);
-- - -- - - -- - -- - - -- - -- - -- --- -- - - - -- - - ---- -- - -
-- subconsulta 2
-- platos cuyo precio es mayor al promedio de su tipo
select pl.idplato, pl.nombre, pl.precio, tp.nombre_tipo
from plato pl
inner join tipo_plato tp 
on pl.tipo_plato_idtipo_plato = tp.idtipo_plato
where pl.precio > (select avg(pl2.precio) from plato pl2 where pl2.tipo_plato_idtipo_plato = pl.tipo_plato_idtipo_plato)
order by tp.nombre_tipo, pl.precio desc;
-- - -- - - -- - -- - - -- - -- - -- --- -- - - - -- - - ---- -- - -
-- subconsulta 3
--  promedio de ventas por mes
select mes, total_ventas, round(total_ventas / num_ventas, 2) as promedio_por_venta
from (select date_format(fecha, '%y-%m') as mes, sum(total) as total_ventas, count(*) as num_ventas from venta
group by date_format(fecha, '%y-%m')) as resumen_mensual
order by mes desc;
-- - -- - - -- - -- - - -- - -- - -- --- -- - - - -- - - ---- -- - -
-- subconsulta 4
-- mesas que actualmente tienen un pedido pendiente
select m.numero_mesa
from mesa m
where (select 1 from pedido p inner join estado_pedido ep 
on ep.idestado_pedido = p.estado_pedido_idestado_pedido
where p.mesa_idmesa = m.idmesa and ep.nombre_estado = 'pendiente');
-- - -- - - -- - -- - - -- - -- - -- --- -- - - - -- - - ---- -- - -
-- subconsulta 5
-- encontrar el pedido más reciente de cada mesa
select p.idpedido, p.mesa_idmesa, p.fecha_hora
from pedido p
where (p.mesa_idmesa, p.fecha_hora) in (select mesa_idmesa, max(fecha_hora) from pedido
group by mesa_idmesa);


-- subconsulta 6

--  identificar los pedidos cuyo tiempo de preparación sea superior al promedio de tiempo de preparación de todos los pedidos.
-- Para cada pedido quiere conocer el cliente, el mesero, la mesa y el tiempo de preparación.

SELECT
    pe.idPedido, CONCAT(um.primerNombre, ' ', COALESCE(um.segundoNombre, ''), ' ', um.primerApellido, ' ',
        COALESCE(um.segundoApellido, '')
    ) AS nombreMesero,

    CONCAT( uc.primerNombre, ' ', COALESCE(uc.segundoNombre, ''), ' ', uc.primerApellido, ' ',
        COALESCE(uc.segundoApellido, '')
    ) AS nombreCliente,

    mesa.numero_mesa, pe.tiempo_preparacion

FROM Pedido pe INNER JOIN Cliente c 
    ON pe.Cliente_id_cliente = c.id_cliente
INNER JOIN Usuario uc 
    ON c.Usuario_idUsuario = uc.idUsuario
INNER JOIN Mesero me 
    ON pe.Mesero_id_mesero = me.id_mesero
INNER JOIN Usuario um 
    ON me.Usuario_idUsuario = um.idUsuario
INNER JOIN Mesa mesa 
    ON pe.Mesa_idMesa = mesa.idMesa
WHERE pe.tiempo_preparacion > ( SELECT AVG(tiempo_preparacion) FROM Pedido);


-- Subconsulta 7
-- detectar insumos que tienen una cantidad disponible inferior al promedio general del inventario.

SELECT i.nombre AS insumo, i.unidad_medida, inv.stock_actual, inv.stock_minimo,
    a.mensaje AS ultima_alerta, a.fecha AS fecha_alerta
FROM inventario inv INNER JOIN insumo i
    ON inv.Insumo_idInsumo = i.idInsumo
LEFT JOIN alerta_inventario a
    ON i.idInsumo = a.Insumo_idInsumo
INNER JOIN administrador adm
    ON inv.Administrador_id_administrador = adm.id_administrador
INNER JOIN usuario u
    ON adm.Usuario_idUsuario = u.idUsuario

WHERE inv.stock_actual < ( SELECT AVG(stock_actual) FROM inventario) AND inv.stock_actual <= inv.stock_minimo
ORDER BY inv.stock_actual ASC;

