def test_missing_token(client):
    res = client.get('/admin/dashboard')
    assert res.status_code == 401