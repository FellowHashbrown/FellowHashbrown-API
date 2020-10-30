from flask_restful import reqparse

from api_methods.base_api import BaseAPI

from .tree import Tree
from .qm import QM

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class LogicAPI:
    """The Logic API will handle all Boolean Expression and 
    Quine-McCluskey functions
    """

    class Parse(BaseAPI):
        """The Parser class is what handles the Boolean Expression
        parsing and evaluating
        """

        def get(self):
            """Gets the result of the Parse API"""

            parameters = super().get()
            expression = parameters.get("expression")
            simplify = parameters.get("simplify", False)
            table = parameters.get("table", False)

            # # # # # 

            # Validate the input
            if expression is None:
                return { "success": False, "error": "You need an expression to parse"}, 400
            if not isinstance(simplify, bool) and simplify.lower() not in ["true", "false"]:
                return { "success": False, "error": "\"simplify\" must be a boolean value"}, 400
            if not isinstance(table, bool) and table.lower() not in ["true", "false"]:
                return { "success": False, "error": "\"table\" must be a boolean value"}, 400
                
            # # # # #

            tree = Tree(expression)
            
            # Check if the user does not want the 
            #   simplified version or a table (Evaluated expression)
            if not simplify and not table:
                return {
                    "success": True,
                    "value": tree.evaluate()
                }, 200
            
            # The user does not want the table (Simplify)
            elif not table:
                return {
                    "success": True,
                    "value": {
                        "minterm": tree.simplify(get_minterm = True),
                        "maxterm": tree.simplify(get_minterm = False),
                        "simplified": tree.simplify(),
                        "functional": tree.functional(),
                        "functional_simplified": tree.simplify().functional()
                    }
                }, 200
            
            # The user does not want to simplify (Table)
            elif not simplify:
                return {
                    "success": True,
                    "value": tree.get_table(as_list = True)
                }, 200
    
    class QuineMcCluskey(BaseAPI):
        """The QuineMcCluskey class is what handles the Quine-McCluskey
        algorithm and all data pertaining to it
        """

        def get(self):
            """Gets the result of the QuineMcCluskey API"""

            parameters = super().get()
            variables = parameters.get("variables")
            values = parameters.get("values")
            dont_cares = parameters.get("dont_cares", "")
            as_maxterm = parameters.get("as_maxterm", False)
        
            # # # # #

            # Validate the input
            if variables is None:
                return { "success": False, "error": "You must specify the variables being used" }, 400
            if values is None:
                return { "success": False, "error": "You must specify the values being used" }, 400
            if not isinstance(as_maxterm, bool) and as_maxterm.lower() not in ["true", "false"]:
                return { "success": False, "error": "\"as_maxterm\" must be a boolean value"}, 400
            
            # # # # #

            variables = variables.split(",")
            values = values.split(",")
            dont_cares = dont_cares.split(",") if len(dont_cares) > 0 else []
            as_maxterm = as_maxterm if isinstance(as_maxterm, bool) else as_maxterm.lower() == "true"

            # Check if the variables are of length 1
            for i in range(len(variables)):
                if len(variables[i]) != 1:
                    return { "success": False, "error": "All variables must be of length 1" }, 400

            # Check if the values and dont_cares are integers
            for i in range(len(values)):
                try:
                    values[i] = int(values[i])
                except ValueError:
                    return { "success": False, "error": "All values must be an integer" }, 400
            
            for i in range(len(dont_cares)):
                try:
                    dont_cares[i] = int(dont_cares[i])
                except ValueError:
                    return { "success": False, "error": "All dont_cares must be an integer" }, 400
            
            # # # # #

            # Everything is valid, execute the algorithm

            qm_result = QM(
                variables, values,
                dont_cares = dont_cares, 
                is_maxterm = as_maxterm
            ).solve()

            return { "success": True, "value": qm_result }, 200
