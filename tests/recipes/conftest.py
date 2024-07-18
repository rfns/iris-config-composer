import pytest

class FakeRecipeContext:
    @property
    def status_variable_name(self):
        return "StatusVariable"

    @property
    def parameter_list_name(self):
        return "ParameterVariable"

@pytest.fixture
def fake_recipe_context():
    return FakeRecipeContext()

