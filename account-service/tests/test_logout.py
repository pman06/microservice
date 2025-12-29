def test_logout_revokes_refresh_toekn(client, user):
    token = client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "password"
    })

    refresh = token.get_json()["refresh_token"]

    res = client.post("/auth/logout", json={
        "refresh_token": refresh
    })

    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"
    