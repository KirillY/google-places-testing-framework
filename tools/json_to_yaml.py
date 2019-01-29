import os
from os import path
import json
import yaml
from tools.suppl import get_absolute_path_from_parent_dir

TARGET_PATH = 'project_config/json_sample/nearbysearch_sample.{}'.split('/')
JSON_PATH = get_absolute_path_from_parent_dir(TARGET_PATH).format('json')
YAML_PATH = get_absolute_path_from_parent_dir(TARGET_PATH).format('yaml')


def load_json(json_path):
    with open(json_path) as js:
        return json.load(js)


def write_yaml(json_string, yaml_path):
    with open(yaml_path, 'w') as yml:
        return yaml.dump(json_string, yml, allow_unicode=True)


if __name__ == "__main__":
    json_string = load_json(JSON_PATH)
    write_yaml(json_string, YAML_PATH)
