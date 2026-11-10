# Backend — Sabor Caleño SGO

REST API for the **Sabor Caleño** project (restaurant management: users, menu, orders, kitchen, admin).

- **Framework:** Flask 3
- **ORM:** SQLAlchemy 2 (sync)
- **Database:** PostgreSQL on Supabase
- **Deploy:** Vercel (`@vercel/python`)
- **Auth:** JWT + bcrypt

---

## 📋 Prerequisites

| Tool   | Min Version | Check              |
| ------ | ----------- | ------------------ |
| Python | 3.11+       | `python --version` |
| pip    | 24+         | `pip --version`    |
| Git    | any recent  | `git --version`    |

---

## 🚀 First-time setup

### 1. Clone the repository

```powershell
git clone <REPO_URL>
cd Proyecto-Formativo-SGO/Proyecto-Formativo-SGO
```

> ⚠️ The project is nested in two folders with the same name. Work inside the **inner** one (where `app/main.py` lives).

### 2. Create and activate the virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

You'll know it worked when the prompt starts with `(venv)`.

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

```powershell
copy .env.example .env
```

Open `.env` in VS Code and **replace `TU_PASSWORD`** with the real Supabase password. Ask for it on the team's private channel (WhatsApp/Discord) — **never through GitHub**.

### 5. Verify the connection

```powershell
python check_tables.py
```

Expected output:

```
TABLES: ['Cliente', 'Plato', 'Tipo_Plato', 'Usuario']
  Cliente: 0 filas
  Plato: 0 filas
  Tipo_Plato: 7 filas
  Usuario: 0 filas
```

If you see `TABLES: []` or an error, check **Troubleshooting** below.

### 6. Start the server

```powershell
flask --app "app:create_app" --debug run --port 8000
```

Open `http://localhost:8000/health` in the browser. Expected:

```json
{ "status": "ok", "service": "Sabor Caleño SGO" }
```

---

## 🔌 How the Supabase connection works

This section explains **why** the connection string looks the way it does. If something fails, this is your diagnostic reference.

### Connection string anatomy

```
postgresql+psycopg://USER:PASSWORD@HOST:PORT/postgres
└──────┬─────────┘ └────┬─────┘ └──────┬───────┘
       │                │              │
       │                │              └─ Supabase pooler host
       │                └─ Supabase user + password
       └─ Driver: psycopg 3 (NOT psycopg2)
```

### Why `postgresql+psycopg://` and not `postgresql://`?

SQLAlchemy needs to know **which driver** to use. With plain `postgresql://` it defaults to `psycopg2` (old, not installed). `+psycopg` tells it to use **psycopg 3** (modern).

| Prefix                      | Driver             | Works here?      |
| --------------------------- | ------------------ | ---------------- |
| `postgresql://`             | psycopg2 (default) | ❌ Not installed |
| `postgresql+psycopg2://`    | psycopg2           | ❌ Not installed |
| **`postgresql+psycopg://`** | **psycopg 3**      | ✅ **Yes**       |

### Why port `6543` and not `5432`?

Supabase offers 3 connection types:

| Type                   | Port     | Host                                | When to use                            |
| ---------------------- | -------- | ----------------------------------- | -------------------------------------- |
| Direct Connection      | 5432     | `db.xxx.supabase.co`                | Apps with persistent connections (VMs) |
| **Transaction Pooler** | **6543** | **`aws-0-xxx.pooler.supabase.com`** | **Serverless / Vercel** ✅             |
| Session Pooler         | 5432     | `aws-0-xxx.pooler.supabase.com`     | IPv4-only without IPv6                 |

Since we deploy to **Vercel**, every request opens/closes a connection → **Transaction Pooler (6543)** is mandatory. Direct connection exhausts Supabase's Free plan limit in seconds.

### Why `prepare_threshold=None`?

PostgreSQL prepared statements don't work through the Transaction Pooler (each request may hit a different backend in the pool). We disable them in `app/infrastructure/database/connection.py`:

