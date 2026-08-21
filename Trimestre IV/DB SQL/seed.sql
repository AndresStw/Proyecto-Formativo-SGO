-- seed_completo.sql
-- Datos de ejemplo para Sabor Caleno SGO
USE sabor_caleno_sgo;

-- CATALOGOS BASICOS
INSERT INTO
    modalidadPedido (nombreModalidad, descripcion)
VALUES
    (
        'En Mesa',
        'Pedido para consumir en el restaurante'
    ),
    ('Para Llevar', 'Pedido para llevar'),
    ('Domicilio', 'Pedido a domicilio');

INSERT INTO
    Estado_Pedido (nombre_estado)
VALUES
    ('Pendiente'),
    ('En Preparacion'),
    ('Listo'),
    ('Entregado'),
    ('Cancelado');

INSERT INTO
    Tipo_Plato (nombre_tipo)
VALUES
    ('Entrada'),
    ('Plato Principal'),
    ('Postre'),
    ('Bebida'),
    ('Guarnicion');

INSERT INTO
    MetodoPago (metodo)
VALUES
    ('Efectivo'),
    ('Tarjeta Credito'),
    ('Tarjeta Debito'),
    ('Transferencia'),
    ('QR');

-- USUARIOS (15 USUARIOS)
INSERT INTO
    Usuario (
        primerNombre,
        segundoNombre,
        primerApellido,
        segundoApellido,
        email,
        password_hash
    )
VALUES
    (
        'Juan',
        'Carlos',
        'Perez',
        'Gomez',
        'juan.perez@restaurante.com',
        '$2y$12$ExampleHash'
    ),
    (
        'Maria',
        'Luisa',
        'Rodriguez',
        'Martinez',
        'maria.r@restaurante.com',
        '$2y$12$ExampleHash'
    ),
    (
        'Carlos',
        'Andres',
        'Lopez',
        'Diaz',
        'carlos.l@restaurante.com',
        '$2y$12$ExampleHash'
    ),
    (
        'Ana',
        'Maria',
        'Torres',
        'Garcia',
        'ana.t@restaurante.com',
        '$2y$12$ExampleHash'
    ),
    (
        'Pedro',
        NULL,
        'Ramirez',
        'Cruz',
        'pedro.r@restaurante.com',
        '$2y$12$ExampleHash'
    ),
    (
        'Laura',
        'Fernanda',
        'Sanchez',
        'Ortiz',
        'laura.s@restaurante.com',
        '$2y$12$ExampleHash'
    ),
    (
        'Miguel',
        'Angel',
        'Gonzalez',
        'Ruiz',
        'miguel.g@restaurante.com',
        '$2y$12$ExampleHash'
    ),
    (
        'Sofia',
        NULL,
        'Martinez',
        'Lopez',
        'sofia.m@restaurante.com',
        '$2y$12$ExampleHash'
    ),
    (
        'David',
        'Alberto',
        'Ramirez',
        'Castro',
        'david.r@restaurante.com',
        '$2y$12$ExampleHash'
    ),
    (
        'Valentina',
        'Isabel',
        'Ortiz',
        'Mora',
        'valentina.o@restaurante.com',
        '$2y$12$ExampleHash'
    ),
    (
        'Andres',
        'Felipe',
        'Mora',
        'Sanchez',
        'andres.m@restaurante.com',
        '$2y$12$ExampleHash'
    ),
    (
        'Camila',
        NULL,
        'Rojas',
        'Diaz',
        'camila.r@restaurante.com',
        '$2y$12$ExampleHash'
    ),
    (
        'Jorge',
        'Enrique',
        'Pineda',
        'Orozco',
        'jorge.p@restaurante.com',
        '$2y$12$ExampleHash'
    ),
    (
        'Natalia',
        'Jimena',
        'Garcia',
        'Perez',
        'natalia.g@restaurante.com',
        '$2y$12$ExampleHash'
    ),
    (
        'Luis',
        'Fernando',
        'Mejia',
        'Vargas',
        'luis.m@restaurante.com',
        '$2y$12$ExampleHash'
    );

