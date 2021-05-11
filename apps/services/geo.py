import geopy.distance
import requests
from settings import HEREAPI_API_KEY, HEREAPI_REVERSE_URL


def calculate_distance(point1, point2):
    return round(geopy.distance.distance(point1, point2).meters, 1)


def get_address(lat, lon):
    url = f'{HEREAPI_REVERSE_URL}?at={lat},{lon}&apikey={HEREAPI_API_KEY}'
    resp = requests.get(url)
    if resp.status_code == 200:
        items = resp.json().get('items')
        if items:
            address = items[0].get('address')
            if address:
                return address.get('label')
