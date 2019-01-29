import googlemaps
from googlemaps import places

from tools.json_to_yaml import write_yaml

gmaps = googlemaps.Client(key='AIzaSyCWOSz0D-dfNnfv7FJh6pP3dghHM9NmyuQ')
" https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=1500&type=restaurant&keyword=cruise&key=AIzaSyCWOSz0D-dfNnfv7FJh6pP3dghHM9NmyuQ"

# Geocoding an address
geocode_result = places.places_nearby(gmaps, location='-33.8670522,151.1957362', radius=1500, type='restaurant',
                                      keyword='cruise')
write_yaml(geocode_result, 'nearbysearch_result.yaml')
