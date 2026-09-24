-- TRIGGER 1 
-- Descontar inventario automáticamente al registrar un pedido
-- Cuando se vende un plato, los insumos deben bajar del inventario según la receta.
Delimiter $$
create trigger trg_descontar_inventario
after insert on detalle_pedido
for each row
begin
declare v_receta_id int;
-- aca se busca la receta asociada al plato vendido
select idReceta into v_receta_id
from receta
where Plato_idPlato = new.Plato_idPlato
limit 1;
-- aca si el plato tiene receta entonces descuenta insumos
if v_receta_id is not null then
update inventario i
join detalle_receta dr on i.Insumo_idInsumo = dr.Insumo_idInsumo
set i.stock_actual = i.stock_actual - (dr.cantidad * new.cantidad)
where dr.Receta_idReceta = v_receta_id;
end if;
end$$
delimiter ;

-- PRUEBA 
INSERT INTO detalle_pedido (Pedido_idPedido, Plato_idPlato, cantidad, precio_unitario, Observaciones)
VALUES (13, 1, 2, 25000.00, 'Prueba Trigger');
-- -- -- -- -- -- -- -- -- -- -- --- -- --- --- --- - - -- - - -- -- - 
-- Genera alerta automática cuando un insumo llega a stock mínimo o menos
-- Avisa al administrador antes de que se acaben los insumos y se detenga la cocina.
-- TRIGGER 2
delimiter $$
CREATE TRIGGER trg_alerta_stock_bajo
after update on inventario
for each row 
begin
if new.stock_actual <= new.stock_minimo and new.stock_actual <> old.stock_actual then
insert into alerta_inventario (Insumo_idInsumo, stock_actual, mensaje)
values (new.Insumo_idInsumo,new.stock_actual,
concat('Stock bajo: quedan ', new.stock_actual, ' unidades (mínimo ', new.stock_minimo, ')')
);
end if;
end$$
delimiter ;
-- PRUEBA 
UPDATE inventario SET stock_actual = 1 WHERE Insumo_idInsumo = 4;

-- -- -- -- -- -- -- -- -- -- -- --- -- --- --- --- - - -- - - -- -- - 
-- Evitar vender platos no disponibles
-- Si un plato está marcado como disponible = 0, no debe poder agregarse a un pedido.
-- TRIGGER 3
DELIMITER $$
CREATE TRIGGER trg_bloquear_plato_no_disponible
BEFORE INSERT ON detalle_pedido
FOR EACH ROW
BEGIN
    DECLARE p_disponible TINYINT;

    SELECT disponible INTO p_disponible
    FROM plato
    WHERE idPlato = NEW.Plato_idPlato;

    IF p_disponible IS NULL OR p_disponible = 0  THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: El plato no existe / No hay cantidad suficiente.';
	ELSE
	UPDATE plato SET disponible = disponible - new.cantidad where idPlato = new.plato_idPlato;
    END IF;
END$$

-- PRUEBA 

INSERT INTO detalle_pedido(Pedido_idPedido,Plato_idPlato,cantidad,precio_unitario)VALUES(24,2,2,25000); -- da
INSERT INTO detalle_pedido(Pedido_idPedido,Plato_idPlato,cantidad,precio_unitario)VALUES(24,2,1,25000); -- 0
 -- 

DROP TRIGGER trg_bloquear_plato_no_disponible;
-- PRUEBA
INSERT INTO detalle_pedido 
(Pedido_idPedido, Plato_idPlato, cantidad, precio_unitario)
VALUES 
(29, 1, 1, 25000);



-- -- -- -- -- -- -- -- -- -- -- --- -- --- --- --- - - -- - - -- -- - 
-- TRIGGER 4
-- Cada ves que se registre un nuevo usuario y ponga una contraseña en password_hash, el trigger lo reemplazaria 
-- por el hash real mas guardar un salt
DELIMITER $$
CREATE TRIGGER trg_hashear_password_usuario
BEFORE INSERT ON usuario
FOR EACH ROW
BEGIN
DECLARE v_salt VARCHAR(250);
-- Generar un salt único
    SET v_salt = UUID();
    -- Si el campo password_hash trae la clave en texto plano,
    -- reemplazarlo por el hash real + guardar el salt
    IF NEW.password_hash IS NOT NULL 
       AND NEW.password_hash <> '' 
       AND NEW.password_salt IS NULL THEN
        
        SET NEW.password_salt = v_salt;
        SET NEW.password_hash = SHA2(CONCAT(NEW.password_hash, v_salt), 256);
    END IF;
END$$
DELIMITER ;
-- PRUEBA
INSERT INTO usuario (primerNombre, primerApellido, email, password_hash)
VALUES ('Samuel', 'Clavijo', 'samuel@gmail.com', 'Samuel123');