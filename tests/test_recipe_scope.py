from icc import RecipeScope

def test_recipe_scope_generates_unique_parameter_container_name():
    scope1 = RecipeScope()
    scope2 = RecipeScope()

    assert scope1.parameter_list_name != scope2.parameter_list_name

def test_recipe_scope_generates_unique_status_variable_name():
    scope1 = RecipeScope()
    scope2 = RecipeScope()

    assert scope1.status_variable_name != scope2.status_variable_name
    assert scope1.status_variable_name != scope2.status_variable_name
