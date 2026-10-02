import logging
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

logger = logging.getLogger("dayflow.db")

class DatabaseManager:
    client: AsyncIOMotorClient = None
    db = None

db_manager = DatabaseManager()

import certifi

async def connect_to_mongo():
    logger.info(f"Connecting to MongoDB at {settings.MONGO_URI}...")
    try:
        db_manager.client = AsyncIOMotorClient(
            settings.MONGO_URI,
            serverSelectionTimeoutMS=5000,
            tlsAllowInvalidCertificates=True
        )
        # Test connection ping
        await asyncio.wait_for(db_manager.client.admin.command('ping'), timeout=5.0)
        db_manager.db = db_manager.client[settings.DB_NAME]
        logger.info(f"Successfully connected to MongoDB database '{settings.DB_NAME}'.")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB database at {settings.MONGO_URI}: {e}")
        raise e

async def close_mongo_connection():
    if db_manager.client:
        db_manager.client.close()
        logger.info("MongoDB connection closed.")

def get_database():
    return db_manager.db
