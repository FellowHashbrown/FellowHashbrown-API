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
            simplify = parameters.get("simplify")
            table = parameters.get("table")

            # Check if the expression exists
            if "expression" in parameters:
                return { "success": False, "error": "You need an expression to parse"}, 400
            tree = Tree(parameters["expression"])
            
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

            return { "success": True, "value": True }, 200