-- ROLES DE USUARIOS

-- Administradores (usuario 1)
INSERT INTO
    Administrador (Usuario_idUsuario, nivel_acceso)
VALUES
    (1, 'Total');

-- Cajeros (usuario 2)
INSERT INTO
    Cajero (Usuario_idUsuario, caja_asignada)
VALUES
    (2, 'Caja 1');

-- Cocineros (usuario 3 y 4)
INSERT INTO
    Cocinero (Usuario_idUsuario, especialidad, turno)
VALUES
    (3, 'Carnes', 'Mañana'),
    (4, 'Postres', 'Tarde');

-- Meseros (usuario 5)
INSERT INTO
    Mesero (Usuario_idUsuario, zona_asignada)
VALUES
    (5, 'Zona Norte');

-- Clientes (usuarios 6 al 15)
INSERT INTO
    Cliente (
        id_cliente,
        Usuario_idUsuario,
        nivelCliente,
        estadoMembresia
    )
VALUES
    ('CLI-001', 6, 'Oro', 'Activa'),
    ('CLI-002', 7, 'Plata', 'Activa'),
    ('CLI-003', 8, 'Estandar', 'Activa'),
    ('CLI-004', 9, 'Oro', 'Activa'),
    ('CLI-005', 10, 'Plata', 'Activa'),
    ('CLI-006', 11, 'Estandar', 'Activa'),
    ('CLI-007', 12, 'Oro', 'Activa'),
    ('CLI-008', 13, 'Plata', 'Activa'),
    ('CLI-009', 14, 'Estandar', 'Inactiva'),
    ('CLI-010', 15, 'Oro', 'Activa');

-- DIRECCIONES Y TELEFONOS
INSERT INTO
    Direccion (Usuario_idUsuario, ciudad, calle, barrio)
VALUES
    (6, 'Cali', 'Calle 10 # 5-20', 'San Fernando'),
    (7, 'Cali', 'Carrera 25 # 10-30', 'El Prado'),
    (8, 'Cali', 'Avenida 6 # 15-45', 'Granada'),
    (9, 'Cali', 'Calle 44 # 8-12', 'San Antonio'),
    (10, 'Cali', 'Carrera 15 # 30-25', 'Ciudad Jardín'),
    (11, 'Cali', 'Calle 32 # 20-15', 'El Ingenio'),
    (12, 'Cali', 'Avenida 3 # 12-08', 'Santa Monica'),
    (13, 'Cali', 'Carrera 8 # 25-30', 'Los Andes'),
    (14, 'Cali', 'Calle 70 # 5-15', 'El Limonar'),
    (15, 'Cali', 'Carrera 20 # 40-35', 'Vipasa');

INSERT INTO
    Telefono (Usuario_idUsuario, telefono, operador)
VALUES
    (6, '+573001234567', 'Claro'),
    (7, '+573102345678', 'Movistar'),
    (8, '+573203456789', 'Claro'),
    (9, '+573304567890', 'Tigo'),
    (10, '+573405678901', 'Movistar'),
    (11, '+573506789012', 'Claro'),
    (12, '+573607890123', 'Tigo'),
    (13, '+573708901234', 'Movistar'),
    (14, '+573809012345', 'Claro'),
    (15, '+573901234567', 'Tigo');

-- MESAS
INSERT INTO
    Mesa (capacidad, numero_mesa, Mesero_id_mesero)
VALUES
    (2, 'Mesa 1', 1),
    (4, 'Mesa 2', 1),
    (6, 'Mesa 3', 1),
    (8, 'Mesa 4', 1);

-- PLATOS (Son 10 PLATOS)
INSERT INTO
    Plato (
        nombre,
        descripcion,
        precio,
        disponible,
        Tipo_Plato_idTipo_Plato
    )
