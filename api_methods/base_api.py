from abc import abstractmethod
from flask import request
from flask_restful import Resource
from os import environ

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def require_token(func):
    def decorator(*args, **kwargs):
        token = None

        # Check if the website key exists in the headers
        #   and is valid
        if "X-FELLOW-KEY" in request.headers:
            token = request.headers["X-FELLOW-KEY"]
        if token != environ["X_FELLOW_KEY"]:
            return { "success": False, "error": "Missing or invalid API key" }, 401
        return func(*args, **kwargs)
    return decorator

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class BaseAPI(Resource):
    """A base class for all APIs to inherit from
    """

    @abstractmethod
    def get(self, *args, **kwargs) -> dict: 
        """An abstract method for the GET request on a URL

        :param args: A list of arguments to pass through
        :param kwargs: A JSON object of keyword arguments to pass through
        
        :returns: A JSON object of the URL parameters
        """
        return dict(request.args)
    
    @abstractmethod
    def post(self, *args, **kwargs) -> dict:
        """An abstract method for the POST request on a URL

        :param args: A list of arguments to pass through
        :param kwargs: A JSON object of keyword arguments to pass through
        
        :returns: A JSON object of the POST's JSON
        """
        return dict(request.json)
        pass
    
    @abstractmethod
    def put(self, *args, **kwargs) -> dict:
        """An abstract method for the PUT request on a URL

        :param args: A list of arguments to pass through
        :param kwargs: A JSON object of keyword arguments to pass through
        
        :returns: A JSON object of the PUT's JSON
        """
        return dict(request.json)
