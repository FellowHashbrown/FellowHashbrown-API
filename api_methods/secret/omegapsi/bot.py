from api_methods.base_api import BaseAPI

class Bot:
    """The Bot class handles all API methods having to do with
    modifying Omega Psi's bot information such as updates,
    disabled commands and cogs, tasks, and notifications
    """

    class Update(BaseAPI):
        """The Update class handles all API methods having to do
        with updates or pending updates being made to Omega Psi
        """

        class Feature(BaseAPI):
            """The Feature class handles all API methods having to do with
            features being made in a pending update for Omega Psi
            """
            
            def post(self):
                """The POST method is able to handle creating a new feature in a pending
                update of Omega Psi
                """
                pass
            
            def put(self):
                """The PUT method is able to handle editing a feature in a pending
                update of Omega Psi
                """
                pass
            
            def delete(self):
                """The DELETE method is able to handle removing a feature in a pending
                update of Omega Psi
                """
                pass

        def get(self):
            """The GET method is able to handle getting the pending update,
            retrieving a specific update, or all updates
            """
            pass
        
        def post(self):
            """The POST method is able to handle creating a pending update"""
            pass
        
        def put(self):
            """The PUT method is able to handle making a pending update
            a new update to Omega Psi
            """
            pass

    class Commands(BaseAPI):
        """The Commands class handles all API methods having to do
        with disabled commands in Omega Psi
        """

        def get(self):
            """The GET method is able to handle retrieving a list
            of disabled commands in Omega Psi
            """
            pass
        
        def post(self):
            """The POST method is able to handle adding a command
            to the list of disabled commands
            """
            pass
        
        def delete(self):
            """The DELETE method is able to handle removing a command
            from the list of disabled commands
            """
            pass
    
    class Cogs(BaseAPI):
        """The Cogs class handles all API methods having to do
        with disabled cogs in Omega Psi
        """

        def get(self):
            """The GET method is able to handle retrieving a list
            of disabled cogs in Omega Psi
            """
            pass
        
        def post(self):
            """The POST method is able to handle adding a cog
            to the list of disabled cogs
            """
            pass
        
        def delete(self):
            """The DELETE method is able to handle removing a cog
            from the list of disabled cogs
            """
            pass

    class Tasks(BaseAPI):
        """The Tasks class handles all API methods that have to do
        with adding, editing, or removing tasks from the developer
        task list
        """

        def get(self):
            """The GET method is able to handle retrieving a list
            of tasks that developers have added to the tasklist
            """
            pass
        
        def post(self):
            """The POST method is able to handle adding a task to 
            the tasklist
            """
            pass
        
        def put(self):
            """The PUT method is able to handle editing a task that
            is in the tasklist
            """
            pass
        
        def delete(self):
            """The DELETE method is able to handle removing a task from
            the tasklist
            """
            pass

    class Notifications(BaseAPI):
        """The Notifications class handles all API methods that have
        to do with setting the data that concerns who gets sent
        notifications and which ones they get sent
        """

        def get(self):
            """The GET method is able to handle getting the list of users
            who retrieve specific notifications
            """
            pass
        
        def post(self):
            """The POST method is able to handle adding a user to a specific
            notification list
            """
            pass
        
        def delete(self):
            """The DELETE method is able to handle removing a user from
            a specific notification list
            """
            pass