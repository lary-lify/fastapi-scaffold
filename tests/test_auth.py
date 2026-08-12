async def test_login_wrong_password(client):
    resp = await client.post(
        "/api/auth/login",
        data={"username": "nobody@test.com", "password": "wrong"},
    )
    assert resp.status_code == 401


async def test_login_and_me(superuser_token, client):
    # Valid login is already exercised by the fixture; verify /auth/me.
    resp = await client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {superuser_token}"}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["email"] == "admin@test.com"
    assert body["is_superuser"] is True


async def test_me_requires_token(client):
    resp = await client.get("/api/auth/me")
    assert resp.status_code == 401
