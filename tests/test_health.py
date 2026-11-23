from app import create_app
from fastapi.testclient import TestClient


def test_health():
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_404():
    client = TestClient(create_app())
    response = client.get("/ruta-que-no-existe")
    assert response.status_code == 404
