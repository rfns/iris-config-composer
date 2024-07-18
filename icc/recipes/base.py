from abc import ABC, abstractmethod
from collections import OrderedDict

from ..recipe_scope import RecipeScope
from ..stage import Stage

type LogPath = str


def get_stage_type_log_file(stage: Stage) -> LogPath:
    match stage:
        case Stage.PRE:
            return "pre-setup.err"
        case Stage.POST:
            return "post-setup.err"
        case _:
            raise ValueError("Invalid timeline type.")


class Recipe(ABC):
    """
    The base class for creating recipes. Contains methods for defining recipe specific parameters
    along with common-usage serialization methods.

    Inheriting classes are supposed to overwrite the method `_on_make` for specific usage.
    """

    def __init__(self, scope: RecipeScope, stage: Stage = Stage.PRE):
        self._scope: RecipeScope = scope
        self._parameters: OrderedDict[str, str] = OrderedDict()
        self._stage: Stage = stage

    @property
    def stage(self) -> Stage:
        """
        Indicates on which stage should this recipe run.
        """
        return self._stage

    def serialize_parameters(self) -> str:
        """
        Serializes a list of configurable parameters as instructions.
        """
        instructions: list[str] = []

        for name, value in self._parameters.items():
            instructions.append(f'set {self.parameter_list_name}("{name}") = "{value}"')

        return "\n".join(instructions)

    def serialize_error_handler(self) -> str:
        """
        Serializes a exception catching mechanism to instruction.
        """
        instructions = [
            f"set errorLog = ##class(%Stream.FileCharacter).%New()",
            f'do errorLog.LinkToFile("/tmp/icc/{get_stage_type_log_file(self.stage)}")',
            "",
            f"if {self.status_variable_name} '= 1",
            "{",
            f"\tdo errorLog.WriteLine($System.Status.GetErrorText({self.status_variable_name}))",
            f"\tdo errorLog.%Save()",
            f'\tset errorLog = ""',
            f"\tdo $System.OBJ.Terminate(, 1)",
            "}",
        ]

        return "\n".join(instructions)

    def set_parameter(self, name: str, value: str) -> None:
        """
        Defines a configurable parameter.
        """
        self._parameters[name] = value

    def get_parameter(self, name: str, default_value: str = "") -> str:
        """
        Returns the value of the parameter name if it exists. Otherwise returns default_value.
        """
        return self._parameters[name] if name in self._parameters else default_value

    @property
    def parameter_list_name(self) -> str:
        """
        Contains the generated name of the parameter container object.
        """
        return self._scope.parameter_list_name

    @property
    def status_variable_name(self) -> str:
        """
        Contains the generated name of the status variable.
        """
        return self._scope.status_variable_name

    def make(self) -> str:
        """
        Expose this recipe instructions.
        """
        instructions = [
            "",
            self.serialize_parameters(),
            "",
            self._on_make(),
            "",
            self.serialize_error_handler(),
        ]
        return "\n".join(instructions)

    def end(self) -> str:
        """
        Prints an instruction that terminates the current session.
        """
        return "halt\n\n"

    @abstractmethod
    def _on_make(self) -> str:
        pass
