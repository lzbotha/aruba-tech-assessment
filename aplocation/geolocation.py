import json
import requests

_API_URL = 'https://www.googleapis.com/geolocation/v1/geolocate'

import logging
logger = logging.getLogger(__name__)


def make_geolocation_request(wifi_access_points, api_key):
    """
    Makes an HTTP POST request to the Google's Geolocation service using a given 
    list of wifi access points and an api_key.

    Args:
        wifi_access_points:     list of dictionaries containing access points
        api_key:                string the API key
    
    Returns:
        dictionary containing the response from the Geolocation API. Note this response 
        may be an error.
    """

    payload = {
        'considerIp': 'false', # this avoids defaulting to something stupid
        'wifiAccessPoints': wifi_access_points,
    }

    params = {
        'key': api_key,
    }

    r = requests.post(
        url=_API_URL, 
        params=params,
        json=payload
    )
    
    return(r.json())