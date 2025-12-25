def get_token(client, email):
    res = client.post("/auth/login", json={
        "email": email,
        "password": "password"
    })

    return res.get_json()["refresh_token"]


def test_admin_access_allowed(client, admin):
    token = get_token(client, "admin@test.com")

    res = client.get("/admin/dashboard", headers={
        "Authorization": f"Bearer {token}"
    })

    assert res.status_code == 200