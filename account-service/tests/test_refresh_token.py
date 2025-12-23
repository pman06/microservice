from app.utils.password_hash import hash_password
def login(client):
    res = client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "password"
    })

    return res

def test_refresh_token_rotation(client, user):
    tokens = login(client)
    refresh = tokens.get_json()["refresh_token"]

    res = client.post("/auth/refresh", json={
        "refresh_token": refresh
    })

    data = res.get_json()
    assert res.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["refresh_token"] != refresh

def test_refresh_with_revoked_token(client, user):
    tokens = login(client)
    refresh = tokens.get_json()["refresh_token"]

    client.post("/auth/logout", json={
        "refresh_token": refresh
    })

    res = client.post("/auth/refresh", json={
        "refresh_token": refresh
    }) 

    data = res.get_json()
    assert res.status_code == 401
    assert data["error"] == "Invalid or expired refresh token"