VALUES
    (
        'Bandeja Paisa',
        'Arroz, frijoles, carne molida, chicharron, huevo, platano, arepa',
        25000,
        TRUE,
        2
    ),
    (
        'Sancocho de Gallina',
        'Sopa tradicional con gallina, yuca, platano, papa',
        22000,
        TRUE,
        2
    ),
    (
        'Arepa con Queso',
        'Arepa de maiz blanco con queso costeno',
        8000,
        TRUE,
        1
    ),
    (
        'Limonada',
        'Limonada natural con hierbabuena',
        6000,
        TRUE,
        4
    ),
    (
        'Tres Leches',
        'Postre de tres leches con merengue',
        10000,
        TRUE,
        3
    ),
    (
        'Cazuela de Mariscos',
        'Sopa de mariscos con arroz y patacones',
        32000,
        TRUE,
        2
    ),
    (
        'Churrasco',
        'Carne de res a la parrilla con papas y ensalada',
        35000,
        TRUE,
        2
    ),
    (
        'Jugo de Lulo',
        'Jugo natural de lulo',
        7000,
        TRUE,
        4
    ),
    (
        'Flan de Caramelo',
        'Flan casero con caramelo',
        9000,
        TRUE,
        3
    ),
    (
        'Pescado Frito',
        'Pescado frito con arroz y ensalada',
        28000,
        TRUE,
        2
    );

-- INSUMOS
INSERT INTO
    Insumo (nombre, unidad_medida, precio_unitario)
VALUES
    ('Arroz', 'kg', 4000),
    ('Frijoles', 'kg', 5000),
    ('Carne Molida', 'kg', 15000),
    ('Chicharron', 'kg', 18000),
    ('Huevo', 'unidad', 800),
    ('Platano', 'unidad', 500),
    ('Arepa', 'unidad', 1500),
    ('Queso Costeno', 'kg', 12000),
    ('Gallina', 'kg', 14000),
    ('Yuca', 'kg', 3000),
    ('Limon', 'kg', 4000),
    ('Hierbabuena', 'kg', 6000),
    ('Leche', 'litro', 4000),
    ('Azucar', 'kg', 3000);

INSERT INTO
    Inventario (
        Insumo_idInsumo,
        stock_actual,
        stock_minimo,
        Administrador_id_administrador
    )
VALUES
    (1, 50, 10, 1),
    (2, 30, 8, 1),
    (3, 20, 5, 1),
    (4, 15, 3, 1),
    (5, 100, 20, 1),
    (6, 80, 15, 1),
    (7, 60, 10, 1),
    (8, 25, 5, 1),
    (9, 10, 2, 1),
    (10, 40, 10, 1);

-- RECETAS
INSERT INTO
    Receta (Plato_idPlato, descripcion)
VALUES
    (1, 'Receta tradicional bandeja paisa');

INSERT INTO
    Detalle_Receta (Receta_idReceta, Insumo_idInsumo, cantidad)
VALUES
    (1, 1, 0.5),
    (1, 2, 0.5),
    (1, 3, 0.3),
    (1, 4, 0.2),
    (1, 5, 1),
    (1, 6, 1),
    (1, 7, 1);


-- PEDIDOS (15 PEDIDOS CON TIEMPOS VARIADOS)

/*Esto va aparte       PEDIDOS DE PRUEBA CON CHAT GPT */

-- Pedido 1 - Entregado (Mesa 1, CLI-001) - tiempo: 25 min
INSERT INTO
    Pedido (
        fecha_hora,
        Mesero_id_mesero,
        Mesa_idMesa,
        Cliente_id_cliente,
        modalidadPedido_id_modalidad,
        Estado_Pedido_idEstado_Pedido,
        tiempo_preparacion,
        hora_entrega
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 2 HOUR),
        1,
        1,
        'CLI-001',
        1,
        4,
        25,
        DATE_ADD (
            DATE_SUB (NOW (), INTERVAL 2 HOUR),
            INTERVAL 25 MINUTE
        )
    );

