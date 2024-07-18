from random import choices
from string import ascii_lowercase

def create_unique_name(length: int = 8) -> str:
    return "".join(choices(ascii_lowercase, k=length))

class RecipeScope:
    """
    The class responsible for ensuring that no variable conflict should happens.
    """
    def __init__(self):
        self._parameter_list_name: str = create_unique_name()
        self._status_variable_name: str = create_unique_name()

    @property
    def parameter_list_name(self) -> str:
        """
        The name of the variable holding the parameter list.
        """
        return self._parameter_list_name

    @property
    def status_variable_name(self) -> str:
        """
        The name of the variable holding the status code.
        """
        return self._status_variable_name
