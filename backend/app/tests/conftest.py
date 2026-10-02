import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.main import app
from app.db.mongodb import db_manager

@pytest.fixture
async def setup_test_db():
    client = AsyncIOMotorClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000, tlsAllowInvalidCertificates=True)
    db_manager.client = client
    db_manager.db = client["dayflow_test_db"]
    yield
    try:
        await client.drop_database("dayflow_test_db")
        client.close()
    except Exception:
        pass

@pytest.fixture
async def async_client(setup_test_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
