import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Tests use an in-memory database and never connect to the developer's MySQL.
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["APP_ENV"] = "testing"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-that-is-long-enough-for-hs256"
os.environ["CORS_ORIGINS"] = "http://localhost:5173"

from app import create_app
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import get_db
from app.models.password_reset_token import PasswordResetToken
from app.models.user import User
from app.models.user_session import UserSession


@pytest.fixture
def test_engine():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(
        engine,
        tables=[
            User.__table__,
            UserSession.__table__,
            PasswordResetToken.__table__,
        ],
    )
    yield engine
    Base.metadata.drop_all(
        engine,
        tables=[
            PasswordResetToken.__table__,
            UserSession.__table__,
            User.__table__,
        ],
    )
    engine.dispose()


@pytest.fixture
def client(test_engine):
    testing_session = sessionmaker(
        bind=test_engine,
        autoflush=False,
        expire_on_commit=False,
    )

    def override_get_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    application = create_app()
    application.dependency_overrides[get_db] = override_get_db
    with TestClient(application) as test_client:
        yield test_client
    application.dependency_overrides.clear()
