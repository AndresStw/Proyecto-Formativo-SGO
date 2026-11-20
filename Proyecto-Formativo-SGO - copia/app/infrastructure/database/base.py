from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Clase base de todos los modelos ORM de Harmony Spa.

    Todos los modelos heredarán de esta clase.
    SQLAlchemy utilizará Base.metadata para registrar
    las tablas y sus relaciones.
    """

    pass