```python
connect_args["prepare_threshold"] = None
```

Without this you get errors like `prepared statement "s1" already exists`.

### Why `sslmode="require"`?

Supabase enforces SSL. Without it the driver rejects the connection with `SSL required`.

---

## 🧪 Available endpoints

| Method | Path              | Description                 | Auth   |
| ------ | ----------------- | --------------------------- | ------ |
| `GET`  | `/health`         | Server healthcheck          | —      |
| `GET`  | `/health/db`      | Healthcheck + DB ping       | —      |
| `GET`  | `/productos`      | List dishes (`?categoria=`) | —      |
| `GET`  | `/productos/<id>` | Dish detail                 | —      |
| `POST` | `/login`          | Sign in (returns JWT)       | —      |
| `POST` | `/register`       | Register new user           | —      |
| `GET`  | `/auth/me`        | Current user profile        | 🔒 JWT |

### Example with PowerShell

```powershell
# List products
Invoke-RestMethod http://localhost:8000/productos

# Filtered products
Invoke-RestMethod "http://localhost:8000/productos?categoria=platos"

# Register a user
Invoke-RestMethod -Method Post -Uri http://localhost:8000/register `
  -ContentType "application/json" `
  -Body '{"email":"test@saborcaleno.com","password":"123456","nombre":"Test User"}'

# Login
Invoke-RestMethod -Method Post -Uri http://localhost:8000/login `
  -ContentType "application/json" `
  -Body '{"email":"test@saborcaleno.com","password":"123456"}'
```

---

## 🩺 Troubleshooting

| Error                                          | Cause                                  | Fix                                                                              |
| ---------------------------------------------- | -------------------------------------- | -------------------------------------------------------------------------------- |
| `Import "flask" could not be resolved`         | VS Code uses wrong interpreter         | `Ctrl+Shift+P` → **Python: Select Interpreter** → pick `venv\Scripts\python.exe` |
| `No module named 'psycopg2'`                   | URL missing `+psycopg`                 | Edit `.env`: `postgresql+psycopg://`                                             |
| `failed to resolve host '...'` with weird text | Password contains `@` without encoding | URL-encode (`@`→`%40`) or reset password to alphanumeric                         |
| `password authentication failed`               | Wrong password                         | Ask the team for the correct one                                                 |
| `prepared statement "s1" already exists`       | Port 5432 (direct)                     | Change to `:6543`                                                                |
| `SSL required`                                 | Missing SSL                            | Already configured in `connection.py`; restart the process                       |
| `TimeoutError` on connect                      | Firewall / wrong region                | Verify host, test on mobile hotspot                                              |
| `TABLES: []`                                   | No tables                              | Run the schema SQL in Supabase                                                   |

---

## 📁 Project structure

```
Proyecto-Formativo-SGO/
├── api/
│   └── index.py                    ← Vercel entrypoint
├── app/
│   ├── __init__.py                 ← create_app() factory
│   ├── core/
│   │   ├── config.py               ← Reads .env
│   │   └── exceptions.py           ← Business exceptions
│   ├── infrastructure/
│   │   └── database/
│   │       ├── base.py             ← SQLAlchemy declarative base
│   │       └── connection.py       ← Engine + get_session()
│   ├── models/                     ← SQLAlchemy tables
│   ├── schemas/                    ← Pydantic validation
│   ├── services/                   ← Business logic
│   └── api/                        ← Blueprints (endpoints)
├── tests/                          ← Pytest
├── .env.example                    ← Template (YES to repo)
├── .env                            ← Real (NO to repo)
├── requirements.txt
├── check_tables.py                 ← DB diagnostic
└── vercel.json
```

---

## 👥 Team workflow

- **Git workflow:** see [`CONTRIBUTING.md`](./CONTRIBUTING.md)
- **Task breakdown by epic:** see [`TASKS.md`](./TASKS.md)
- **Database:** only the **project lead** runs SQL on Supabase (request changes via PR)
