from abc import abstractmethod
from flask import request
from flask_restful import Resource
from os import environ

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def require_token(func):
    print("in require token")
    def decorator(*args, **kwargs):
        print("in decorator")
        token = None

        # Check if the website key exists in the headers
        #   and is valid
        if "X-FELLOW-KEY" in request.headers:
            token = request.headers["X-FELLOW-KEY"]
        print(token)
        if token != environ["X_FELLOW_KEY"]:
            return { "success": False, "error": "Missing or invalid API key" }, 403
        return func(*args, **kwargs)
    return decorator

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class BaseAPI(Resource):
    """A base class for all APIs to inherit from
    """

    @abstractmethod
    def get(self, *args, **kwargs): 
        """An abstract method for the GET request on a URL

        Parameters
        ----------
            *args
                A list of arguments to pass through
            **kwargs
                A JSON object of keyword arguments to pass through
        
        Returns
        -------
            dict
                A JSON object of the URL parameters
        """
        return dict(request.args)