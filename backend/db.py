from pymongo import MongoClient
from config import settings


def get_database():
    # Get host and port from settings
    host = settings["MONGO_HOST"]
    port = settings["MONGO_PORT"]

    # Provide the mongodb url to connect python to mongodb using pymongo
    CONNECTION_STRING = f"mongodb://{host}:{port}"

    # Create a connection using MongoClient.
    client = MongoClient(CONNECTION_STRING)

    # Create the database
    return client["elections"]


if __name__ == "__main__":

    # Get the database
    elections = get_database()
    votes = elections["votes"]
    states = elections["states"]