-- Pedido 2 - Entregado (Mesa 2, CLI-002) - tiempo: 30 min
INSERT INTO
    Pedido (
        fecha_hora,
        Mesero_id_mesero,
        Mesa_idMesa,
        Cliente_id_cliente,
        modalidadPedido_id_modalidad,
        Estado_Pedido_idEstado_Pedido,
        tiempo_preparacion,
        hora_entrega
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 3 HOUR),
        1,
        2,
        'CLI-002',
        1,
        4,
        30,
        DATE_ADD (
            DATE_SUB (NOW (), INTERVAL 3 HOUR),
            INTERVAL 30 MINUTE
        )
    );

-- Pedido 3 - Entregado (Domicilio, CLI-003) - tiempo: 45 min
INSERT INTO
    Pedido (
        fecha_hora,
        Mesero_id_mesero,
        Mesa_idMesa,
        Cliente_id_cliente,
        modalidadPedido_id_modalidad,
        Estado_Pedido_idEstado_Pedido,
        tiempo_preparacion,
        hora_entrega
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 4 HOUR),
        1,
        NULL,
        'CLI-003',
        3,
        4,
        45,
        DATE_ADD (
            DATE_SUB (NOW (), INTERVAL 4 HOUR),
            INTERVAL 45 MINUTE
        )
    );

-- Pedido 4 - Entregado (Mesa 3, CLI-004) - tiempo: 15 min
INSERT INTO
    Pedido (
        fecha_hora,
        Mesero_id_mesero,
        Mesa_idMesa,
        Cliente_id_cliente,
        modalidadPedido_id_modalidad,
        Estado_Pedido_idEstado_Pedido,
        tiempo_preparacion,
        hora_entrega
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 5 HOUR),
        1,
        3,
        'CLI-004',
        1,
        4,
        15,
        DATE_ADD (
            DATE_SUB (NOW (), INTERVAL 5 HOUR),
            INTERVAL 15 MINUTE
        )
    );

-- Pedido 5 - Entregado (Para Llevar, CLI-005) - tiempo: 20 min
INSERT INTO
    Pedido (
        fecha_hora,
        Mesero_id_mesero,
        Mesa_idMesa,
        Cliente_id_cliente,
        modalidadPedido_id_modalidad,
        Estado_Pedido_idEstado_Pedido,
        tiempo_preparacion,
        hora_entrega
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 6 HOUR),
        1,
        NULL,
        'CLI-005',
        2,
        4,
        20,
        DATE_ADD (
            DATE_SUB (NOW (), INTERVAL 6 HOUR),
            INTERVAL 20 MINUTE
        )
    );

-- Pedido 6 - Entregado (Mesa 4, CLI-006) - tiempo: 55 min
INSERT INTO
    Pedido (
        fecha_hora,
        Mesero_id_mesero,
        Mesa_idMesa,
        Cliente_id_cliente,
        modalidadPedido_id_modalidad,
        Estado_Pedido_idEstado_Pedido,
        tiempo_preparacion,
        hora_entrega
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 7 HOUR),
        1,
        4,
        'CLI-006',
        1,
        4,
        55,
        DATE_ADD (
            DATE_SUB (NOW (), INTERVAL 7 HOUR),
            INTERVAL 55 MINUTE
        )
    );

-- Pedido 7 - Entregado (Mesa 1, CLI-007) - tiempo: 35 min
INSERT INTO
    Pedido (
        fecha_hora,
        Mesero_id_mesero,
        Mesa_idMesa,
        Cliente_id_cliente,
        modalidadPedido_id_modalidad,
        Estado_Pedido_idEstado_Pedido,
        tiempo_preparacion,
        hora_entrega
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 8 HOUR),
        1,
        1,
        'CLI-007',
        1,
        4,
        35,
        DATE_ADD (
            DATE_SUB (NOW (), INTERVAL 8 HOUR),
            INTERVAL 35 MINUTE
        )
    );

