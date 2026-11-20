
# tests/test_auth.py
def test_register_success(client):
    # Arrange: what we'll send
    payload = {"username": "bob", "password": "pw123"}

    # Act: call the API
    response = client.post("/auth/register", json=payload)

    # Assert: status first, then the body
    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "bob"
    assert "id" in body
    assert "password" not in body          # the API must never echo the password back