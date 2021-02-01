from os import environ
from pymongo import MongoClient

# from database.db.omegapsi.bot import DBOmegaPsiBot
# from database.db.omegapsi.case_numbers import DBOmegaPsiCaseNumbers

class DBOmegaPsi:
    """This class contains methods to modify the Game of Life database"""

    CLIENT = MongoClient(f"mongodb+srv://{environ['DATABASE_USERNAME']}:{environ['DATABASE_PASSWORD']}@fellowhashbrown.orymo.gcp.mongodb.net/omegapsi?retryWrites=true&w=majority")

    def __init__(self):
        self.__bot = DBOmegaPsi.CLIENT.omegapsi["bot"]
        # self.__case_numbers = DBOmegaPsiCaseNumbers(DBOmegaPsi.CLIENT.omegapsi["case_numbers"])
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @property
    def bot(self):
        """Returns the bot object in the database"""
        return self.__bot
    
    @property
    def case_numbers(self):
        """Returns the case numbers object in the database"""
        return self.__case_numbers
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    def get_updates(self):
        """Returns a JSON object of updates from Omega Psi"""
        bot_data = self.bot.find_one({"_id": "bot_information"})
        return bot_data["updates"]
