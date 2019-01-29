import json

from genson import SchemaBuilder

from tools.suppl import get_absolute_path_from_parent_dir

TARGET_PATH = 'project_config/swagger_spec/nearbysearch_{}.json'.split('/')
JSON_SAMPLE_PATH = get_absolute_path_from_parent_dir(TARGET_PATH).format('sample')
JSON_SCHEME_PATH = get_absolute_path_from_parent_dir(TARGET_PATH).format('scheme')


def read(json_sample_path):
    with open(json_sample_path) as js:
        return json.load(js)


def build_schema(json_sample):
    builder = SchemaBuilder()
    builder.add_schema({"type": "object", "properties": {}})
    builder.add_object(json_sample)
    return builder.to_schema()


def write(json_scheme_path, json_scheme):
    with open(json_scheme_path, 'w') as outfile:
        json.dump(json_scheme, outfile, indent=2)


if __name__ == "__main__":
    json_sample = read(JSON_SAMPLE_PATH)
    json_scheme = build_schema(json_sample)
    write(JSON_SCHEME_PATH, json_scheme)
