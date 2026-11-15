
def test_smoke_db_is_reachable(client):
    response = client.get("/health/db")
    assert response.status_code == 200