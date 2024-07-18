from ..recipe_scope import RecipeScope
from ..stage import Stage
from .base import Recipe


class DatabaseConfigurationRecipe(Recipe):
    def __init__(self, scope: RecipeScope, stage: Stage = Stage.PRE):
        super().__init__(scope, stage)

        self.set_parameter("Resource", "%DB_DEFAULT")

    def set_database_name(self, name: str) -> None:
        """
        Defines the name of the database.
        """
        self.set_parameter("Name", name)

    @property
    def database_name(self) -> str:
        """
        The name of the database.
        """
        return self.get_parameter("Name")

    def set_storage_path(self, path: str) -> None:
        """
        Defines the location path where the related database files should be stored.
        """
        self.set_parameter("Directory", path)

    @property
    def storage_path(self) -> str:
        """
        The location path where the related database files should be stored. Defaults to <UNDEFINED>.
        """
        return self.get_parameter("Directory")

    def set_resource(self, resource: str) -> None:
        """
        Defines the name of the resource that should be assigned to this database.
        """
        self.set_parameter("Resource", resource)

    @property
    def resource(self) -> str:
        """
        The database resource name. Defaults to %DB_DEFAULT.
        """
        return self.get_parameter("Resource", "%DB_DEFAULT")

    def _on_make(self) -> str:
        create_fragment: str = (
            f'##class(Config.Databases).Create("{self.database_name}", .{self.parameter_list_name})'
        )
        return f"set {self.status_variable_name} = {create_fragment}"
