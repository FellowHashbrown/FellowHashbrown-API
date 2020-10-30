from os import environ
from flask import request

from api_methods.base_api import BaseAPI, require_token

from database.database import database

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class RedirectsAPI(BaseAPI):
    """Handles all the API requests with a project or a
    redirect to that project

    All the methods in this API require a token
    """

    @require_token
    def get(self, project_id: str=None):
        """Handles the GET request on the redirects API

        :param project_id: A specific project to retrieve
            If None is specified, will return all projects
            as a JSON object
        """
        
        # Get the projects and their corresponding redirects
        project_ids = database.website.get_projects()

        # Check if a specific project is requested
        if project_id is not None:
            if project_id not in project_ids:
                return { "success": False, "error": "Invalid project ID" }, 404
            return { "success": True, "value": database.website.get_project(project_id) }, 200
        
        # Load all projects into a list and then into a dictionary
        #   and return all the projects
        projects = [
            database.website.get_project(project_id)
            for proj in project_ids
        ]
        projects = {
            proj["id"]: proj
            for proj in projects
        }
        return { "success": True, "value": projects }, 200
    
    @require_token
    def post(self, project_id: str=None):
        """Handles the POST request on the redirects API
        which creates a new project in the database

        :param project_id: The ID to store the project as
        """

        

        # Check that no project exists already
        if database.website.get_project(project_id) is not None:
            return { "success": False, "error": "Project already exists" }, 403
        
        database.website.add_project
        pass
    
    @require_token
    def put(self, project_id: str=None):
        """Handles the PUT request on the redirects API
        which adds a redirect to the specified project

        :param project_id: The project to add the redirect to
        """
        pass