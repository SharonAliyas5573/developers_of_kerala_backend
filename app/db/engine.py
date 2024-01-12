from pymongo import MongoClient
from app.core.config import settings


class Database:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]


db = Database(settings.MONGODB_URI, settings.MONGODB_NAME).db
