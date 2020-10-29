from flask import Flask, jsonify, render_template
from flask_restful import Api
from json import load
from threading import Thread

from api_methods.animals import AnimalsAPI
from api_methods.morse import MorseAPI
from api_methods.strange_planet import StrangePlanetAPI

# # # # # # # # # # # # # # # # # # # # 

app = Flask("Fellow Hashbrown APIs")
api = Api(app)

# # # # # # # # # # # # # # # # # # # # 

@app.route("/", methods = ["GET"])
def api_page():
    with open("apis.json", "r") as apis_json:
        apis_json = load(apis_json)
    return render_template(
        "index.html",
        apis = apis_json,
        page = {
            'page': 'api',
            "title": "APIs",
            "description": "if you're a developer, you've reached the available APIs that i've written and you know exactly what to do! if you're not a developer, you may not understand this but feel free to try :)"
        },
        template_folder = "."
    )

"""
API.add_resource(api.hangman.HangmanAPI, '/hangman')
API.add_resource(api.scramble.ScrambleAPI, '/scramble')
API.add_resource(api.logic.LogicAPI.Parser, '/logic/parse')
API.add_resource(api.logic.LogicAPI.QuineMcCluskey, '/logic/qm')
API.add_resource(api.profanity.ProfanityAPI, '/profanity')
API.add_resource(api.shows.llamas.LlamasAPI, '/shows/llama')
API.add_resource(api.shows.office.OfficeAPI, '/shows/office')
API.add_resource(api.game_of_life.GameOfLifeAPI, '/gameOfLife')
"""
api.add_resource(AnimalsAPI, '/animals')
api.add_resource(MorseAPI.Encode, '/morse/encode')
api.add_resource(MorseAPI.Decode, '/morse/decode')
api.add_resource(StrangePlanetAPI, '/strangePlanet')

# # # # # # # # # # # # # # # # # # # # 

def run():
    app.run(host = '0.0.0.0', port = 8080)

t = Thread(target = run)
t.start()
