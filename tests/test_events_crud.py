# tests/test_events_crud.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from lab02.main import create_app
from lab02.db import Base, get_db


@pytest.fixture(scope="function")
def client():
    """
    FastAPI TestClient using ONE shared in-memory SQLite database
    so that the schema persists across connections.
    """
    # 1) Shared in-memory engine (StaticPool keeps a single connection)
    engine = create_engine(
        "sqlite://",  # note: no /:memory: when using StaticPool
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # 2) Import models so Base knows the tables, then create schema
    from lab02 import models  # noqa: F401
    Base.metadata.create_all(bind=engine)

    # 3) Override FastAPI dependency to use our test session
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c


def test_crud_flow(client: TestClient):
    # CREATE
    r = client.post("/events/", json={"title": "Launch", "details": "T-10"})
    assert r.status_code == 201
    created = r.json()
    event_id = created["id"]
    assert created["title"] == "Launch"

    # LIST
    r = client.get("/events/")
    assert r.status_code == 200
    assert any(e["id"] == event_id for e in r.json())

    # GET by id
    r = client.get(f"/events/{event_id}")
    assert r.status_code == 200
    assert r.json()["details"] == "T-10"

    # UPDATE (PUT)
    r = client.put(f"/events/{event_id}", json={"title": "Liftoff", "details": "T+0"})
    assert r.status_code == 200
    assert r.json()["title"] == "Liftoff"

    # DELETE
    r = client.delete(f"/events/{event_id}")
    assert r.status_code == 204

    # VERIFY deletion
    assert client.get(f"/events/{event_id}").status_code == 404
    assert all(e["id"] != event_id for e in client.get("/events/").json())
