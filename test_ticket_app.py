import pytest
from fastapi.testclient import TestClient

from ticket_app.auth_service import AuthService
from ticket_app.dependencies import get_auth_service, get_current_user, get_service
from ticket_app.main import app
from ticket_app.service import TicketService
from ticket_app.store import TicketStore
from ticket_app.user_store import UserStore


ANA = {"id": 1, "username": "ana"}
LUIS = {"id": 2, "username": "luis"}


@pytest.fixture
def client():
    ticket_service = TicketService(TicketStore())
    auth_service = AuthService(UserStore())
    app.dependency_overrides[get_service] = lambda: ticket_service
    app.dependency_overrides[get_auth_service] = lambda: auth_service
    yield TestClient(app)
    app.dependency_overrides.clear()


def log_in_as(user):
    app.dependency_overrides[get_current_user] = lambda: user


def test_create_requires_login(client):
    assert client.post("/tickets", json={"title": "A"}).status_code == 401


def test_owner_can_delete(client):
    log_in_as(ANA)
    client.post("/tickets", json={"title": "A"})
    assert client.delete("/tickets/1").status_code == 204


def test_other_user_gets_403(client):
    log_in_as(ANA)
    client.post("/tickets", json={"title": "A"})
    log_in_as(LUIS)
    assert client.delete("/tickets/1").status_code == 403


def test_real_login_flow(client):
    client.post("/auth/register", json={"username": "ana", "password": "pw"})
    token = client.post("/auth/login", json={"username": "ana", "password": "pw"}).json()["access_token"]
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "ana"}


#deprecated
##@pytest.fixture
##def client():
##    fresh_service = TicketService(TicketStore())              # one empty store for THIS test
##    app.dependency_overrides[get_service] = lambda: fresh_service
##    yield TestClient(app)
##    app.dependency_overrides.clear()                          # undo the swap after the test
##
##
##def test_create_ticket_returns_201(client):
##    response = client.post("/tickets", json={"title": "Login broken"})
##    assert response.status_code == 201
##    assert response.json() == {"id": 1, "title": "Login broken", "priority": "low"}
##
##
##def test_duplicate_title_returns_409(client):
##    client.post("/tickets", json={"title": "Login broken"})
##    response = client.post("/tickets", json={"title": "Login broken"})
##    assert response.status_code == 409
##
##
##def test_invalid_priority_returns_422(client):
##    response = client.post("/tickets", json={"title": "Slow page", "priority": "urgent"})
#    assert response.status_code == 422