from api_methods.base_api import BaseAPI

class Games:
    """The Games class holds all APIs that has to do with any games
    or minigames that are created as an API in here
    """

    class GameOfLifeAPI(BaseAPI):
        """The Game of Life API returns the data for
        a Game of Life game including house cards,
        career cards, board spaces, etc.
        """
        
        def get(self):
            
            
            pass