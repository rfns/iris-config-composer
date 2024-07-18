from enum import Enum

from ..recipe_scope import RecipeScope
from ..stage import Stage
from .base import Recipe


class ResourcePermission(Enum):
    READ = "R"
    WRITE = "W"
    USE = "U"
    READWRITE = "RW"
    READUSE = "RU"
    READWRITEUSE = "RWU"
    WRITEUSE = "WU"

    def __str__(self):
        return self.value


class ResourceRecipe(Recipe):
    """
    The recipe class for generating a resource.
    """

    def __init__(self, scope: RecipeScope, stage: Stage = Stage.PRE):
        super().__init__(scope, stage)

        self.set_permission(ResourcePermission.READWRITEUSE)

    def set_resource_name(self, name: str) -> None:
        """
        Defines the resource name to be created.
        """
        self.set_parameter("Name", name)

    @property
    def resource_name(self) -> str:
        """
        The name of this resource.
        """
        return self.get_parameter("Name")

    def set_permission(self, permission: ResourcePermission) -> None:
        """
        Defines a set of permissions for this resource.
        """
        self.set_parameter("PublicPermission", str(permission))

    @property
    def permission(self) -> ResourcePermission:
        """
        The permission set for this resource.
        """
        return ResourcePermission(self.get_parameter("PublicPermission", "RW"))

    def set_description(self, description: str) -> None:
        """
        Defines the description for this resource.
        """
        self.set_parameter("Description", description)

    @property
    def description(self) -> str:
        """
        A description for this resource.
        """
        return self.get_parameter("Description")

    def _on_make(self) -> str:
        return f"set {self.status_variable_name} = ##class(Security.Resources).CreateOne(.{self.parameter_list_name})"
