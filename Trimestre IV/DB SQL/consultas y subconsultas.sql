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