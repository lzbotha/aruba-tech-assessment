import time
import os
import logging
import json

from flask import Flask, jsonify
from flask import request
from flask import abort, Response

from aplocation.geolocation import make_geolocation_request

app = Flask(__name__)


def scan_is_valid(scan):
    # TODO check that this scan has all the needed pieces and that they are valid
    return True

def apscan_to_wifiAccessPoint(scan):
    return {
        "macAddress": scan['bssid'],
        "signalStrength": scan['rssi'],
        "age": round(time.time() - scan['timestamp']),
        "channel": eval(scan["channel"]),
    }

def request_body_to_wifiAccessPoints(request_dict):
    
    scans = []

    for scan in request_dict['apscan_data']:
        if scan_is_valid(scan):
            scans.append(apscan_to_wifiAccessPoint(scan))

        else:
            # If a scan is malformed dont include it and try to get the location anyway
            # potentially return with warning?
            # TODO: log a warning / info here
            pass

    if len(scans) < 2:
        # TODO: we need at least 2 to do a geolocation lookup
        raise Exception("TODO fix this")

    return scans

@app.route('/api/v1.0/location', methods=['POST'])
def get_location_from_ap_scans():

    # Get the API key for the geolocation API
    try:
        api_key = os.environ['GEOLOCATION_API_KEY']
    except KeyError:
        logging.error("GEOLOCATION_API_KEY environment variable not set")

        abort(Response(
            status=500, 
            mimetype='application/json',
            response=json.dumps({
                'code': 500,
                'message': 'Server configuration error',
            })
        ))
        

    # TODO: validate the request body
    wifi_access_points = request_body_to_wifiAccessPoints(request.json)

    location_response = make_geolocation_request(wifi_access_points, api_key)

    # Return a 500 if there something went wrong with the lookup
    if 'error' in location_response:
        logging.error(f"Geolocation error {location_response['error']}")

        abort(Response(
            status=500, 
            mimetype='application/json',
            response=json.dumps({
                'code': 500,
                'message': 'Server error',
            })
        ))

    return jsonify(location_response), 200
