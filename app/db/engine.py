from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from app.core.config import settings


class Database:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]


db = Database(settings.MONGODB_URI, settings.MONGODB_NAME).db


def check_db_connection():
    try:
        # The ismaster command is cheap and does not require auth.
        db.command("ismaster")
        return {"status": "Database is connected"}
    except ServerSelectionTimeoutError as e:
        return {"status": "Database connection failed", "exception": str(e)}
