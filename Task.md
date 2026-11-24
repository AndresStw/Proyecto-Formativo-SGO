# Task Breakdown — Sabor Caleño Backend

**Current status:**

- ✅ Local MySQL (XAMPP) connected.
- ✅ Alembic configured.
- ✅ Authentication and business tables are created in MySQL.
- ✅ Alembic is at revision `e09827dd3b4d`.

---

## ⚠️ IMPORTANT: How to create a Model (ORM)

Each Epic must create its own files inside `app/models/`.
Create and review a migration for each new model set before applying it to a shared database. Keep relationships aligned with the single `users` table for account roles.

Example workflow for your task:

1. Create the `.py` files in `app/models/`.
2. Update `app/models/__init__.py` to import your new models.
3. Run `python -c "import app.models; print('OK')"` to ensure no import errors.
4. Generate and review an Alembic migration, then run `alembic upgrade head` in the intended environment.

---

## 🔴 EP-01 — Authentication & Accounts (BLOCKING) - ✅ COMPLETED

**Assignee:** Lead
**Framework:** FastAPI + SQLAlchemy + JWT

_Architecture note: account roles use one `users` table with a `role` column. Business records reference `users.id`; there are no separate account tables for customers, waiters, cooks, cashiers or administrators._

**Model tasks (`app/models/`):**

- [x] `user.py` (`id`, names, email, `password_hash`, phone, address, role, active state).
- [x] Persist JWT sessions and one-time password reset tokens.

**Endpoint tasks (`app/api/v1/auth.py`):**

- [x] `POST /api/v1/auth/register` (Creates a `CLIENTE` account and returns a JWT).
- [x] `POST /api/v1/auth/login` (Validates credentials and returns a JWT).
- [x] `GET /api/v1/auth/me` (Protected profile read).
- [x] `PUT /api/v1/auth/me` (Protected profile update).
- [x] `POST /api/v1/auth/logout` (Revokes the current session).
- [x] `POST /api/v1/auth/forgot-password` (Writes a reset link to the application log).
- [x] `POST /api/v1/auth/reset-password` (Validates a reset token and changes the password).
- [x] `GET /api/v1/auth/users` and `POST /api/v1/auth/users` (Administrator account management).

**Authorization dependencies:**

- [x] `get_current_user` (Validates JWT, session, account state and expiry).
- [x] `require_admin` (Protects administrator-only routes).

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
