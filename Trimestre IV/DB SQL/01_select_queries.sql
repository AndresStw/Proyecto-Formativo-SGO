-- Nombre: 01_select_queries.sql "Por etapas "
-- Autor: @AndresStw - Kevin L..
-- Fecha: 2026-08-20
-- Descripción: Consultas SELECT de solo lectura para análisis de experiencia de cliente. NO modificar datos.
-- Uso: Ejecutar en entorno de solo lectura / exportar resultados.


#1
-- Consulta: resumen de pedidos por usuario 
SELECT
    u.id,
    u.nombre,
    COUNT(o.id) AS total_pedidos,
    SUM(o.total) AS total_gastado
FROM
    usuarios u
    LEFT JOIN ordenes o ON o.usuario_id = u.id
GROUP BY
    u.id,
    u.nombre
ORDER BY
    total_pedidos DESC;
    -- Sin validar aun