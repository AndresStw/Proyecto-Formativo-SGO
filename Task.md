---

## 📄 File 3: `TASKS.md` (English — organized by epics)

```markdown
# Task Breakdown — Sabor Caleño Backend

**Current status:** `/health`, `/health/db`, `/productos` running. Supabase connection OK.

Tasks are grouped by **epic** as defined in the RF/RNF/EP specification document. Each task has clear input/output contracts so teammates can work in parallel.

---

## 🔴 EP-01 — Authentication & Accounts (BLOCKING)

**Why first:** every other endpoint requires the JWT middleware.

**Responsible:** **\*\*\*\***\_**\*\*\*\***

**Reference:** RF-AUTH-01 to RF-AUTH-08

**Files to create:**

- `app/models/usuario.py`
- `app/schemas/auth.py`
- `app/services/auth_service.py`
- `app/api/auth.py`
- `app/utils/security.py`
- `app/utils/decorators.py` (`@require_auth` middleware)
- `tests/test_auth.py`

**Endpoints:**
| Method | Path | Body | Response |
|---|---|---|---|
| POST | `/register` | `{email, password, nombre, telefono?}` | `{accessToken, user:{id,email,nombre}}` |
| POST | `/login` | `{email, password}` | `{accessToken, user:{...}}` |
| GET | `/auth/me` | — (`Authorization: Bearer <token>`) | `{id,email,nombre,rol}` |
| POST | `/auth/logout` | — | `{ok:true}` (frontend clears token) |

**Business rules to enforce:**

- **RN-01:** Password ≥ 6 chars, hashed with bcrypt
- **RN-02:** Email must be unique per user
- **RN-03:** JWT must include `rol` and expire (default 24h)
- **RN-05:** Public `/register` **always** creates role `Cliente` (ignore any `rol` sent in the form)

**Dependencies:** `bcrypt`, `PyJWT`, `email-validator`

**Acceptance criteria:**

- [ ] Registration creates rows in `Usuario` + `Cliente`
- [ ] Login returns a JWT valid for 24h
- [ ] `/auth/me` without token returns 401
- [ ] Passwords stored with bcrypt (never plain text)
- [ ] A user registering with `rol: "admin"` in body still gets `Cliente` role

---

## 🟡 EP-02 — Catalog Visualization & Filtering (parallel)

**Can start in parallel with EP-01.**

**Responsible:** **\*\*\*\***\_**\*\*\*\***

**Reference:** RF-CAT-01 to RF-CAT-06

**Files:**

- `app/models/plato.py`, `app/models/tipo_plato.py`
- `app/schemas/producto.py`
- `app/services/producto_service.py`
- `app/api/productos.py`
- `tests/test_productos.py`

**Endpoints:**
| Method | Path | Query | Response |
|---|---|---|---|
| GET | `/productos` | `?categoria=platos` (optional) | `[{id,nombre,precio,categoria,imagen,...}]` |
| GET | `/productos/<id>` | — | `{...}` |

**Business rules:**

- **RN-01:** Dishes with `disponible=false` must be returned with `disponible: false`
- **RN-02:** Catalog must load in < 2.5s (server side: pagination + indexes)

**Acceptance criteria:**

- [ ] Returns all available dishes
- [ ] Category filter works (`desayunos`, `caldos`, `bebidas`, `platos`, `postres`)
- [ ] `categoria` field maps `Tipo_Plato.nombre_tipo` → frontend string

---

## 🟠 EP-03 — Shopping Cart & Order Processing

**Depends on:** EP-01, EP-02

**Responsible:** **\*\*\*\***\_**\*\*\*\***

**Reference:** RF-CAR-01 to RF-CAR-12

**Files:**

- `app/models/pedido.py`, `app/models/detalle_pedido.py`
- `app/models/estado_pedido.py`, `app/models/modalidad_pedido.py`
- `app/schemas/pedido.py`
- `app/services/pedido_service.py`
- `app/api/pedidos.py`
- `tests/test_pedidos.py`

**Endpoints:**
| Method | Path | Body | Response |
|---|---|---|---|
| POST | `/pedidos` | `{items:[{plato_id,cantidad}], modalidad_id, observaciones?}` | `{id, total, estado:"Pendiente"}` |
| GET | `/pedidos` | — | List of authenticated user's orders |
| GET | `/pedidos/<id>` | — | Order detail |
| PATCH | `/pedidos/<id>/status` | `{estado_id}` | Updated order |

**Business rules:**

- **RN-02:** New orders start in `Pendiente` status
- **RN-03:** Validate dish availability before confirming
- **RN-04:** Chat simulation adds items to the real cart

**Acceptance criteria:**

- [ ] Client only sees their own orders
- [ ] Total is calculated automatically from `precio_unitario * cantidad`
- [ ] Status transitions are validated (Pendiente → En Preparación → Listo → Entregado)
- [ ] `fecha_hora` is set automatically

---

## 🟠 EP-04 — Table Administration & Reservations

**Depends on:** EP-01

**Responsible:** **\*\*\*\***\_**\*\*\*\***

**Reference:** RF-RES-01 to RF-RES-04

**Files:**

- `app/models/mesa.py`, `app/models/reserva.py`
- `app/schemas/mesa.py`, `app/schemas/reserva.py`
- `app/services/mesa_service.py`, `app/services/reserva_service.py`
- `app/api/mesas.py`, `app/api/reservas.py`
- `tests/test_reservas.py`

**Endpoints:**
| Method | Path | Body | Response |
|---|---|---|---|
| GET | `/mesas` | — | List of tables with state |
| POST | `/reservas` | `{fecha, hora, personas, nombre, telefono, mesa_id?}` | `{id, estado:"Confirmada"}` |
| GET | `/reservas` | — | List of reservations (admin/mesero) |
| PATCH | `/mesas/<id>/state` | `{estado}` | Updated table |

**Business rules:**

- **RN-01:** Cannot reserve for past dates
- **RN-02:** Party size cannot exceed table capacity
- **RN-03:** 15-minute tolerance before releasing a table
- **RN-04:** Client can only cancel with 2h notice

**Acceptance criteria:**

- [ ] Client can create a reservation
- [ ] Admin/mesero see all reservations
- [ ] Validates table availability for the requested time slot
- [ ] Rejects reservations for past dates and over-capacity parties

---

## 🟠 EP-06 — Kitchen & Cashier Operations

**Depends on:** EP-01, EP-03

**Responsible:** **\*\*\*\***\_**\*\*\*\***

**Reference:** RF-PED-01 to RF-PED-10

**Files:**

- `app/schemas/cocina.py`, `app/schemas/venta.py`
- `app/services/cocina_service.py`, `app/services/venta_service.py`
- `app/api/cocina.py`, `app/api/caja.py`
- `app/models/venta.py`, `app/models/cajero.py`
- `tests/test_cocina.py`, `tests/test_caja.py`

**Endpoints:**
| Method | Path | Response |
|---|---|---|
| GET | `/cocina/pedidos` | Orders in `Pendiente` or `En Preparación` status |
| PATCH | `/cocina/pedidos/<id>/ready` | Marks order as `Listo` |
| POST | `/caja/ventas` | `{pedido_id, metodo_pago_id, total}` |
| GET | `/caja/ventas/today` | Today's sales report |

**Business rules:**

- **RN-01:** Cook only sees `Pendiente` or `En Preparación` orders
- **RN-02:** Marking as `Listo` notifies waiter/cashier
- **RN-03:** Sale only registers if order is `Listo` or `Entregado`

**Acceptance criteria:**

- [ ] Only `Cocinero` or `Admin` roles can access `/cocina/*`
- [ ] Only `Cajero` or `Admin` can register sales
- [ ] Marking ready updates `hora_entrega`
- [ ] Sale creation validates order state

---

## 🟢 EP-05 — Admin Panel & System Control

**Depends on:** EP-01, EP-02, EP-03, EP-04

**Responsible:** **\*\*\*\***\_**\*\*\*\***

**Reference:** RF-ADM-01 to RF-ADM-10

**Files:**

- `app/schemas/admin.py`
- `app/services/admin_service.py`
- `app/api/admin.py`
- `app/models/insumo.py`, `app/models/inventario.py`
- `tests/test_admin.py`

**Endpoints:**
| Method | Path | Response |
|---|---|---|
| GET | `/admin/dashboard` | Today's metrics (sales, active orders, occupied tables) |
| GET | `/admin/usuarios` | All users |
| POST/PUT/DELETE | `/admin/platos` | Dish CRUD (soft delete) |
| GET | `/admin/inventario` | Stock levels + low-stock alerts |
| GET | `/admin/ventas` | Sales history with date filters |

**Business rules:**

- **RN-01:** Only `Admin` role can access this module
- **RN-02:** Dishes are soft-deleted (`disponible=false`), never physically deleted
- **RN-03:** Closed sales cannot be modified
- **RN-04:** Stock below minimum triggers a dashboard alert

**Acceptance criteria:**

- [ ] Admin sees today's metrics on login
- [ ] Creating a dish makes it appear on the client menu
- [ ] Alert shows when an insumo drops below `stock_minimo`
- [ ] Non-admin users get 403

---

## 🔵 EP-07 — Interface Personalization

**Depends on:** EP-01 (optional)

**Responsible:** **\*\*\*\***\_**\*\*\*\***

**Reference:** RF-UX-01 to RF-UX-05

**Note:** Most of this epic lives on the **frontend** (localStorage + CSS variables). Backend work is **optional** — only if you want to persist preferences per user across devices.

**Optional endpoints:**
| Method | Path | Body | Response |
|---|---|---|---|
| GET | `/users/me/preferences` | — | `{theme:"green"\|"yellow"\|"pink"\|"blue"}` |
| PUT | `/users/me/preferences` | `{theme}` | Updated preferences |

**Acceptance criteria (if implemented):**

- [ ] Preferences persisted in `Usuario` table (add column `theme VARCHAR(20)`)
- [ ] `PUT` validates theme against allowed values
- [ ] Only the authenticated user can modify their own preferences

---

## 🔵 EP-08 (optional) — Data migration

**Parallel task, no dependencies.**

**Responsible:** **\*\*\*\***\_**\*\*\*\***

**Objective:** Populate `Plato` table with the 21 products from `menuData.js`.

**Files:**

- `scripts/seed_productos.py`

**Acceptance criteria:**

- [ ] Script is idempotent (running twice does not duplicate)
- [ ] All 21 products are in `Plato`
- [ ] Dish types match `menuData.categorias`

---

## 📅 Suggested order of work

**Week 1:**

- Lead + Dev A → **EP-01** (Auth)
- Dev B → **EP-02** (Products)
- Dev C → **EP-08** (Data migration)
- Dev D → Vercel deploy setup

**Week 2:**

- Dev A → **EP-04** (Tables & Reservations)
- Dev B → **EP-03** (Orders)
- Dev C → **EP-06** (Kitchen & Cashier)
- Dev D → Tests + documentation

**Week 3:**

- Everyone → **EP-05** (Admin) + **EP-07** (Personalization)

---

## ⚠️ Coordination between epics

- **JWT contract:** EP-01 defines the token format. All other epics only use `@require_auth` and `g.current_user.idUsuario`.
- **Order contract:** EP-03 defines `PedidoOut` schema. EP-06 and EP-05 consume it.
- **Product contract:** EP-02 defines `ProductoOut`. EP-03 uses it to calculate totals.
- **Database:** if an epic needs a new table, **notify the lead** first so it can be created in Supabase (or open a PR with a migration).
