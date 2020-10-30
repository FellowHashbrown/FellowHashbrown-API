from api_methods.base_api import BaseAPI

from database.database import database


class RedirectsAPI(BaseAPI):
    """
    """

    def get(self):
        
        # Get the projects and their corresponding redirects
        project_ids = database.website.get_projects()
        projects = [
            database.website.get_project(project)
            for project in project_ids
        ]
        projects = {
            project["id"]: project
            for project in projects
        }
        return { "success": True, "value": projects }, 200
    
    def put(self):
        pass
    
    def post(self):
        pass