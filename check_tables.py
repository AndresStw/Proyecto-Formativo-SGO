from app.infrastructure.database.connection import engine
from sqlalchemy import text

with engine.connect() as conn:
    rows = conn.execute(text(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema = 'public' ORDER BY table_name"
    )).scalars().all()
    print("TABLES:", list(rows))

    if rows:
        for t in rows:
            count = conn.execute(text(f'SELECT COUNT(*) FROM "{t}"')).scalar()
            print(f"  {t}: {count} filas")
    else:
        print("No hay tablas. Ejecuta el SQL del Bloque 0.")