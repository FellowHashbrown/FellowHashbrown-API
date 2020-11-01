from random import randint, choice

from api_methods.base_api import BaseAPI

from database.database import database

class QuotesAPI:
    """The QuotesAPI class handles the Llamas quotes and 
    The Office quotes
    """

    class Llamas(BaseAPI):
        """The Llamas class will handle the Llamas with Hats API"""

        def get(self):

            parameters = super().get()
            episode = parameters.get("episode")
            author = parameters.get("author")
            full_script = parameters.get("fullScript", False)

            # Get the llamas quotes
            quotes = database.quotes.get_llamas_quotes()

            # Check if the episode is a valid episode
            no_full_script = False
            if episode is not None:
                try:
                    episode = int(episode)
                    if not (1 <= episode <= len(quotes)):
                        raise ValueError()
                except ValueError:
                    return { "success": False, "error": "episode must be a number between 1 and 12" }, 404
            else:
                no_full_script = True
                episode = randint(1, len(quotes))
            
            # Check if the user is getting the full script
            if full_script is not None and not isinstance(full_script, bool):
                if full_script.lower() in ["true", "false"]:
                    full_script = full_script.lower() == "true"  
                else:
                    return { "success": False, "error": "fullScript must either be true or false" }, 400
            
            # Find a quote with any specified filters if the user
            #   is not getting the full script (which requires an episode)
            if not full_script:
                filtered_quotes = []
                for quote in quotes[f"episode{episode}"]["quotes"]:
                    if author is None or quote["author"].lower() == author.lower():
                        filtered_quotes.append(quote)
                random_quote = choice(filtered_quotes)
                random_quote.update(
                    success = True
                )
                return random_quote, 200
            
            # Getting the full script of an episode
            if no_full_script:
                return { "success": False, "error": "An episode must be specified to get the full script" }, 200
            episode_data = quotes[f"episode{episode}"]
            episode_data.pop("_id")
            episode_data.update(
                success = True
            )
            return episode_data, 200
    
    class TheOffice(BaseAPI):
        """The Office class will handle the Office API"""

        def get(self):
            return { "success": False, "error": "Not implemented yet" }, 404