-- seed.sql
-- Datos de ejemplo para Sabor Caleno SGO
USE sabor_caleno_sgo;

-- =============================================
-- CATALOGOS BASICOS
-- =============================================
-- Modalidades de pedido
INSERT INTO
    modalidadPedido (nombreModalidad, descripcion)
VALUES
    (
        'En Mesa',
        'Pedido para consumir en el restaurante'
    ),
    ('Para Llevar', 'Pedido para llevar'),
    ('Domicilio', 'Pedido a domicilio');

-- Estados de pedido
INSERT INTO
    Estado_Pedido (nombre_estado)
VALUES
    ('Pendiente'),
    ('En Preparacion'),
    ('Listo'),
    ('Entregado'),
    ('Cancelado');

-- Tipos de plato
INSERT INTO
    Tipo_Plato (nombre_tipo)
VALUES
    ('Entrada'),
    ('Plato Principal'),
    ('Postre'),
    ('Bebida'),
    ('Guarnicion');

-- Metodos de pago
INSERT INTO
    MetodoPago (metodo)
VALUES
    ('Efectivo'),
    ('Tarjeta Credito'),
    ('Tarjeta Debito'),
    ('Transferencia'),
    ('QR');

-- =============================================
-- USUARIOS
-- =============================================
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
    );

-- =============================================
-- ROLES DE USUARIOS
-- =============================================
-- Administrador (usuario 1)
INSERT INTO
    Administrador (Usuario_idUsuario, nivel_acceso)
VALUES
    (1, 'Total');

-- Cajero (usuario 2)
INSERT INTO
    Cajero (Usuario_idUsuario, caja_asignada)
VALUES
    (2, 'Caja 1');

-- Cocinero (usuario 3)
INSERT INTO
    Cocinero (Usuario_idUsuario, especialidad, turno)
VALUES
    (3, 'Carnes', 'Mañana'),
    (4, 'Postres', 'Tarde');

-- Mesero (usuario 5)
INSERT INTO
    Mesero (Usuario_idUsuario, zona_asignada)
VALUES
    (5, 'Zona Norte');

-- Cliente (usuario 6)
INSERT INTO
    Cliente (
        id_cliente,
        Usuario_idUsuario,
        nivelCliente,
        estadoMembresia
    )
VALUES
    ('CLI-001', 6, 'Oro', 'Activa');

-- =============================================
-- DIRECCIONES Y TELEFONOS
-- =============================================
INSERT INTO
    Direccion (Usuario_idUsuario, ciudad, calle, barrio)
VALUES
    (6, 'Cali', 'Calle 10 # 5-20', 'San Fernando');

INSERT INTO
    Telefono (Usuario_idUsuario, telefono, operador)
VALUES
    (6, '+573001234567', 'Claro');

-- =============================================
-- MESAS
-- =============================================
INSERT INTO
    Mesa (capacidad, numero_mesa, Mesero_id_mesero)
VALUES
    (2, 'Mesa 1', 1),
    (4, 'Mesa 2', 1),
    (6, 'Mesa 3', 1),
    (8, 'Mesa 4', 1);

-- =============================================
-- PLATOS
-- =============================================
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
    );

-- =============================================
-- INSUMOS
-- =============================================
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

-- =============================================
-- INVENTARIO
-- =============================================
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

-- =============================================
-- RECETAS
-- =============================================
-- Receta para Bandeja Paisa (idPlato = 1)
INSERT INTO
    Receta (Plato_idPlato, descripcion)
VALUES
    (1, 'Receta tradicional bandeja paisa');

INSERT INTO
    Detalle_Receta (Receta_idReceta, Insumo_idInsumo, cantidad)
VALUES
    (1, 1, 0.5), -- Arroz
    (1, 2, 0.5), -- Frijoles
    (1, 3, 0.3), -- Carne Molida
    (1, 4, 0.2), -- Chicharron
    (1, 5, 1), -- Huevo
    (1, 6, 1), -- Platano
    (1, 7, 1);

-- Arepa
-- =============================================
-- PEDIDOS
-- =============================================
INSERT INTO
    Pedido (
        fecha_hora,
        Mesero_id_mesero,
        Mesa_idMesa,
        Cliente_id_cliente,
        modalidadPedido_id_modalidad,
        Estado_Pedido_idEstado_Pedido
    )
VALUES
    (NOW (), 1, 1, 'CLI-001', 1, 2);

-- Detalle del pedido
INSERT INTO
    Detalle_Pedido (
        Pedido_idPedido,
        Plato_idPlato,
        cantidad,
        precio_unitario,
        Observaciones
    )
VALUES
    (1, 1, 2, 25000, 'Sin chicharron por favor'),
    (1, 4, 2, 6000, 'Con hielo');

-- =============================================
-- VENTAS
-- =============================================
INSERT INTO
    Venta (
        fecha,
        total,
        Pedido_idPedido,
        Metodo_Pago_idMetodo_Pago,
        Cajero_id_cajero
    )
VALUES
    (NOW (), 62000, 1, 1, 1);