import pytest
from fastapi.testclient import TestClient
from lab02.main import create_app

@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)

def test_create_and_list_events(client):
    r = client.post("/events/", json={"title": "Launch", "details": "T-10"})
    assert r.status_code == 201
    event = r.json()
    assert event["title"] == "Launch"

    r2 = client.get("/events/")
    assert r2.status_code == 200
    items = r2.json()
    assert any(e["title"] == "Launch" for e in items)
