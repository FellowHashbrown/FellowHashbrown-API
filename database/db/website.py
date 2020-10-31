from os import environ

from pymongo import MongoClient

from database.platform import get_datetime
from database.platform import Platform, DIRECT_DOWNLOAD

class DBWebsite:
    """This class contains methods to modify the Website database"""

    CLIENT = MongoClient(f"mongodb+srv://{environ['DATABASE_USERNAME']}:{environ['DATABASE_PASSWORD']}@fellowhashbrown.orymo.gcp.mongodb.net/website?retryWrites=true&w=majority")

    def __init__(self):
        self.__redirects = DBWebsite.CLIENT.website["redirects"]
        self.__users = DBWebsite.CLIENT.website["users"]
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    @property
    def redirects(self):
        """Returns the redirects Collection in the Website database"""
        return self.__redirects
    
    @property
    def users(self):
        """Returns the users Collection in the Website database"""
        return self.__users
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_projects(self) -> list:
        """Returns a list of project IDs"""

        # Get the IDs in the redirect collection
        projects = self.redirects.find({})
        return [
            project["_id"]
            for project in projects
        ]
    
    def get_project(self, mongo_id: str) -> dict:
        """Returns the project specified by the mongo id
        If no project exists, None will be returned

        :param mongo_id: The ID of the project to get
        """
        return self.redirects.find_one({"_id": mongo_id})
    
    def set_project(self, mongo_id: str, project_data: dict):
        """Sets the specified project data to the specified id

        :param mongo_id: The ID of the project to set
        :param project_data: The data to set for the project
        """
        self.redirects.find_one_and_update(
            {"_id": mongo_id},
            {"$set": project_data},
            upsert = False
        )
    
    def add_project(self, mongo_id: str, name: str, id: str=None) -> [dict, None]:
        """Adds a new project to the redirect collection in the Website
        database

        :param mongo_id: The ID of the project to identify in the database
        :param name: The name of the project to make it easier to read
        :param id: An optional ID if you want to specify it differently on the
            website than the given mongo_id
            Note: If this is not specified, it will just be the same as mongo_id
        
        :returns: None, if the project was added or an error JSON object
        """
        
        # Check if a project already exists with the specified mongo_id
        if self.get_project(mongo_id) is not None:
            return { "error": "Project already exists" }
        
        # There is no existing project
        project = {
            "_id": mongo_id,
            "id": id if id is not None else mongo_id,
            "name": name,
            "platforms": {}
        }
        self.redirects.insert_one(project)
        return project
    
    def remove_project(self, mongo_id: str) -> [dict, None]:
        """Removes the project with the specified mongo id

        :param mongo_id: The ID in mongo of the project to remove

        :returns: The project JSON or None, if a project was not found
            with the specified ID
        """
        
        # Check if a project exists by the mongo_id
        project_data = self.redirects.find_one_and_delete({"_id": mongo_id})
        if project_data is None:
            return { "error": "No project was found" }
        return project_data
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    def add_redirect(self, mongo_id: str, platform: str, version: str, redirect: str) -> [dict, None]:
        """Adds a new redirect to the specified project

        :param mongo_id: The ID of the project to add the redirect to
        :param platform: The Platform to set the redirect for
        :param redirect: A Google Drive file ID that points to the file

        :returns: None, if the redirect was added or an error JSON object
        """

        # Check if platform exists
        found = False
        for pform in Platform:
            if platform.lower() == pform.value.lower():
                found = True
                break
        if not found:
            return { "error": "The platform you specified does not exist" }

        # Check if the project exists
        project_data = self.get_project(mongo_id)
        if project_data is None:
            return { "error": "There was no project with the specified ID" }
        
        # Add the platform to the project list if needed
        if platform.value not in project_data["platforms"]:
            project_data["platforms"][platform.value] = []
        
        # Insert the redirect into the top of the platform array
        redirect_data = {
            "version": version,
            "link": DIRECT_DOWNLOAD.format(redirect),
            "release_date": get_datetime()
        }
        project_data["platforms"][platform.value].insert(0, redirect_data)
        self.set_project(mongo_id, project_data)
        return redirect_data
    
    def remove_redirect(self, mongo_id: str, platform: Platform, index: int) -> [dict, None]:
        """Remove the specified redirect at the specified index

        :param mongo_id: The ID of the project to remove the redirect from
        :param platform: The Platform to remove the redirect from
        :param index: The index of the redirect to remove

        :returns: None, if the redirect was removed or an error JSON
        """

        # Check if the project exists
        project_data = self.get_project(mongo_id)
        if project_data is None:
            return { "error": "There was no project with the specified ID" }
        
        # Check if the platform exists
        if platform.value not in project_data["platforms"]:
            return { "error": "The platform you specified does not exist" }
        
        # Remove the redirect if possible
        if index >= len(project_data["platforms"][platform.value]):
            return { "error": "The redirect index you specified does not exist" }
        project_data["platforms"][platform.value].remove(index)
        self.set_project(mongo_id, project_data)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
