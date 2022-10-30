from pymongo import MongoClient


def get_database():

    # Provide the mongodb url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://mongo:27017"

    # Create a connection using MongoClient.
    client = MongoClient(CONNECTION_STRING)

    # Create the database
    return client["elections"]


if __name__ == "__main__":

    # Get the database
    elections = get_database()
    votes = elections["votes"]
    states = elections["states"]
