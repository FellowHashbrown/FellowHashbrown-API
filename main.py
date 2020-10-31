from flask import Flask, render_template
from flask_restful import Api
from json import load, dumps
from random import randint
from threading import Thread

from api_methods.animals import AnimalsAPI
from api_methods.morse import MorseAPI
from api_methods.strange_planet import StrangePlanetAPI
from api_methods.logic.logic import LogicAPI

from api_methods.games.games import GamesAPI
# from api_methods.quotes.quotes import QuotesAPI

from api_methods.secret.redirects import RedirectsAPI

# # # # # # # # # # # # # # # # # # # # 

app = Flask("Fellow Hashbrown APIs")
api = Api(app)

# # # # # # # # # # # # # # # # # # # # 

@app.route("/")
def home():

    # Load the API data
    with open("apis.json", "r") as api_json:
        apis_json = load(api_json)
    
    # Convert the response JSONs to a string formatted
    #   in json style
    for api in apis_json:
        for request in api["requests"]:
            for response in request["responses"]:
                response["response"] = dumps(
                    response["response"],
                    indent = "&nbsp;&nbsp;").replace(
                        "\n", "<br>")
    
    return render_template(
        "api.html",
        apis = apis_json,
        page = {
            "page": "api",
            "title": "APIs",
            "description": "if you're a developer, you've reached the available APIs that i've written and you know exactly what to do! if you're not a developer, you may not understand this but feel free to try :)"
        }
    ), 200

"""
API.add_resource(api.hangman.HangmanAPI, '/hangman')
API.add_resource(api.scramble.ScrambleAPI, '/scramble')
API.add_resource(api.profanity.ProfanityAPI, '/profanity')
API.add_resource(api.game_of_life.GameOfLifeAPI, '/gameOfLife')
"""

api.add_resource(AnimalsAPI, '/animals')
api.add_resource(MorseAPI.Encode, '/morse/encode')
api.add_resource(MorseAPI.Decode, '/morse/decode')
api.add_resource(StrangePlanetAPI, '/strangePlanet')

api.add_resource(GamesAPI.GameOfLife, '/games/gameOfLife')

# API.add_resource(api.shows.llamas.LlamasAPI, '/shows/llama')
# API.add_resource(api.shows.office.OfficeAPI, '/shows/office')

api.add_resource(LogicAPI.Parse, '/logic/parse')
api.add_resource(LogicAPI.QuineMcCluskey, '/logic/qm')

api.add_resource(RedirectsAPI, '/redirects')

# # # # # # # # # # # # # # # # # # # # 

def run():
    app.run(
        host = '0.0.0.0', 
        port = randint(1000, 9999))

t = Thread(target = run)
t.start()
