from enum import Enum


class Stage(Enum):
    PRE = "pre"
    """
    Indicates that the recipe should be executed on build stage.
    """

    POST = "post"
    """
    Indicates that the recipe should be executed on run stage.
    """

    def __str__(self):
        return self.value
