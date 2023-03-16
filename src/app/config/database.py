import os

from pymongo import MongoClient
from pymongo.collection import Collection
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure


load_dotenv()
URI = os.getenv('MONGODB_URI')
client = None


def get_db() -> Collection:
    global client
    if client is None:
        raise ValueError("Database connection not available")
    db = client.get_database('ProjectImagenette2')
    return db


def startup_event() -> None:
    global client
    try:
        client = MongoClient(URI)
        print('Database connection established')
    except ConnectionFailure as e:
        print(f'Could not connect to MongoDB: {e}')


def shutdown_event():
    global client
    client.close()
    print('Database connection closed')


def get_collection(collection: str) -> Collection:
    global client
    if client is None:
        raise ValueError("Database connection not available")
    db = client.get_database('ProjectImagenette2')
    return Collection(db, collection)
