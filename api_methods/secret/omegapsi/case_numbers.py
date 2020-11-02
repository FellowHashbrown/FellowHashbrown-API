from api_methods.base_api import BaseAPI

class CaseNumbers:
    """The CaseNumbers class handles all API methods that have
    to do with getting suggestion, bug, compliment, and insult cases
    """

    # Suggestions
    class Suggestions(BaseAPI):
        """The Suggestions class handles all API methods that have
        to do with creating, viewing, and considering Suggestions

        Viewing and considering suggestions are only methods that
        Omega Psi developers can do
        """

    # Bugs
    class Bugs(BaseAPI):
        """The Bugs class handles all API methods that have
        to do with creating, viewing, and fixing Bugs

        Viewing and fixing bugs are only methods that
        Omega Psi developers can do
        """
        pass

    # Compliments
    class Compliments(BaseAPI):
        """The Compliments class handles all API methods that have
        to do with creating, viewing, confirming, or denying
        compliments

        Viewing, confirming, and denying suggestions are only methods that
        Omega Psi developers can do
        """
        pass

    # Insults
    class Insults(BaseAPI):
        """The Insults class handles all API methods that have
        to do with creating, viewing, confirming, or denying
        insults

        Viewing, confirming, and denying insults are only methods that
        Omega Psi developers can do
        """
        pass