-- Pedido 8 - Entregado (Domicilio, CLI-008) - tiempo: 40 min
INSERT INTO
    Pedido (
        fecha_hora,
        Mesero_id_mesero,
        Mesa_idMesa,
        Cliente_id_cliente,
        modalidadPedido_id_modalidad,
        Estado_Pedido_idEstado_Pedido,
        tiempo_preparacion,
        hora_entrega
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 9 HOUR),
        1,
        NULL,
        'CLI-008',
        3,
        4,
        40,
        DATE_ADD (
            DATE_SUB (NOW (), INTERVAL 9 HOUR),
            INTERVAL 40 MINUTE
        )
    );

-- Pedido 9 - Entregado (Mesa 2, CLI-009) - tiempo: 10 min
INSERT INTO
    Pedido (
        fecha_hora,
        Mesero_id_mesero,
        Mesa_idMesa,
        Cliente_id_cliente,
        modalidadPedido_id_modalidad,
        Estado_Pedido_idEstado_Pedido,
        tiempo_preparacion,
        hora_entrega
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 10 HOUR),
        1,
        2,
        'CLI-009',
        1,
        4,
        10,
        DATE_ADD (
            DATE_SUB (NOW (), INTERVAL 10 HOUR),
            INTERVAL 10 MINUTE
        )
    );

-- Pedido 10 - Entregado (Mesa 3, CLI-010) - tiempo: 50 min
INSERT INTO
    Pedido (
        fecha_hora,
        Mesero_id_mesero,
        Mesa_idMesa,
        Cliente_id_cliente,
        modalidadPedido_id_modalidad,
        Estado_Pedido_idEstado_Pedido,
        tiempo_preparacion,
        hora_entrega
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 11 HOUR),
        1,
        3,
        'CLI-010',
        1,
        4,
        50,
        DATE_ADD (
            DATE_SUB (NOW (), INTERVAL 11 HOUR),
            INTERVAL 50 MINUTE
        )
    );

-- Pedido 11 - Entregado (Para Llevar, CLI-001) - tiempo: 28 min
INSERT INTO
    Pedido (
        fecha_hora,
        Mesero_id_mesero,
        Mesa_idMesa,
        Cliente_id_cliente,
        modalidadPedido_id_modalidad,
        Estado_Pedido_idEstado_Pedido,
        tiempo_preparacion,
        hora_entrega
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 12 HOUR),
        1,
        NULL,
        'CLI-001',
        2,
        4,
        28,
        DATE_ADD (
            DATE_SUB (NOW (), INTERVAL 12 HOUR),
            INTERVAL 28 MINUTE
        )
    );

-- Pedido 12 - Entregado (Mesa 4, CLI-002) - tiempo: 32 min
INSERT INTO
    Pedido (
        fecha_hora,
        Mesero_id_mesero,
        Mesa_idMesa,
        Cliente_id_cliente,
        modalidadPedido_id_modalidad,
        Estado_Pedido_idEstado_Pedido,
        tiempo_preparacion,
        hora_entrega
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 13 HOUR),
        1,
        4,
        'CLI-002',
        1,
        4,
        32,
        DATE_ADD (
            DATE_SUB (NOW (), INTERVAL 13 HOUR),
            INTERVAL 32 MINUTE
        )
    );

-- Pedido 13 - En Preparación (Mesa 1, CLI-003) - sin tiempo aún
INSERT INTO
    Pedido (
        fecha_hora,
        Mesero_id_mesero,
        Mesa_idMesa,
        Cliente_id_cliente,
        modalidadPedido_id_modalidad,
        Estado_Pedido_idEstado_Pedido,
        tiempo_preparacion,
        hora_entrega
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 30 MINUTE),
        1,
        1,
        'CLI-003',
        1,
        2,
        NULL,
        NULL
    );

