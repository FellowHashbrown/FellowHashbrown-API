import os, json
from random import choice
from requests import get

from api_methods.base_api import BaseAPI

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class StrangePlanetAPI(BaseAPI):

    COMICS = [
        "rO257PZ", "qFEaKXi", "MPaZP2H",
        "Fgbb7aP", "7bn5zvn", "M21Sl7D",
        "zB2u0yd", "nVctvn6"
    ]

    REACTIONS = [
        "AUnUXjQ", "Wcu3v9l", "gBozqSM"
    ]

    IGNORE_TAGS = [
        "a", "an", "the", "we", "i", "us"
    ]

    def get_all(self, target = "all"):
        images = []

        # Iterate through the specified list
        target_list = StrangePlanetAPI.COMICS
        if target == "all":
            target_list += StrangePlanetAPI.REACTIONS
        elif target == "reactions":
            target_list = StrangePlanetAPI.REACTIONS

        for album in StrangePlanetAPI.COMICS:
            new_images = get(
                "https://api.imgur.com/3/album/{}/images".format(album),
                headers = {
                    "Authorization": "Client-ID {}".format(os.environ["IMGUR_API_KEY"])
                }
            ).json()["data"]

            for image in new_images:
                image["is_comic_reaction"] = album in StrangePlanetAPI.REACTIONS
        images += new_images
        return images

    def get(self):
        parameters = super().get()

        keywords = parameters.get("keywords")
        number = parameters.get("number")

        recent = parameters.get("recent", False)
        random = parameters.get("random", False)

        target = parameters.get("target", "comics").lower()
        limit = parameters.get("limit", 1)

        # Validate the parameters
        images = self.get_all(target if (not recent and not random) else "comics")
        try:
            limit = int(limit)
            if limit <= 0 and limit != -1:
                raise TypeError()
        except TypeError:
            return { "success": False, "error": "Limit must be a number greater than 0" }, 400
        if not isinstance(recent, bool) and recent.lower() not in ["true", "false", "t", "f"]:
            return { "success": False, "error": "\"recent\" parameter must be boolean value" }, 400
        else:
            recent = False
        if not isinstance(random, bool) and random.lower() not in ["true", "false", "t", "f"]:
            return { "success": False, "error": "\"random\" parameter must be boolean value" }, 400
        else:
            random = False
        if target not in ["all", "comics", "reactions"]:
            return { "success": False, "error": "target must be \"comics\", \"reactions\", or \"all\"" }, 400
        if number is not None:
            try:
                number = int(number)
                if number <= 0 or number >= len(images):
                    raise TypeError()
            except:
                return { "success": False, "error": "Invalid comic number" }, 400

        # Get a searched comic or reaction
        if keywords:
            new_keywords = ""
            for c in keywords:
                if c == "-":
                    new_keywords += " "
                elif c.isalnum() or c == " ":
                    new_keywords += c
            keywords = new_keywords.strip()
            keywords_split = keywords.split()

            # Keep track of keywords results
            results = []
            for image in images:

                # Get the description of the comic to pull out the tags
                if image["description"]:
                    description = json.loads(image["description"])
                    title = description["title"]
                    tags = description["tags"]
                    number = description["number"]
                    
                    # Iterate through the keywords and check to see if they exist in the tags of the comics
                    match_level = 0
                    match_streak = 1
                    for keyword in keywords_split:
                        if keyword in tags and keyword not in StrangePlanetAPI.IGNORE_TAGS and len(keyword) >= 5:
                            match_level += match_streak
                            match_streak += 1
                        else:
                            match_streak = 1
                    
                    # Don't set the comic data if there were no matching keywords
                    if match_level != 0:
                        comic_data = {
                            "match_level": match_level,
                            "link": image["link"]
                        }
                        results.append(comic_data)
            
            # Sort the results by the match level and remove the key from each comic
            results = sorted(results, reverse = True, key = lambda comic: comic["match_level"])
            if limit != -1:
                results = results[ : limit]
            results = [ comic["link"] for comic in results ]
            return { "success": True, "data": results }, 200
        
        # Get a random or recent comic
        else:
            if recent:
                return { "success": True, "data": images[-1]["link"] }, 200
            return { "success": True, "data": choice(images)["link"] }, 200
