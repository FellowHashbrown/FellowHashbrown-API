from os import environ
from pymongo import MongoClient

class DBOmegaPsi:
    """This class contains methods to modify the Game of Life database"""

    CLIENT = MongoClient(f"mongodb+srv://{environ['DATABASE_USERNAME']}:{environ['DATABASE_PASSWORD']}@fellowhashbrown.orymo.gcp.mongodb.net/omegapsi?retryWrites=true&w=majority")

    def __init__(self):
        self.__bot = DBOmegaPsi.CLIENT.omegapsi["bot"]
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @property
    def bot(self):
        """Returns the bot Collection in the database"""
        return self.__bot
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_updates(self):
        """Returns a JSON object of updates from Omega Psi"""
        bot_data = self.bot.find_one({"_id": "bot_information"})
        return bot_data["updates"]
