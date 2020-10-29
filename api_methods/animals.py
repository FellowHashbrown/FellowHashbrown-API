import os
from random import choice
from requests import get

from api_methods.base_api import BaseAPI

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class AnimalsAPI(BaseAPI):
    """The Animals API will return pictures of animals specified
    in either baby form, or adult form
    """

    ALBUM_IDS = {
        "penguin": ["2ic7ezG", "e4Ge4Ab"],
        "elephant": ["uy4kzBg"],
        "sloth": ["aXDXaDl"],
        "rabbit": ["rRxNYWu"],
        "dog": ["c7LtiLJ"],
        "cat": ["Ou30pAV"],
        "fox": ["0SMR8Ot"],
        "hedgehog": ["wo7GZPp"],
        "bat": ["k9R4VlT"],
        "squirrel": ["UlZjvly"],
        "hamster": ["K7my2ZB"]
    }

    def get(self):
        parameters = super().get()
        a_type = parameters.get("type")  # The animal type
        baby = parameters.get("baby")

        # Check if the animal type is given
        if a_type:
            a_type = a_type.lower()

            # Check if the animal type is invalid
            if a_type not in AnimalsAPI.ALBUM_IDS:
                return { "success": False, "error": "Invalid animal" }, 400
        
        # No animal type is given, choose a random one
        else:
            a_type = choice(list(AnimalsAPI.ALBUM_IDS.keys()))
        
        # Load the album images through imgur's API
        images = []
        for album in AnimalsAPI.ALBUM_IDS[a_type]:
            images += get(
                "https://api.imgur.com/3/album/{}/images".format(album),
                headers = {
                    "Authorization": "Client-ID {}".format(os.environ["IMGUR_API_KEY"])
                }
            ).json()["data"]
        
        # Choose a random image and return the link
        image = choice(images)
        while baby and image["description"] != "baby":
            image = choice(images)
        baby_animal = image["description"] == "baby"
        link = image["link"]

        return { "success": True, "value": link, "baby_animal": baby_animal }, 200