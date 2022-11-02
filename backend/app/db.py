from pymongo import MongoClient
from backend.app.config import settings


def get_database():
    """Connects to elections database"""

    # Get host and port from settings
    host = settings["MONGO_HOST"]
    port = settings["MONGO_PORT"]

    # Provide the mongodb url to connect python to mongodb using pymongo
    CONNECTION_STRING = f"mongodb://{host}:{port}"

    # Create a connection using MongoClient.
    client = MongoClient(CONNECTION_STRING)

    # Create the database
    return client["elections"]
