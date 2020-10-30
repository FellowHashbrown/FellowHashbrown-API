from os import environ
from pymongo import MongoClient

class DBQuotes:

    CLIENT = MongoClient(f"mongodb+srv://{environ['DATABASE_USERNAME']}:{environ['DATABASE_PASSWORD']}@fellowhashbrown.orymo.gcp.mongodb.net/quotes?retryWrites=true&w=majority")

    def __init__(self):
        self.__theOffice = DBQuotes.CLIENT.theOffice
        self.__llamasWithHats = DBQuotes.CLIENT.llamasWithHats
        self.__brooklyn99 = DBQuotes.CLIENT.brooklyn99
        self.__parksAndRec = DBQuotes.CLIENT.parksAndRec
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_office_quotes(self):
        pass
    
    def get_office_quote(self, season: int=None, episode: int=None, author:str=None, *, random: bool=True):
        pass
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_llamas_quotes(self):
        pass
    
    def get_llamas_quote(self, episode: int=None, author: str=None, *, random: bool=True):
        pass
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_brooklyn_99_quotes(self):
        pass
    
    def get_brooklyn_99_quote(self, season: int=None, episode: int=None, author: str=None, *, random: bool=True):
        pass
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_parks_and_rec_quotes(self):
        pass
    
    def get_parks_and_rec_quote(self, season: int=None, episode: int=None, author: str=None, *, random: bool=True):
        pass