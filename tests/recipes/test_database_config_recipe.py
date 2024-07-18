from icc.recipes import DatabaseConfigurationRecipe

UNDEFINED_VALUE = "<UNDEFINED>"


def test_database_name_definition(fake_recipe_context):
    db_name = "TESTDB"
    recipe = DatabaseConfigurationRecipe(fake_recipe_context)

    recipe.set_database_name(db_name)

    assert db_name == recipe.database_name


def test_storage_path_definition(fake_recipe_context):
    path = "/test/location"
    recipe = DatabaseConfigurationRecipe(fake_recipe_context)

    recipe.set_storage_path(path)

    assert recipe.storage_path == path


def test_set_database_resource(fake_recipe_context):
    resource_name = "%DB_TEST"

    recipe = DatabaseConfigurationRecipe(fake_recipe_context)
    recipe.set_resource(resource_name)

    assert recipe.resource == resource_name


def test_make_returns_instruction_string(fake_recipe_context):
    recipe = DatabaseConfigurationRecipe(fake_recipe_context)

    recipe.set_database_name("TESTDB")
    recipe.set_resource("%DB_TEST")
    recipe.set_storage_path("/test")

    db_name = recipe.database_name
    status_var = recipe.status_variable_name
    param_list = recipe.parameter_list_name

    instructions = (
        "",
        f'set {param_list}("Resource") = "{recipe.resource}"',
        f'set {param_list}("Name") = "{recipe.database_name}"',
        f'set {param_list}("Directory") = "{recipe.storage_path}"',
        "",
        f'set {status_var} = ##class(Config.Databases).Create("{db_name}", .{param_list})',
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
