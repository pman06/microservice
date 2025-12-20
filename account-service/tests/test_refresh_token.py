def login(client):
    res = client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "password"
    })

    return res

def test_refresh_token_rotation(client, user):
