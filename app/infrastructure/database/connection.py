"""Motor de conexión a Supabase (PostgreSQL) + session factory."""
from contextlib import contextmanager
from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()

# Detección automática de Supabase para ajustar SSL y pooler
_is_supabase = "supabase.co" in settings.database_url or "pooler.supabase.com" in settings.database_url

connect_args: dict = {}
if _is_supabase:
    connect_args["sslmode"] = "require"
    # CRÍTICO con el Transaction Pooler (puerto 6543):
    # desactiva los prepared statements que el pooler no soporta.
    connect_args["prepare_threshold"] = None

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=2,
    connect_args=connect_args,
)

SessionFactory = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


@contextmanager
def get_session() -> Iterator[Session]:
    """
    Context manager que garantiza commit/rollback/close.
    Uso:
        with get_session() as db:
            ...
    """
    db = SessionFactory()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()