import string
from random import choices

class RecipeScope:
    """
    Defines a set of random variable names to prevent collision.
    """

    def __init__(self):
        self._config_object_name = self._create_random_name()
        self._parameter_list_name = self._create_random_name()
        self._status_variable_name = self._create_random_name()

    @staticmethod
    def _create_random_name():
        return "".join(choices(string.ascii_lowercase, k=8))

    @property
    def config_name(self):
        """
        Contains the generated name of the config object.
        """
        return self._config_object_name

    @property
    def parameter_list_name(self):
        """
        Contains the generated name of the parameter container object.
        """
        return self._parameter_list_name

    @property
    def status_name(self):
        """
        Contains the generated name of the status variable.
        """
        return self._status_variable_name

def create_recipe_context() -> RecipeScope:
    """
    Returns a new instance of scope.
    """
    return RecipeScope()