-- Pedido 14 - Pendiente (Mesa 2, CLI-004) - sin tiempo aún
INSERT INTO
    Pedido (
        fecha_hora,
        Mesero_id_mesero,
        Mesa_idMesa,
        Cliente_id_cliente,
        modalidadPedido_id_modalidad,
        Estado_Pedido_idEstado_Pedido,
        tiempo_preparacion,
        hora_entrega
    )
VALUES
    (NOW (), 1, 2, 'CLI-004', 1, 1, NULL, NULL);

-- Pedido 15 - Entregado (Domicilio, CLI-005) - tiempo: 42 min
INSERT INTO
    Pedido (
        fecha_hora,
        Mesero_id_mesero,
        Mesa_idMesa,
        Cliente_id_cliente,
        modalidadPedido_id_modalidad,
        Estado_Pedido_idEstado_Pedido,
        tiempo_preparacion,
        hora_entrega
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 14 HOUR),
        1,
        NULL,
        'CLI-005',
        3,
        4,
        42,
        DATE_ADD (
            DATE_SUB (NOW (), INTERVAL 14 HOUR),
            INTERVAL 42 MINUTE
        )
    );

-- DETALLES DE PEDIDOS

-- Pedido 1 (Bandeja Paisa x2, Limonada x2)
INSERT INTO
    Detalle_Pedido (
        Pedido_idPedido,
        Plato_idPlato,
        cantidad,
        precio_unitario,
        Observaciones
    )
VALUES
    (1, 1, 2, 25000, 'Sin chicharron'),
    (1, 4, 2, 6000, 'Con hielo');

-- Pedido 2 (Sancocho x1, Tres Leches x2, Jugo Lulo x2)
INSERT INTO
    Detalle_Pedido (
        Pedido_idPedido,
        Plato_idPlato,
        cantidad,
        precio_unitario,
        Observaciones
    )
VALUES
    (2, 2, 1, 22000, 'Sin yuca'),
    (2, 5, 2, 10000, NULL),
    (2, 8, 2, 7000, NULL);

-- Pedido 3 (Churrasco x2, Arepa x3, Flan x1)
INSERT INTO
    Detalle_Pedido (
        Pedido_idPedido,
        Plato_idPlato,
        cantidad,
        precio_unitario,
        Observaciones
    )
VALUES
    (3, 7, 2, 35000, 'Termino medio'),
    (3, 3, 3, 8000, NULL),
    (3, 9, 1, 9000, NULL);

-- Pedido 4 (Cazuela x1, Pescado x1, Limonada x2)
INSERT INTO
    Detalle_Pedido (
        Pedido_idPedido,
        Plato_idPlato,
        cantidad,
        precio_unitario,
        Observaciones
    )
VALUES
    (4, 6, 1, 32000, NULL),
    (4, 10, 1, 28000, NULL),
    (4, 4, 2, 6000, NULL);

-- Pedido 5 (Arepa x4, Limonada x2)
INSERT INTO
    Detalle_Pedido (
        Pedido_idPedido,
        Plato_idPlato,
        cantidad,
        precio_unitario,
        Observaciones
    )
VALUES
    (5, 3, 4, 8000, 'Queso extra'),
    (5, 4, 2, 6000, NULL);

-- Pedido 6 (Cazuela x2, Churrasco x1, Jugo Lulo x3)
INSERT INTO
    Detalle_Pedido (
        Pedido_idPedido,
        Plato_idPlato,
        cantidad,
        precio_unitario,
        Observaciones
    )
VALUES
    (6, 6, 2, 32000, NULL),
    (6, 7, 1, 35000, NULL),
    (6, 8, 3, 7000, 'Sin hielo');

-- Pedido 7 (Bandeja x1, Sancocho x1, Tres Leches x2)
INSERT INTO
    Detalle_Pedido (
        Pedido_idPedido,
        Plato_idPlato,
        cantidad,
        precio_unitario,
        Observaciones
    )
