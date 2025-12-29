def test_missing_token(client):
    res = client.get('/admin/dashboard')
    assert res.status_code == 401

def test_invalod_jwt_token(client):
    res = client.get('/admin/dashboard', headers={
        "Authorization": f"Bearer invalidtoken"
    })

    assert res.status_code == 401

def test_refresh_without_token(client):
    res = client.post("/auth/refresh")

    assert res.status_code == 400