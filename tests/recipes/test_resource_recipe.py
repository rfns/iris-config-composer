from icc.recipes import ResourceRecipe
from icc.recipes.resource import ResourcePermission

UNDEFINED_VALUE = "<UNDEFINED>"


def test_database_resource_name_definition(fake_recipe_context):
    recipe = ResourceRecipe(fake_recipe_context)
    resource_name = "%DB_TEST"

    recipe.set_resource_name("%DB_TEST")

    assert resource_name == recipe.resource_name


def test_resource_permission_definition(fake_recipe_context):
    permission = ResourcePermission.READWRITE
    recipe = ResourceRecipe(fake_recipe_context)

    recipe.set_permission(permission)

    assert recipe.permission == permission


def test_resource_permission_defaults_to_rwu(fake_recipe_context):
    default_permission = ResourcePermission.READWRITEUSE
    recipe = ResourceRecipe(fake_recipe_context)

    assert recipe.permission == default_permission


def test_resource_description_definition(fake_recipe_context):
    description = "A test resource"
    recipe = ResourceRecipe(fake_recipe_context)

    recipe.set_description(description)

    assert recipe.description == description


def test_make_returns_instruction_string(fake_recipe_context):
    recipe = ResourceRecipe(fake_recipe_context)

    recipe.set_resource_name("%DB_TESTDB")
    recipe.set_permission(ResourcePermission.READWRITE)
    recipe.set_description("A description for this test resource.")

    resource_name = recipe.resource_name
    status_var = recipe.status_variable_name
    param_list = recipe.parameter_list_name

    instructions = (
        "",
        f'set {param_list}("PublicPermission") = "{recipe.permission}"',
        f'set {param_list}("Name") = "{resource_name}"',
        f'set {param_list}("Description") = "{recipe.description}"',
        "",
        f"set {status_var} = ##class(Security.Resources).CreateOne(.{recipe.parameter_list_name})",
        "",
        "set errorLog = ##class(%Stream.FileCharacter).%New()",
        'do errorLog.LinkToFile("/tmp/icc/pre-setup.err")',
        "",
        f"if {status_var} '= 1",
        "{",
        f"\tdo errorLog.WriteLine($System.Status.GetErrorText({status_var}))",
        f"\tdo errorLog.%Save()",
        f'\tset errorLog = ""',
        f"\tdo $System.OBJ.Terminate(, 1)",
        "}",
    )

    assert recipe.make() == "\n".join(instructions)
