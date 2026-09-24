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
from
 (select date_format(fecha, '%y-%m') as mes, sum(total) as total_ventas, count(*) as num_ventas from venta
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


-- subconsulta 8 
	-- Identificar platos que se han
    -- vendido una cantidad de unidades mayor al promedio de unidades vendidas por plato
    
    SELECT
    pl.nombre AS plato,
    tp.nombre_tipo AS tipoPlato,
    SUM(dp.cantidad) AS unidadesVendidas,
    COUNT(DISTINCT dp.Pedido_idPedido) AS cantidadPedidos
FROM plato pl
INNER JOIN tipo_plato tp
    ON pl.Tipo_Plato_idTipo_Plato = tp.idTipo_Plato
INNER JOIN detalle_pedido dp
    ON pl.idPlato = dp.Plato_idPlato
INNER JOIN pedido p
    ON dp.Pedido_idPedido = p.idPedido
GROUP BY
    pl.idPlato,
    pl.nombre,
    tp.nombre_tipo
HAVING SUM(dp.cantidad) > (
    SELECT AVG(cantidad)
    FROM detalle_pedido
)
ORDER BY unidadesVendidas DESC;

-- subconsulta 9
-- Mostrar los clientes 
-- que han realizado una cantidad de pedidos superior al promedio de pedidos
SELECT CONCAT( u.primerNombre, ' ', COALESCE(u.segundoNombre, ''), ' ',
        u.primerApellido, ' ', COALESCE(u.segundoApellido, '')) AS nombreCliente,
    c.nivelCliente, COUNT(p.idPedido) AS cantidadPedidos
FROM cliente c INNER JOIN usuario u ON c.Usuario_idUsuario = u.idUsuario
INNER JOIN pedido p ON c.id_cliente = p.Cliente_id_cliente
INNER JOIN estado_pedido ep ON p.Estado_Pedido_idEstado_Pedido = ep.idEstado_Pedido
GROUP BY c.id_cliente, nombreCliente, c.nivelCliente
HAVING COUNT(p.idPedido) > (
    SELECT AVG(cantidad)
    FROM (
        SELECT COUNT(*) AS cantidad
        FROM pedido
        GROUP BY Cliente_id_cliente
    ) AS promedio
)
ORDER BY cantidadPedidos DESC;


-- Subconsulta 10
-- Mostrar los meseros que tienen pedidos cuyo tiempo de preparación es superior al promedio general.
SELECT CONCAT( u.primerNombre, ' ', COALESCE(u.segundoNombre, ''), ' ', u.primerApellido, ' ', COALESCE(u.segundoApellido, '')
    ) AS nombreMesero, COUNT(p.idPedido) AS cantidadPedidos,
    AVG(p.tiempo_preparacion) AS promedioPreparacion
FROM mesero m
INNER JOIN usuario u
    ON m.Usuario_idUsuario = u.idUsuario
INNER JOIN pedido p
    ON m.id_mesero = p.Mesero_id_mesero
INNER JOIN estado_pedido ep
    ON p.Estado_Pedido_idEstado_Pedido = ep.idEstado_Pedido
WHERE ep.nombre_estado = 'Entregado'
GROUP BY
    m.id_mesero,
    nombreMesero
HAVING AVG(p.tiempo_preparacion) > (
    SELECT AVG(tiempo_preparacion)
    FROM pedido
    WHERE tiempo_preparacion IS NOT NULL
)
ORDER BY promedioPreparacion DESC;