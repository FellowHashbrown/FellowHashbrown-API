from os import environ
from pymongo import MongoClient

class DBGameOfLife:
    """This class contains methods to modify the Game of Life database"""

    CLIENT = MongoClient(f"mongodb+srv://{environ['DATABASE_USERNAME']}:{environ['DATABASE_PASSWORD']}@fellowhashbrown.orymo.gcp.mongodb.net/game_of_life?retryWrites=true&w=majority")

    def __init__(self):
        self.__game_of_life = DBGameOfLife.CLIENT.gameoflife["game_of_life"]
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @property
    def game_of_life(self):
        """Returns the game of life Collection in the database"""
        return self.__game_of_life
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_game_of_life(self):
        """Returns all the data in the Game of Life
        from the database
        """
        
        # Find all documents and return them
        return {
            doc["_id"]: doc
            for doc in self.game_of_life.find()
        }
