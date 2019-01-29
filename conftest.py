import pytest
from bravado.client import SwaggerClient
from bravado.requests_client import RequestsClient
from faker import Faker

from project_config import config
from tools.suppl import get_absolute_path_from_parent_dir
from tools.suppl import load_yaml

# pytest_plugins = "pytest_plugins.parametrizer"


@pytest.fixture
def swagger_spec_file():
    return get_absolute_path_from_parent_dir(config.SWAGGER_YAML_PATH)


@pytest.fixture
def bravado_client(swagger_spec_file):
    http_client = RequestsClient()
    spec = load_yaml(swagger_spec_file)
    client = SwaggerClient.from_spec(
        spec,
        http_client=http_client,
        config={
            'validate_swagger_spec': False,
            # 'validate_requests': False,
        },

    )
    return client


@pytest.fixture
def fake():
    fake = Faker()
    fake.seed(config.FAKER_SEED)
    return fake


@pytest.fixture
def nearbysearch_base_query():
    return dict(
        key=config.API_KEY,
        location='-33.8670522,151.1957362',
        radius=1500,
        # type='restaurant',
        # keyword='cruise'
    )


@pytest.fixture
def nearbysearch_client(bravado_client):
    return bravado_client.GooglePlaces.nearbysearch


@pytest.fixture
def nearbysearch_json_schema(nearbysearch_client):
    return nearbysearch_client.operation.swagger_spec.deref_flattened_spec['definitions']['Nearbysearch']


@pytest.fixture
def nearbysearch_params(nearbysearch_client):
    return nearbysearch_client.operation.params


@pytest.fixture(params=["travel_agency", "restaurant", "food", "establishment"])
def types(request):
    return request.param
