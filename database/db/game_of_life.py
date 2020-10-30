from os import environ
from pymongo import MongoClient

class DBGameOfLife:
    """
    """

    CLIENT = MongoClient(f"mongodb+srv://{environ['DATABASE_USERNAME']}:{environ['DATABASE_PASSWORD']}@fellowhashbrown.orymo.gcp.mongodb.net/game_of_life?retryWrites=true&w=majority")

    def __init__(self):
        pass
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_game_of_life(self, target: str=None):
        pass
    