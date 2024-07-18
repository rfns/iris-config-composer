from enum import Enum


class Stage(Enum):
    """
    Indicates that the recipe should be executed on build stage.
    """

    PRE = "pre"
    """
    Indicates that the recipe should be executed on run stage.
    """
    POST = "post"

    def __str__(self):
        return self.value
