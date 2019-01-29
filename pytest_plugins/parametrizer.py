from tools.suppl import load_yaml, get_absolute_path_from_parent_dir

# TODO: it returns some strange fixtures???
def pytest_generate_tests(metafunc):
    module_name = metafunc.module.__name__
    function_name = metafunc.function
    parameter_sets_path = get_absolute_path_from_parent_dir('project_config/parameter_sets/parameter_sets.yaml'.split('/'))
    parameter_sets = load_yaml(parameter_sets_path)
    parameters = parameter_sets[module_name][function_name]
    for fixture in metafunc.fixturenames:
        if fixture in function_name:
            metafunc.parametrize(fixture, parameters)
