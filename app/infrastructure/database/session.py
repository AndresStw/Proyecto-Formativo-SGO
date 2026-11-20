from collections.abc import Generator

from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.database.connection import engine


SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """Entrega una sesión por solicitud y siempre la cierra."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()