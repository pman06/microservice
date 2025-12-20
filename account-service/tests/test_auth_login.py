from conftest import client, user

def test_login_success(client, user):
    res = client.post("/auth/login", json={
        'email': "user@test.com",
        "password": "password"
    })

    assert res.status_code == 200
    assert res.get_json()["user"]["email"] == user.email
    data = res.get_json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_login_invalid_password(client, user):
    res = client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "wrongpassword"
    })

    assert res.status_code == 401
    assert res.get_json()["error"] == "Invalid credentials"

def test_login_nonexistence_user(client):
    res = client.post("/auth/login", json={
        "email": "wronguser@test.com",
        "password": "password"
    })

    assert res.status_code == 401
    assert res.get_json()["error"] == "Invalid credentials"  

def test_login_no_data(client):
    res = client.post("/auth/login", json=None)

    assert res.status_code == 400
    assert res.get_json()["error"] == "No data provided"