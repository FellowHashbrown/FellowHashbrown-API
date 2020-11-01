from os import environ
from random import randint, choice

from pymongo import MongoClient


class DBQuotes:
    """This class contains methods to modify the Quotes database"""

    CLIENT = MongoClient(f"mongodb+srv://{environ['DATABASE_USERNAME']}:{environ['DATABASE_PASSWORD']}@fellowhashbrown.orymo.gcp.mongodb.net/quotes?retryWrites=true&w=majority")

    def __init__(self):
        self.__the_office = DBQuotes.CLIENT.quotes["theOffice"]
        self.__llamas_with_hats = DBQuotes.CLIENT.quotes["llamasWithHats"]
        self.__brooklyn_99 = DBQuotes.CLIENT.quotes["brooklyn99"]
        self.__parks_and_rec = DBQuotes.CLIENT.quotes["parksAndRec"]
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @property
    def the_office(self):
        return self.__the_office
    
    @property
    def llamas_with_hats(self):
        return self.__llamas_with_hats
    
    @property
    def brooklyn_99(self):
        return self.__brooklyn_99
    
    @property
    def parks_and_rec(self):
        return self.__parks_and_rec

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_office_quotes(self):
        """Returns all the office quotes in the database"""
        return {
            doc["_id"]: doc
            for doc in self.the_office.find()
        }
    
    def get_office_quote(self, season: int=None, episode: int=None, is_deleted=False):
        """Returns an office quote from a specific season, episode, and author"""
        quotes = self.get_office_quotes()

        # Get a random season and episode
        if season is None and episode is None:
            season = randint(1, len(quotes))
            episode = randint(1, len(quotes[f"season{season}"]["episodes"]))
        elif episode is None:
            if not(1 <= season <= 9):
                return { "error": "Invalid season" }
            episode = randint(1, len(quotes[f"season{season}"]))
        elif season is None:
            return { "error": "Cannot get random episode from unspecified season" }
        
        # Validate the season and episode
        if not(1 <= season <= 9):
            return { "error": "Invalid season" }
        if not(1 <= episode <= len(quotes[f"season{season}"]["episodes"])):
            return { "error": "Invalid episode" }
        quotes = quotes[f"season{season}"]["episodes"][episode - 1]["quotes"]
        
        # Search through the quotes given a specific filter of author and is_deleted
        filtered_quotes = []
        for quote in quotes:
            if is_deleted is None or is_deleted == quote["deleted"]:
                filtered_quotes.append(quote)
        return choice(filtered_quotes)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_llamas_quotes(self):
        """Returns all the llamas with hates quotes in the database"""
        return {
            doc["_id"]: doc
            for doc in self.llamas_with_hats.find()
        }
    
    def get_llamas_quote(self, episode: int=None, author: str=None):
        """Returns a llamas with hats quote from a specific episode and author"""
        quotes = self.get_llamas_quotes()

        # Get a random episode
        #   or validate the episode
        if episode is None:
            episode = randint(1, len(quotes))
        if not(1 <= episode <= len(quotes)):
            return { "error": "Invalid episode" }
        quotes = quotes[f"episode{episode}"]["quotes"]
        
        # Search through the quotes given a specific filter of author
        filtered_quotes = []
        for quote in quotes:
            if author is None or quote["author"].lower() == author.lower:
                filtered_quotes.append(quote)
        return choice(filtered_quotes)

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