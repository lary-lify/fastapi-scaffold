async def test_create_and_list_users(superuser_token, client):
    # Create a normal user.
    resp = await client.post(
        "/api/users",
        json={"email": "user@test.com", "full_name": "Normal", "password": "userpass1"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert resp.status_code == 201, resp.text
    created = resp.json()
    assert created["email"] == "user@test.com"
    assert created["is_superuser"] is False

    # Duplicate email rejected.
    dup = await client.post(
        "/api/users",
        json={"email": "user@test.com", "password": "userpass1"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert dup.status_code == 400

    # List returns both accounts.
    listing = await client.get(
        "/api/users", headers={"Authorization": f"Bearer {superuser_token}"}
    )
    assert listing.status_code == 200
    assert len(listing.json()) >= 2


async def test_create_user_forbidden_for_normal_user(superuser_token, client):
    # Make a non-superuser token.
    await client.post(
        "/api/users",
        json={"email": "normal@test.com", "full_name": "N", "password": "normalpass1"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    login = await client.post(
        "/api/auth/login",
        data={"username": "normal@test.com", "password": "normalpass1"},
    )
    token = login.json()["access_token"]

    resp = await client.post(
        "/api/users",
        json={"email": "another@test.com", "password": "anotherpass1"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 403


async def test_update_me(superuser_token, client):
    resp = await client.patch(
        "/api/users/me",
        json={"full_name": "Renamed"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["full_name"] == "Renamed"
