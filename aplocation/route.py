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
    """
    Check if an input scan dictionary is valid / can be converted to the Geolocation
    format.

    Args:
        scan: apscan dictionary

    Returns:
        bool true if valid false otherwise
    """

    # TODO check that this scan has all the needed pieces and that they are valid
    if 'bssid' not in scan: # macAddress is the only compulsory field 
        return False
        
    return True

def apscan_to_wifiAccessPoint(scan):
    """
    Helper method that converts between the input apscan format and the one Goolge expects

    Args:
        scan: apscan dictionary

    Returns:
        dictionary containing the apscan in Google format
    """

    _scan = {"macAddress": scan['bssid']}

    # Check for the optional fields and add them if present
    if 'signalStrength' in scan:
        _scan["signalStrength"] = scan['rssi'],

    if 'age' in scan:
        _scan["age"] =  round(time.time() - scan['timestamp'])
        
    if 'channel' in scan:
        _scan["channel"] = eval(scan["channel"])
    

    return _scan

def request_body_to_wifiAccessPoints(request_dict):
    """
    Convert a dictionary of access point scans into the format expected by the 
    Geolocation API.

    Args:
        request_dict: dictionary containing the apscans

    Returns:
        a list of dictionaries containing the converted apscans

    Raises:
        HTTPException: via flask.abort if conversion fails
    """
    
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
        abort(Response(
            status=400, 
            mimetype='application/json',
            response=json.dumps({
                'code': 400,
                'message': 'API requires at least 2 valid access points',
            })
        ))

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
