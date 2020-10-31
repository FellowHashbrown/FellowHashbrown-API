from api_methods.base_api import BaseAPI

from database.database import database

class GamesAPI:
    """The Games class holds all APIs that has to do with any games
    or minigames that are created as an API in here
    """

    class GameOfLife(BaseAPI):
        """The Game of Life API returns the data for
        a Game of Life game including house cards,
        career cards, board spaces, etc.
        """
        
        def get(self):
            """Handles the GET request on the GameOfLife API"""
            
            parameters = super().get()
            target = parameters.get("target")

            # Check if target is not specified
            if target is None:
                return { "success": False, "error": "target must be specified" }, 400
            game_of_life = database.game_of_life.get_game_of_life()
            base_json = { "success": True }
            if target == "college":
                base_json.update(data = game_of_life["college_career_cards"]["cards"])
            elif target == "career":
                base_json.update(data = game_of_life["career_cards"]["cards"])
            elif target == "house":
                base_json.update(data = game_of_life["house_cards"]["cards"])
            elif target == "pet":
                base_json.update(data = game_of_life["pet_cards"]["cards"])
            elif target == "action":
                base_json.update(data = game_of_life["action_cards"]["cards"])
            elif target == "board":
                base_json.update(data = game_of_life["board_spaces"]["spaces"])
            elif target == "game_of_life":
                base_json.update(
                    career_cards = game_of_life["career_cards"]["cards"],
                    college_career_cards = game_of_life["college_career_cards"]["cards"],
                    house_cards = game_of_life["house_cards"]["cards"],
                    pet_cards = game_of_life["pet_cards"]["cards"],
                    action_cards = game_of_life["action_cards"]["cards"],
                    board_spaces = game_of_life["board_spaces"]["spaces"]
                )
            else:
                return { "success": False, "error": "Invalid target" }, 404
            return base_json, 200