VALUES
    (7, 1, 1, 25000, NULL),
    (7, 2, 1, 22000, NULL),
    (7, 5, 2, 10000, NULL);

-- Pedido 8 (Pescado x2, Arepa x2, Limonada x3)
INSERT INTO
    Detalle_Pedido (
        Pedido_idPedido,
        Plato_idPlato,
        cantidad,
        precio_unitario,
        Observaciones
    )
VALUES
    (8, 10, 2, 28000, NULL),
    (8, 3, 2, 8000, NULL),
    (8, 4, 3, 6000, NULL);

-- Pedido 9 (Churrasco x1, Cazuela x1, Flan x2)
INSERT INTO
    Detalle_Pedido (
        Pedido_idPedido,
        Plato_idPlato,
        cantidad,
        precio_unitario,
        Observaciones
    )
VALUES
    (9, 7, 1, 35000, NULL),
    (9, 6, 1, 32000, NULL),
    (9, 9, 2, 9000, NULL);

-- Pedido 10 (Bandeja x2, Pescado x1, Jugo Lulo x2)
INSERT INTO
    Detalle_Pedido (
        Pedido_idPedido,
        Plato_idPlato,
        cantidad,
        precio_unitario,
        Observaciones
    )
VALUES
    (10, 1, 2, 25000, NULL),
    (10, 10, 1, 28000, NULL),
    (10, 8, 2, 7000, NULL);

-- Pedido 11 (Sancocho x2, Arepa x2, Limonada x2)
INSERT INTO
    Detalle_Pedido (
        Pedido_idPedido,
        Plato_idPlato,
        cantidad,
        precio_unitario,
        Observaciones
    )
VALUES
    (11, 2, 2, 22000, NULL),
    (11, 3, 2, 8000, NULL),
    (11, 4, 2, 6000, NULL);

-- Pedido 12 (Cazuela x1, Churrasco x2, Tres Leches x3)
INSERT INTO
    Detalle_Pedido (
        Pedido_idPedido,
        Plato_idPlato,
        cantidad,
        precio_unitario,
        Observaciones
    )
VALUES
    (12, 6, 1, 32000, NULL),
    (12, 7, 2, 35000, NULL),
    (12, 5, 3, 10000, NULL);

-- Pedido 13 (Bandeja x1, Limonada x1)
INSERT INTO
    Detalle_Pedido (
        Pedido_idPedido,
        Plato_idPlato,
        cantidad,
        precio_unitario,
        Observaciones
    )
VALUES
    (13, 1, 1, 25000, NULL),
    (13, 4, 1, 6000, NULL);

-- Pedido 14 (Pescado x1, Jugo Lulo x2)
INSERT INTO
    Detalle_Pedido (
        Pedido_idPedido,
        Plato_idPlato,
        cantidad,
        precio_unitario,
        Observaciones
    )
VALUES
    (14, 10, 1, 28000, NULL),
    (14, 8, 2, 7000, NULL);

-- Pedido 15 (Sancocho x1, Flan x2, Limonada x1)
INSERT INTO
    Detalle_Pedido (
        Pedido_idPedido,
        Plato_idPlato,
        cantidad,
        precio_unitario,
        Observaciones
    )
VALUES
    (15, 2, 1, 22000, NULL),
    (15, 9, 2, 9000, NULL),
    (15, 4, 1, 6000, NULL);

-- VENTAS (Para pedidos entregados) Pruebita 

-- Pedido 1: 2*25000 + 2*6000 = 62000
INSERT INTO
    Venta (
        fecha,
        total,
        Pedido_idPedido,
        Metodo_Pago_idMetodo_Pago,
        Cajero_id_cajero
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 2 HOUR),
        62000,
        1,
        1,
        1
    );

