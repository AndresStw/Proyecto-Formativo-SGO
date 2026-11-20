# Task Breakdown — Sabor Caleño Backend

**Current status:**

- ✅ Local MySQL (XAMPP) connected.
- ✅ Alembic configured.
- ✅ Database is empty. We need to build the ORM models!

---

## ⚠️ IMPORTANT: How to create a Model (ORM)

Each Epic must create its own files inside `app/models/`.
**Do not run Alembic directly on `Backend`.** Work on your feature branch, create the models, test the import, and open a PR. The Lead will run the final migration.

Example workflow for your task:

1. Create the `.py` files in `app/models/`.
2. Update `app/models/__init__.py` to import your new models.
3. Run `python -c "import app.models; print('OK')"` to ensure no syntax errors.
4. Push and open a PR.

---

## 🔴 EP-01 — Authentication & Accounts (BLOCKING) - ✅ COMPLETED

**Assignee:** Lead
**Framework:** Laravel 11 + Laravel Sanctum

_Architecture Note: Implemented using "Single Table Inheritance" (a single `Usuario` table with a `rol` column) instead of separate tables for Cliente, Mesero, etc. This simplifies queries and maintenance._

**Model Tasks (Laravel - `app/Models/`):**

- [x] `Usuario.php` (idUsuario, names, email, password_hash, telefono, direccion, rol, estado) implementing `HasApiTokens`.

**Endpoint Tasks (`routes/api.php`):**

- [x] `POST /api/register` (Creates user with 'cliente' role by default and returns Token).
- [x] `POST /api/login` (Validates Bcrypt credentials and returns Token).
- [x] `GET /api/me` (Protected route to view profile).
- [x] `PUT /api/me` (Protected route to update profile).
- [x] `POST /api/logout` (Destroys the current token).
- [x] `POST /api/forgot-password` (Sends a simulated reset link to the log file).
- [x] `POST /api/reset-password` (Resets the password using the token).

**Middlewares:**

- [x] `auth:sanctum` (Replaces the old Python `@require_auth` decorator, protects private routes).
- [x] `AdminMiddleware` (Created and registered to protect admin-only routes).

---

## 🟡 EP-02 — Catalog & Menu (Public)

**Assignee:** [Teammate 1]

**Model Tasks (Create in `app/models/`):**

- [ ] `plato.py` (id, name, price, image, calories)
- [ ] `catalogos.py` (`Tipo_Plato`)

**Endpoint Tasks:**

- [ ] `GET /productos` and `GET /productos/<id>`
- [ ] Create `scripts/seed_platos.py` to populate the DB with the 21 dishes from `menuData.js`.

---

## 🟠 EP-03 — Cart & Orders

**Assignee:** [Teammate 2]

**Model Tasks (Create in `app/models/`):**

- [ ] `pedido.py` (`Pedido`, `Detalle_Pedido`)
- [ ] `catalogos.py` (`modalidadPedido`, `Estado_Pedido`) - _Coordinate with Teammate 1 on `catalogos.py`_

**Endpoint Tasks:**

- [ ] `POST /pedidos` (create order)
- [ ] `GET /pedidos` (user history)
- [ ] `PATCH /pedidos/<id>/status`

---

## 🟠 EP-04 — Tables & Reservations

**Assignee:** [Teammate 3]

**Model Tasks (Create in `app/models/`):**

- [ ] `mesa.py`

**Endpoint Tasks:**

- [ ] `GET /mesas`
- [ ] `POST /reservas` (check table capacity)

---

## 🟢 EP-05 & EP-06 — Admin, Kitchen & Inventory

**Assignee:** [Teammate 4]

**Model Tasks (Create in `app/models/`):**

- [ ] `inventario.py` (`Insumo`, `Inventario`, `Receta`)
- [ ] `pedido.py` (`Venta`) - _Coordinate with Teammate 2 on `pedido.py`_
- [ ] `catalogos.py` (`MetodoPago`)

**Endpoint Tasks:**

- [ ] `GET /cocina/pedidos`
- [ ] `PATCH /cocina/pedidos/<id>/ready`
- [ ] `POST /caja/ventas`
