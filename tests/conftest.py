import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.core.database import Base, engine, init_db
from app.main import app


@pytest_asyncio.fixture
async def client():
    await init_db()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def superuser_token(client):
    """Create a superuser directly in the DB and return a valid access token."""
    from app.core.database import SessionLocal
    from app.core.security import get_password_hash
    from app.models.user import User

    async with SessionLocal() as s:
        s.add(
            User(
                email="admin@test.com",
                hashed_password=get_password_hash("adminpass1"),
                full_name="Admin",
                is_superuser=True,
                is_active=True,
            )
        )
        await s.commit()

    resp = await client.post(
        "/api/auth/login",
        data={"username": "admin@test.com", "password": "adminpass1"},
    )
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]
