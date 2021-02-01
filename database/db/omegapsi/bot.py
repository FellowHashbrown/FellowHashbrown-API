from datetime import datetime
from uuid import uuid4

from util import set_default, datetime_to_string, datetime_to_dict

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class Bot:
    def __init__(self, bot):
        self.bot = bot

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Information Access Methods
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_bot(self) -> dict:
        """Synchronously retrieves the bot data stored in the database"""

        # Defaults
        data = {
            "_id": "bot_information",
            "developers": ["373317798430244864"],
            "testers": ["373317798430244864"],
            "owner": "373317798430244864",
            "updates": [],
            "pending_update": {},
            "tasks": [],
            "restart": {
                "send": False
            },
            "disabled_commands": [],
            "disabled_cogs": [],
            "notifications": {
                "update": [],
                "new_feature": []
            }
        }

        # Get the bot data from the data base
        bot_data = self.bot.find_one({"_id": "bot_information"})
        if bot_data is None:
            self.set_bot(data, insert=True)
            bot_data = self.get_bot()
        bot_data = set_default(data, bot_data)
        return bot_data

    def set_bot(self, bot_data, *, insert=False):
        """Synchronously updates the bot data stored in the database

        :param bot_data: A JSON object holding information about Omega Psi
        :param insert: Whether to insert or update data in the database
        """
        if insert:
            self.bot.insert_one(bot_data)
        else:
            self.bot.update_one(
                {"_id": "bot_information"},
                {"$set": bot_data},
                upsert=False)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Updates / Pending Update Access Methods
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_updates(self) -> list:
        """Synchronously retrieves a list of updates made to Omega Psi

        :returns: A list of JSON object of updates of the following format:
            {
                "date": ____,
                "version": ____,
                "description": ____,
                "features": [
                    {
                        "feature": ____,
                        "type": ____
                    },
                    ... More Features ...
                ]
            }
        """
        bot_data = self.get_bot()
        return bot_data["updates"]

    def set_updates(self, updates: list):
        """Synchronously sets the list of updates made to Omega Psi

        :param updates: A list of JSON objects for updates made to Omega Psi
        """
        bot_data = self.get_bot()
        bot_data["updates"] = updates
        self.set_bot(bot_data)

    def get_recent_update(self) -> dict:
        """Synchronously retrieves the most recent update made to Omega Psi"""
        updates = self.get_updates()
        return updates[0]

    def get_pending_update(self) -> dict:
        """Synchronously retrieves the pending update being made to Omega Psi"""
        bot_data = self.get_bot()
        return bot_data["pending_update"]

    def set_pending_update(self, pending_update: dict):
        """Synchronously sets the pending update being made to Omega Psi

        :param pending_update: A JSON object of the pending update to set
        """
        bot_data = self.get_bot()
        bot_data["pending_update"] = pending_update
        self.set_bot(bot_data)

    def create_pending_update(self):
        """Synchronously creates a pending update to Omega Psi"""
        if self.get_pending_update() == {}:
            self.set_pending_update({
                "features": {}
            })

    def commit_pending_update(self, version: str, description: str):
        """Synchronously commits and publishes the pending update as an update to Omega Psi

        :param version: The version of the update
        :param description: The description of the update
        """
        updates = self.get_updates()
        features = self.get_pending_update()["features"]
        current_date = datetime_to_string(datetime.now(), short=True)
        updates.insert(0, {
            "date": current_date,
            "version": version,
            "description": description,
            "features": [
                {
                    "feature": features[feature]["feature"],
                    "type": features[feature]["type"]
                }
                for feature in features
            ]
        })
        self.set_updates(updates)
        self.set_pending_update({})

    def add_pending_feature(self, feature: str, feature_type: str) -> dict:
        """Synchronously adds a new pending feature to Omega Psi

        :param feature: The feature to add to the pending update
        :param feature_type: The type of feature that is being added to the pending update
        
        :returns: The JSON object of the created feature that contains the id,
            the feature, the feature type, and the datetime it was added
        """
        pending_update = self.get_pending_update()
        uid = uuid4()
        feature_json = {
            "id": str(uid),
            "feature": feature,
            "type": feature_type,
            "datetime": datetime_to_dict(datetime.now())
        }
        pending_update["features"][str(uid)] = feature_json
        self.set_pending_update(pending_update)
        return feature_json

    def edit_pending_feature(self, feature_id: str, feature: str, feature_type: str) -> [dict, None]:
        """Synchronously edits the feature given in the pending update

        :param feature_id: The ID of the feature to edit
        :param feature: The new feature value
        :param feature_type: he new feature type value
            
        :returns: The JSON object of the resulting edit of the feature
            If None is returned, the feature_id was not found
        """
        pending_update = self.get_pending_update()
        if feature_id in pending_update["features"]:
            pending_update["features"][feature_id].update(
                feature=feature,
                type=feature_type
            )
            self.set_pending_update(pending_update)
            return pending_update["features"][feature_id]
        return None

    def remove_pending_feature(self, feature_id: str) -> [dict, None]:
        """Synchronously removes the feature given from the pending update

        :param feature_id: The ID of the feature to remove
            
        :returns: The JSON object of the removed feature
            If None is returned, the feature_id was not found
        """
        pending_update = self.get_pending_update()
        if feature_id in pending_update["features"]:
            feature_json = pending_update["features"].pop(feature_id)
            self.set_pending_update(pending_update)
            return feature_json
        return None

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Tasks Access Methods
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_tasks(self) -> dict:
        """Synchronously retrieves the task list from the database"""
        bot_data = self.get_bot()
        return bot_data["tasks"]

    def set_tasks(self, tasks: dict):
        """Synchronously sets the task list in the database

        :param tasks: A JSON object for tasks to set in the database
        """
        bot_data = self.get_bot()
        bot_data["tasks"] = tasks
        self.set_bot(bot_data)

    def add_task(self, task: str) -> dict:
        """Synchronously adds a new task to the task list

        :param task: The task to add to the database

        :returns: A JSON object of the task and an ID for the task
        """
        tasks = self.get_tasks()
        uid = uuid4()
        tasks[str(uid)] = task
        self.set_tasks(tasks)
        return {
            "task": task,
            "id": str(uid)
        }

    def edit_task(self, task_id: str, task: str) -> [dict, None]:
        """Synchronously edits a task in the task list

        :param task_id: The ID of the task to edit
        :param task: The new task value
        
        :returns: The resulting task edit
            If None is returned, the task was not found
        """
        tasks = self.get_tasks()
        if task_id in tasks:
            tasks[task_id] = task
            self.set_tasks(tasks)
            return {
                "task": task,
                "id": task_id
            }
        return None

    def remove_task(self, task_id: str) -> [dict, None]:
        """Synchronously removes a task from the task list

        :param task_id: The ID of the task to remove
        
        :returns: The removed task
            If None is returned, the task was not found
        """
        tasks = self.get_tasks()
        if task_id in tasks:
            task = tasks.pop(task_id)
            self.set_tasks(tasks)
            return {
                "task": task,
                "id": task_id
            }
        return None

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Command/Cog Invocation Access Methods
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def is_command_enabled(self, command_name):
        """Synchronously returns whether or not the specified 
        command is enabled

        Parameters
        ----------
            command_name : str
                The name of the command to check if it's enabled
        
        Returns
        -------
            bool
                Whether or not the command is enabled
        """
        bot_data = self.get_bot()
        return command_name not in bot_data["disabled_commands"]

    def enable_command(self, command_name):
        """Synchronously enables the specified command

        Parameters
        ----------
            command_name : str
                The command to enable
        
        Returns
        -------
            bool
                Whether or not the command was enabled
        """
        bot_data = self.get_bot()
        if command_name in bot_data["disabled_commands"]:
            bot_data["disabled_commands"].remove(command_name)
            self.set_bot(bot_data)
            return True
        return False

    def disable_command(self, command_name):
        """Synchronously disables the specified command

        Parameters
        ----------
            command_name : str
                The command to disable
        
        Returns
        -------
            bool
                Whether or not the command was disabled
        """
        bot_data = self.get_bot()
        if command_name not in bot_data["disabled_commands"]:
            bot_data["disabled_commands"].append(command_name)
            self.set_bot(bot_data)
            return True
        return False
    
    # # # # # # # # # # # # # # #

    def get_disabled_cogs(self) -> list:
        """Synchronously returns a list of disabled 
        cogs in the entire bot
        """
        bot_data = self.get_bot()
        return bot_data["disabled_cogs"]        

    def is_cog_enabled(self, cog_name):
        """Synchronously returns whether or not the specified
        cog is enabled

        :param cog_name: The name of the cog to check if it's enabled
        """
        bot_data = self.get_bot()
        return cog_name not in bot_data["disabled_cogs"]    

    def enable_cog(self, cog_name) -> bool:
        """Synchronously enables the specified cog

        :param cog_name: The cog to enable
        :returns: Whether or not the cog was enabled
        """
        bot_data = self.get_bot()
        if cog_name in bot_data["disabled_cogs"]:
            bot_data["disabled_cogs"].remove(cog_name)
            self.set_bot(bot_data)
            return True
        return False    
    
    def disable_cog(self, cog_name):
        """Synchronously disables the specified cog

        :param cog_name: The cog to disable
        :returns: Whether or not the cog was disabled
        """
        bot_data = self.get_bot()
        if cog_name not in bot_data["disabled_cogs"]:
            bot_data["disabled_cogs"].append(cog_name)
            self.set_bot(bot_data)
            return True
        return False

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Notifications Access Methods
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_notifications(self):
        """Synchronously retrieves the notification data for the bot

        Returns
        -------
            dict
                The notification data for the bot
        """
        bot_data = self.get_bot()
        return bot_data["notifications"]

    def set_notification(self, notification_data):
        """Synchronously sets the notification data for the bot

        Parameters
        ----------
            notification_data : dict
                The notification data for the bot
        """
        bot_data = self.get_bot()
        bot_data["notifications"] = notification_data
        self.set_bot(bot_data)

    def manage_notifications(self, target, user: str, add):
        """Synchronously manages notifications in the bot

        Parameters
        ----------
            target : str
                Which notification to manage
            user : str or User
                The user to add or remove from the specified notification
            add : boolean
                Whether or not to add the user to the specified notification
        """
        notification_data = self.get_notifications()
        user = user if isinstance(user, str) else str(user.id)
        if add and user not in notification_data[target]:
            notification_data[target].append(user)
        elif not add and user in notification_data[target]:
            notification_data[target].remove(user)
        self.set_notification(notification_data)
