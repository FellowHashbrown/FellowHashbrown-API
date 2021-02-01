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
    def get(self):
        """Handles the GET request on the redirects API"""

        parameters = super().get()
        project_id = parameters.get("project_id")
        
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
            database.website.get_project(proj)
            for proj in project_ids
        ]
        projects = {
            proj["id"]: proj
            for proj in projects
        }
        return { "success": True, "value": projects }, 200
    
    @require_token
    def post(self):
        """Handles the POST request on the redirects API
        which creates a new project in the database
        """

        project_id = request.json.get("project_id")
        id = request.json.get("id") if "id" in request.json else project_id
        name = request.json.get("name")

        # Check if the project_id or name was not given
        if project_id is None or name is None:
            return { "success": False, "error": "project_id and name must be given" }, 400

        # Check that no project exists already
        if database.website.get_project(project_id) is not None:
            return { "success": False, "error": "Project already exists" }, 403
        
        result = database.website.add_project(project_id, name, id)
        if result is not None:
            return { "success": True, "error": result["error"] }, 403
        return { "success": True, "value": f"Project {project_id} created" }, 201
    
    @require_token
    def put(self):
        """Handles the PUT request on the redirects API
        which adds a redirect to the specified project
        """
        
        project_id = request.json.get("project_id")
        platform = request.json.get("platform")
        version = request.json.get("version")
        redirect = request.json.get("redirect")

        # Check if any of the values are not given
        if project_id is None or platform is None or version is None or redirect is None:
            return { "success": False, "error": "project_id, platform, version, and redirect must be given" }, 400
        
        # Create the project if necessary
        if database.website.get_project(project_id) is None:
            result = database.website.add_project(project_id)
            if result is not None:
                return { "success": False, "error": result["error"] }, 403
        
        # Add the redirect to the project
        result = database.website.add_redirect(
            project_id, platform,
            version, redirect)
        if "error" in result:
            return { "success": False, "error": result["error"] }, 403
        return { "success": True, "value": f"Redirect added to project {project_id}"}, 201
