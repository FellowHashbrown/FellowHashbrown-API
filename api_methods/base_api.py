from abc import abstractmethod
from flask import request
from flask_restful import Resource

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