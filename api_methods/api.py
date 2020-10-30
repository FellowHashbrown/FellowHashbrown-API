from json import load

from flask import render_template

from api_methods.base_api import BaseAPI

class Home(BaseAPI):
    def get(self):
        with open("apis.json", "r") as api_json:
            apis_json = load(api_json)
        return render_template(
            "api.html",
            apis = apis_json,
            page = {
                "page": "api",
                "title": "APIs",
                "description": "if you're a developer, you've reached the available APIs that i've written and you know exactly what to do! if you're not a developer, you may not understand this but feel free to try :)"
            }
        ), 200