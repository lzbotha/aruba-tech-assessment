import os
import requests

url = 'https://www.googleapis.com/geolocation/v1/geolocate'
params = {
    'key': os.environ['GEOLOCATION_API_KEY'],
}


# TODO figure out if there is more information that can be used here
payload = {
    'wifiAccessPoints': [
        {
            'macAddress': '9c:b2:b2:66:c1:be',
        },
        {
            'macAddress': '84:78:ac:b9:76:19',
        },
    ],
}
import json
r = requests.post(
    url=url, 
    params=params,
    json=json.dumps(payload)
)


print(r.url)
print(r.text)