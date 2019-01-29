import os
from os import path
from jsonschema import validate
from ruamel.yaml import YAML


def get_absolute_path_from_parent_dir(relative_path):
    return path.join(path.dirname(os.getcwd()), *relative_path)


def load_yaml(file_path):
    """
    converts YAML document to a Python object
    :param file_path: yaml file path
    :return: a python object
    """
    ruamel_yaml = YAML()
    try:
        with open(file_path, 'r', encoding="utf-8") as stream:
            return ruamel_yaml.load(stream)
    except FileNotFoundError:
        return {'Error message': 'File {} not found'.format(file_path)}


def assert_valid_schema(instance, schema, **kwargs):
    """ Checks whether the given data matches the schema """
    return validate(instance, schema, **kwargs)
