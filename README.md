# Backend — Sabor Caleño SGO

REST API for the **Sabor Caleño** project. Built with Flask, SQLAlchemy 2, MySQL (XAMPP local), and Alembic.

## 📋 Prerequisites

- Python 3.11+
- **XAMPP** (with MySQL running)
- **TablePlus** or **DBeaver** (optional, to view the database)

## 🚀 First-time setup

### 1. Clone the repo and enter the folder

```powershell
git checkout Backend
git pull origin Backend
cd Proyecto-Formativo-SGO/Proyecto-Formativo-SGO
```

### 2. Create and activate the virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

_(If PowerShell blocks scripts, run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`)_

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Setup the local database (XAMPP)

1. Open XAMPP Control Panel and **Start MySQL**.
2. Open TablePlus or DBeaver and connect to `127.0.0.1:3306` (User: `root`, Password: empty).
3. Run this SQL query to create the empty database:

```sql
CREATE DATABASE sabor_caleno_sgo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configure environment variables

```powershell
copy .env.example .env
```

Ensure your `.env` has the local MySQL URL:

```env
DATABASE_URL=mysql+pymysql://root:@localhost:3306/sabor_caleno_sgo
```

### 6. Run database migrations (Create tables)

This reads the Python models in `app/models/` and creates the tables in XAMPP.
_(Only the Lead runs `upgrade head` on the `Backend` branch once models are merged)._

```powershell
alembic upgrade head
```

### 7. Verify connection

```powershell
python check_db.py
```

You should see: `✅ ¡Conexión a MySQL (XAMPP) exitosa!` and the list of tables.

### 8. Start the server

```powershell
flask --app "app:create_app" --debug run --port 8000
```

---

## 🛑 Git & Database Rules

1. **NEVER** push to `main` or `Backend` directly. Use `feature/epXX-name` branches.
2. **NEVER** edit tables manually in TablePlus/DBeaver. All schema changes go through Python Models + Alembic.
3. **ONLY** the Lead runs `alembic revision` and `alembic upgrade` on the `Backend` branch to avoid merge conflicts.

---

## 🩺 Troubleshooting

| Error                                           | Cause                          | Fix                                                                              |
| ----------------------------------------------- | ------------------------------ | -------------------------------------------------------------------------------- |
| `Import "flask" could not be resolved`          | VS Code uses wrong interpreter | `Ctrl+Shift+P` → **Python: Select Interpreter** → pick `venv\Scripts\python.exe` |
| `Access denied for user 'root'@'localhost'`     | Wrong MySQL password           | Check XAMPP MySQL config or `.env` URL                                           |
| `Unknown database 'sabor_caleno_sgo'`           | Database not created           | Run the `CREATE DATABASE...` SQL in TablePlus                                    |
| `Can't load plugin: sqlalchemy.dialects:driver` | `alembic.ini` has a dummy URL  | Comment out `sqlalchemy.url = driver://...` in `alembic.ini`                     |
