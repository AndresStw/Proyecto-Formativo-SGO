from app import create_app


def test_health():
    app = create_app()
    client = app.test_client()
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_404():
    app = create_app()
    client = app.test_client()
    r = client.get("/ruta-que-no-existe")
    assert r.status_code == 404