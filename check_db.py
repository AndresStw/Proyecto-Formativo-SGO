from app.infrastructure.database.connection import engine
from sqlalchemy import text, inspect

def probar_conexion():
    try:
        with engine.connect() as conn:
            # 1. Probar que el servidor responde
            conn.execute(text("SELECT 1"))
            print("✅ ¡Conexión a MySQL (XAMPP) exitosa!")
            
            # 2. Listar las tablas que creó Alembic
            inspector = inspect(engine)
            tablas = inspector.get_table_names()
            
            print(f"\nTablas encontradas en la base de datos ({len(tablas)}):")
            for tabla in tablas:
                print(f"  - {tabla}")
                
            if "Usuario" in tablas and "Plato" in tablas:
                print("\n ¡El ORM y las migraciones funcionaron perfecto!")
            else:
                print("\n Faltan tablas. Asegúrate de haber corrido: alembic upgrade head")
                
    except Exception as e:
        print(f"Error de conexión: {e}")
        print("Revisa que XAMPP (MySQL) esté encendido y que tu .env tenga la URL correcta.")

if __name__ == "__main__":
    probar_conexion()