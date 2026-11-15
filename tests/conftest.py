import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ticket_app.main import app
from ticket_app.database import Base
from ticket_app.dependencies import get_session
from ticket_app import orm_models  # noqa: F401  (importing registers User/Ticket on Base.metadata)

TEST_DATABASE_URL = "postgresql+psycopg://postgres:secret@localhost:5432/tickets_test"
test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(bind=test_engine)


@pytest.fixture
def db_session():
    """Fresh tables for every test + a session the TEST uses to inspect the DB."""
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
    session = TestSessionLocal()
    yield session
    session.close()

@pytest.fixture
def client(db_session):
    """TestClient whose requests use the test DB instead of `tickets`."""
    def override_get_session():
        session = TestSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def ana(client):
    """Seed: user 'ana' with one ticket. Returns her token and ticket id."""
    client.post("/auth/register", json={"username": "ana", "password": "ana_pw"})
    token = client.post("/auth/login", json={"username": "ana", "password": "ana_pw"}).json()["access_token"]
    ticket = client.post(
        "/tickets",
        json={"title": "Ana's ticket", "priority": "low"},
        headers={"Authorization": f"Bearer {token}"},
    ).json()
    return {"token": token, "ticket_id": ticket["id"]}
