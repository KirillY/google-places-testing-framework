import jsonschema
import pytest

from tools.suppl import assert_valid_schema


@pytest.mark.smoke
def test(nearbysearch_client, nearbysearch_base_query):
    r_nearbysearch = nearbysearch_client(**nearbysearch_base_query).response()
    assert r_nearbysearch.metadata.status_code == 200


@pytest.mark.positive
def test_content_type_header(nearbysearch_client, nearbysearch_base_query):
    r_nearbysearch = nearbysearch_client(**nearbysearch_base_query).response()
    assert r_nearbysearch.metadata.status_code == 200
    assert r_nearbysearch.metadata.headers['Content-Type'] == 'application/json; charset=UTF-8'


@pytest.mark.positive
def test_arbitrary_us_city_location(nearbysearch_client, nearbysearch_base_query, nearbysearch_json_schema, fake):
    """Should return at least one result"""
    arbitrary_us_city_location = '{}, {}'.format(*fake.local_latlng(country_code="US"))
    nearbysearch_base_query.update(dict(location=arbitrary_us_city_location))
    r_nearbysearch = nearbysearch_client(**nearbysearch_base_query).response()
    assert r_nearbysearch.metadata.status_code == 200
    nearbysearch_json_schema.update({'required': ['results']})
    assert_valid_schema(instance=r_nearbysearch.result, schema=nearbysearch_json_schema)


@pytest.mark.positive
def test_water_location(nearbysearch_client, nearbysearch_base_query, nearbysearch_json_schema):
    """Should return "results" of length 0"""
    water_location = '29.829652, -76.707609'
    nearbysearch_base_query.update(dict(location=water_location))
    r_nearbysearch = nearbysearch_client(**nearbysearch_base_query).response()
    assert r_nearbysearch.metadata.status_code == 200
    nearbysearch_json_schema['properties']['results'].update({"maxItems": 0})
    assert_valid_schema(instance=r_nearbysearch.result, schema=nearbysearch_json_schema)


@pytest.mark.positive
def test_check_uri_format(nearbysearch_client, nearbysearch_base_query, nearbysearch_json_schema):
    """Should return "icon" property in a valid uri format"""
    r_nearbysearch = nearbysearch_client(**nearbysearch_base_query).response()
    assert r_nearbysearch.metadata.status_code == 200
    nearbysearch_json_schema['properties']['results']['items']['properties']['icon'].update({'format': 'uri'})
    assert_valid_schema(instance=r_nearbysearch.result, schema=nearbysearch_json_schema,
                        format_checker=jsonschema.FormatChecker())


@pytest.mark.positive
def test_check_unique_instances(nearbysearch_client, nearbysearch_base_query, nearbysearch_json_schema):
    """All "results" should be unique"""
    r_nearbysearch = nearbysearch_client(**nearbysearch_base_query).response()
    assert r_nearbysearch.metadata.status_code == 200
    nearbysearch_json_schema['properties']['results'].update({"uniqueItems": True})
    assert_valid_schema(instance=r_nearbysearch.result, schema=nearbysearch_json_schema)


@pytest.mark.positive
def test_check_max_items_per_query(nearbysearch_client, nearbysearch_base_query, nearbysearch_json_schema):
    """Max 20 items per query"""
    r_nearbysearch = nearbysearch_client(**nearbysearch_base_query).response()
    assert r_nearbysearch.metadata.status_code == 200
    nearbysearch_json_schema['properties']['results'].update({"maxItems": 20})
    assert_valid_schema(instance=r_nearbysearch.result, schema=nearbysearch_json_schema)

@pytest.mark.skip
@pytest.mark.positive
def test_max_results_per_session(nearbysearch_client, nearbysearch_base_query, nearbysearch_json_schema, nearbysearch_params):
    """Max 60 items per session"""
    nearbysearch_base_query.update(dict(radius=15000))
    nearbysearch_json_schema['properties']['results'].update({"maxItems": 20})

    r_nearbysearch_1 = nearbysearch_client(**nearbysearch_base_query).response()
    assert_valid_schema(instance=r_nearbysearch_1.result, schema=nearbysearch_json_schema)

    # nearbysearch_params.pop('key')
    nearbysearch_params.pop('location')
    nearbysearch_base_query = {'key': nearbysearch_base_query['key']}
    nearbysearch_base_query.update({"pagetoken": r_nearbysearch_1.result["next_page_token"]})
    r_nearbysearch_2 = nearbysearch_client(**nearbysearch_base_query).response()
    assert_valid_schema(instance=r_nearbysearch_2.result, schema=nearbysearch_json_schema)
    
    # TODO: Failed with {'html_attributions': [], 'results': [], 'status': 'INVALID_REQUEST'} by no reason (key and pagetoken were sent properly)
    
    nearbysearch_base_query = {"pagetoken": r_nearbysearch_2.result["next_page_token"]}
    r_nearbysearch_3 = nearbysearch_client(**nearbysearch_base_query).response()
    assert_valid_schema(instance=r_nearbysearch_3.result, schema=nearbysearch_json_schema)

    assert not r_nearbysearch_3.result.get("next_page_token")


@pytest.mark.positive
def test_types(nearbysearch_client, nearbysearch_base_query, nearbysearch_json_schema, types):
    nearbysearch_base_query.update(dict(type=types))
    r_nearbysearch = nearbysearch_client(**nearbysearch_base_query).response()
    assert r_nearbysearch.metadata.status_code == 200
    assert_valid_schema(instance=r_nearbysearch.result, schema=nearbysearch_json_schema)
