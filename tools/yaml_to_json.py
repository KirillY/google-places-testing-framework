import json
import sys
from collections import OrderedDict
from collections.abc import Mapping, Sequence

import ruamel.yaml
from ruamel.yaml.error import YAMLError

from tools.suppl import get_absolute_path_from_parent_dir

yaml = ruamel.yaml.YAML()
yaml.indent(sequence=4, offset=2)

TARGET_PATH = 'project_config/json_scheme/nearbysearch_scheme.{}'.split('/')
YAML_PATH = get_absolute_path_from_parent_dir(TARGET_PATH).format('yaml')
JSON_PATH = get_absolute_path_from_parent_dir(TARGET_PATH).format('json')


class OrderlyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Mapping):
            return OrderedDict(o)
        elif isinstance(o, Sequence):
            return list(o)
        return json.JSONEncoder.default(self, o)


def yaml_2_json(in_file, out_file):
    with open(in_file, 'r') as stream:
        try:
            yaml_datamap = yaml.load(stream)
            json_datamap = OrderlyJSONEncoder(indent=2).encode(yaml_datamap)
            with open(out_file, 'w') as output:
                output.write(json_datamap)
        except YAMLError as exc:
            print(exc)
            return False
    return True


if __name__ == "__main__":
    yaml_2_json(YAML_PATH, JSON_PATH)
    with open(JSON_PATH) as fp:
        sys.stdout.write(fp.read())
