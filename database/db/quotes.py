from os import environ
from pymongo import MongoClient

class DBQuotes:
    """
    """

    CLIENT = MongoClient(f"mongodb+srv://{environ['DATABASE_USERNAME']}:{environ['DATABASE_PASSWORD']}@fellowhashbrown.orymo.gcp.mongodb.net/quotes?retryWrites=true&w=majority")

    def __init__(self):
        pass