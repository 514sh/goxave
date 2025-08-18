from dotenv import dotenv_values
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

config = {
  **dotenv_values(".env.local")
}

_db_client = None

def get_mongo_db_client():
  global _db_client
  if _db_client is None:
    mongo_uri = f"mongodb://{config.get("DB_HOST")}:{config.get("DB_PORT")}/"
    return AsyncIOMotorClient(mongo_uri)
  return _db_client
