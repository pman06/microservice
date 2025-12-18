def login(client, user):
    res = client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "password"
    })

    return res

