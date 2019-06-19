# TODO: rename this file

import json
import requests

_API_URL = 'https://www.googleapis.com/geolocation/v1/geolocate'


def make_geolocation_request(wifi_access_points, api_key):

    # TODO figure out if there is more information that can be used here
    payload = {
        'wifiAccessPoints': wifi_access_points,
    }

    params = {
        'key': api_key,
    }

    r = requests.post(
        url=_API_URL, 
        params=params,
        json=json.dumps(payload)
    )
    

    return(r.json())