import os

from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure


load_dotenv()
URI = os.getenv('MONGODB_URI')


# Connect to the MongoDB database
def connect_to_mongo() -> MongoClient:
    try:
        client = MongoClient(URI)
        print("Connected to MongoDB")
        return client
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None


# Close the MongoDB connection
def close_mongo_connection(client: MongoClient) -> None:
    client.close()
    print("MongoDB connection closed")


client = MongoClient(URI)


def get_db():
    db = client.your_database_name
    return db
