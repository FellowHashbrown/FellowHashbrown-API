from .db.game_of_life import DBGameOfLife
from .db.quotes import DBQuotes
from .db.website import DBWebsite

class Database:
    """The Database will contain the data for website downloads,
    and the API endpoints
    """

    def __init__(self):
        self.__game_of_life = DBGameOfLife()
        self.__quotes = DBQuotes()
        self.__website = DBWebsite()
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @property
    def game_of_life(self) -> DBGameOfLife:
        """Returns the Game of Life Database object"""
        return self.__game_of_life
    
    @property
    def quotes(self) -> DBQuotes:
        """Returns the Quotes Database object"""
        return self.__quotes
    
    @property
    def website(self) -> DBWebsite:
        """Returns the Website Database object"""
        return self.__website
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

database = Database()