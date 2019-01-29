from bravado.requests_client import RequestsClient
from bravado.client import SwaggerClient
from google_places_api_problem.tools.json_to_yaml import load_json

config = {
    # Validate the swagger spec
    'validate_swagger_spec': False,
}

http_client = RequestsClient()
# http_client.set_api_key(
#     'https://api18.centaurportal.com/v1.1.4/', 'MTYtYjAyNC0yNDE2MjVmODljYjg=',
#     param_name='api_key', param_in='header'
# )

spec = load_json('../swagger/eapi_taras_replaced_error.json')

client = SwaggerClient.from_spec(
    spec,
    http_client=http_client,
    config=config,
)

r_locations = client.INFO.locationsGetUsingGET(
    _request_options={"headers": {"api_key": "MTYtYjAyNC0yNDE2MjVmODljYjg="}}).response()
print()