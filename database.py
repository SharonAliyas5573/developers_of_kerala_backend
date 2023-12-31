from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

client = MongoClient(os.environ.get('MONGODB_URI'), 8000)
db = client.kerala_devs


# Print all collection names
collection = db['developers_talent']

# Retrieve all documents in the collection
documents = collection.find()

# Print all documents
for document in documents:
    print(document)
# db has been initialized and can be imported and used in main.py
# examples of usage : https://www.w3schools.com/python/python_mongodb_getstarted.asp