-- Pedido 2: 22000 + 2*10000 + 2*7000 = 56000
INSERT INTO
    Venta (
        fecha,
        total,
        Pedido_idPedido,
        Metodo_Pago_idMetodo_Pago,
        Cajero_id_cajero
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 3 HOUR),
        56000,
        2,
        2,
        1
    );

-- Pedido 3: 2*35000 + 3*8000 + 9000 = 103000
INSERT INTO
    Venta (
        fecha,
        total,
        Pedido_idPedido,
        Metodo_Pago_idMetodo_Pago,
        Cajero_id_cajero
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 4 HOUR),
        103000,
        3,
        1,
        1
    );

-- Pedido 4: 32000 + 28000 + 2*6000 = 72000
INSERT INTO
    Venta (
        fecha,
        total,
        Pedido_idPedido,
        Metodo_Pago_idMetodo_Pago,
        Cajero_id_cajero
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 5 HOUR),
        72000,
        4,
        3,
        1
    );

-- Pedido 5: 4*8000 + 2*6000 = 44000
INSERT INTO
    Venta (
        fecha,
        total,
        Pedido_idPedido,
        Metodo_Pago_idMetodo_Pago,
        Cajero_id_cajero
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 6 HOUR),
        44000,
        5,
        4,
        1
    );

-- Pedido 6: 2*32000 + 35000 + 3*7000 = 120000
INSERT INTO
    Venta (
        fecha,
        total,
        Pedido_idPedido,
        Metodo_Pago_idMetodo_Pago,
        Cajero_id_cajero
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 7 HOUR),
        120000,
        6,
        2,
        1
    );

-- Pedido 7: 25000 + 22000 + 2*10000 = 67000
INSERT INTO
    Venta (
        fecha,
        total,
        Pedido_idPedido,
        Metodo_Pago_idMetodo_Pago,
        Cajero_id_cajero
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 8 HOUR),
        67000,
        7,
        5,
        1
    );

-- Pedido 8: 2*28000 + 2*8000 + 3*6000 = 90000
INSERT INTO
    Venta (
        fecha,
        total,
        Pedido_idPedido,
        Metodo_Pago_idMetodo_Pago,
        Cajero_id_cajero
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 9 HOUR),
        90000,
        8,
        1,
        1
    );

-- Pedido 9: 35000 + 32000 + 2*9000 = 85000
INSERT INTO
    Venta (
        fecha,
        total,
        Pedido_idPedido,
        Metodo_Pago_idMetodo_Pago,
        Cajero_id_cajero
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 10 HOUR),
        85000,
        9,
        2,
        1
    );

-- Pedido 10: 2*25000 + 28000 + 2*7000 = 92000
INSERT INTO
    Venta (
        fecha,
        total,
        Pedido_idPedido,
        Metodo_Pago_idMetodo_Pago,
        Cajero_id_cajero
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 11 HOUR),
        92000,
        10,
        3,
        1
    );

-- Pedido 11: 2*22000 + 2*8000 + 2*6000 = 72000
INSERT INTO
    Venta (
        fecha,
        total,
        Pedido_idPedido,
        Metodo_Pago_idMetodo_Pago,
        Cajero_id_cajero
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 12 HOUR),
        72000,
        11,
        4,
        1
    );

-- Pedido 12: 32000 + 2*35000 + 3*10000 = 132000
INSERT INTO
    Venta (
        fecha,
        total,
        Pedido_idPedido,
        Metodo_Pago_idMetodo_Pago,
        Cajero_id_cajero
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 13 HOUR),
        132000,
        12,
        5,
        1
    );

-- Pedido 15: 22000 + 2*9000 + 6000 = 46000
INSERT INTO
    Venta (
        fecha,
        total,
        Pedido_idPedido,
        Metodo_Pago_idMetodo_Pago,
        Cajero_id_cajero
    )
VALUES
    (
        DATE_SUB (NOW (), INTERVAL 14 HOUR),
        46000,
        15,
        1,
        1
    );