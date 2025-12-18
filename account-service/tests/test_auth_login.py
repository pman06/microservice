from conftest import client, user

def test_login_success(client, user):
    res = client.post("/auth/login", json={
        'email': "user@test.com",
        "password": "password"
    })

    assert res.status_code == 200
    data = res.get_json()
    assert "access_token" in data
    assert "refresh_token" in data