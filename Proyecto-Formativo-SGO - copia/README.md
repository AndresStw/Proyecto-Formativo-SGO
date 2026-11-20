# Backend — Sabor Caleño SGO

<<<<<<< HEAD
<p align="center">
  <img src="https://img.shields.io/badge/Estado-En%20desarrollo-blue" alt="Estado: en desarrollo">
  <img src="https://img.shields.io/github/last-commit/AndresStw/Proyecto-Formativo-SGO/main?label=%C3%BAltimo%20commit" alt="Último commit">
  <img src="https://img.shields.io/github/contributors/AndresStw/Proyecto-Formativo-SGO?label=contribuyentes" alt="Contribuyentes">
  <img src="https://img.shields.io/github/stars/AndresStw/Proyecto-Formativo-SGO?style=social" alt="Estrellas">
</p>

Repositorio académico del Proyecto Formativo SGO, enfocado en el análisis, la documentación y el desarrollo del sistema de gestión de operaciones de **Sabor Caleño**.
=======
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
>>>>>>> origin/Backend

## 📋 Contenido

<<<<<<< HEAD
- **Trimestre I:** requisitos funcionales y no funcionales, presentaciones iniciales, diagramas BPMN y análisis preliminares.
- **Trimestre II:** extensiones del proyecto, presentaciones, cotizaciones, análisis de proveedores y SRS.
- **Trimestre III:** avances y entregables del proyecto.
- **Trimestre IV:** desarrollo del sistema Sabor Caleño SGO.

Explora las carpetas [`Trimestre I`](./Trimestre%20I/), [`Trimestre II`](./Trimestre%20II/), [`Trimestre III`](./Trimestre%20III/) y [`Trimestre IV`](./Trimestre%20IV/).

## 🎯 Objetivos

1. Mejorar la experiencia de usuario en los procesos de gestión organizacional.
2. Consolidar la documentación y los artefactos del proyecto.
3. Facilitar la colaboración entre los integrantes del equipo.
4. Mantener un registro claro de requisitos, análisis y decisiones de diseño.

## 📊 Lenguajes

Composición del código detectada por GitHub para este repositorio. La tabla se actualiza con GitHub Actions.

<!-- languages:start -->
| Lenguaje | Tamaño | Proporción |
| --- | ---: | ---: |
| HTML | 57.3 KB | 48.0 % |
| CSS | 40.4 KB | 33.9 % |
| JavaScript | 21.6 KB | 18.1 % |
<!-- languages:end -->

[Ver ejecuciones de actualización de lenguajes](https://github.com/AndresStw/Proyecto-Formativo-SGO/actions/workflows/update-language-stats.yml).

## 📈 Commits por colaborador

La animación muestra los commits que GitHub atribuye a los colaboradores de este repositorio. Se actualiza automáticamente con cada cambio en `main` y semanalmente.

<p align="center">
  <img src="https://raw.githubusercontent.com/AndresStw/Proyecto-Formativo-SGO/main/stats/contributors.gif" alt="Gráfico animado de commits por colaborador en Proyecto Formativo SGO">
</p>

Consulta también la [página de contribuidores](https://github.com/AndresStw/Proyecto-Formativo-SGO/graphs/contributors), el [historial de commits](https://github.com/AndresStw/Proyecto-Formativo-SGO/commits/main/) y la [actividad de commits](https://github.com/AndresStw/Proyecto-Formativo-SGO/graphs/commit-activity).

## 🌿 Ramas

La rama predeterminada es [`main`](https://github.com/AndresStw/Proyecto-Formativo-SGO/tree/main). Revisa [todas las ramas](https://github.com/AndresStw/Proyecto-Formativo-SGO/branches) para ver las ramas de trabajo disponibles.

## 📁 Estructura

```text
Proyecto-Formativo-SGO/
├── .github/
│   ├── scripts/
│   │   └── generate-contributor-chart.py
│   └── workflows/
│       ├── update-language-stats.yml
│       └── update-contributor-stats.yml
├── stats/
│   └── contributors.gif  (generado por GitHub Actions)
├── Trimestre I/
├── Trimestre II/
├── Trimestre III/
├── Trimestre IV/
└── README.md
```
=======
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
>>>>>>> origin/Backend
