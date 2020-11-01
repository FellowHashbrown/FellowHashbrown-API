from flask import request

from api_methods.base_api import BaseAPI, require_token

from database.database import database

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class OmegaPsiAPI(BaseAPI):
    """Handles all the API requests with Omega Psi

    All the methods in this API require a token except
    the GET method
    """

    def get(self):
        """Handles the GET request on the Omega Psi API"""

        updates = database.omegapsi.get_updates()
        return updates
