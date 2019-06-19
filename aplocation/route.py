import time
import os
import json
import re

from flask import Flask, jsonify
from flask import request
from flask import abort, Response

from aplocation.geolocation import make_geolocation_request

app = Flask(__name__)

import logging
logger = logging.getLogger(__name__)


def scan_is_valid(scan):
    """
    Check if an input scan dictionary is valid / can be converted to the Geolocation
    format.

    Args:
        scan: apscan dictionary

    Returns:
        bool true if valid false otherwise
    """

    if 'bssid' not in scan: # macAddress is the only compulsory field 
        return False

    # Code borrowed from https://stackoverflow.com/questions/7629643/how-do-i-validate-the-format-of-a-mac-address
    if not re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", scan['bssid'].lower()):
        return False

    return True

def apscan_to_wifiAccessPoint(scan):
    """
    Helper method that converts between the input apscan format and the one Goolge expects.
    Ignores optional inputs if they are invalid.

    Args:
        scan: apscan dictionary

    Returns:
        dictionary containing the apscan in Google format
    """

    _scan = {"macAddress": scan['bssid']}

    # These parameters are optional. As such if they fail validation we can ignore them.
    if 'rssi' in scan:
        if isinstance(scan['rssi'], int) or isinstance(scan['rssi'], float):
            _scan["signalStrength"] = scan['rssi']
        else:
            logger.info('Non float rssi value found. Ignoring it.')

    if 'timestamp' in scan:
        if (isinstance(scan['timestamp'], int) or isinstance(scan['timestamp'], float)) and scan['timestamp'] > 0:
            _scan["age"] =  round(time.time() - scan['timestamp'])
        else:
            logger.info('Invalid timestamp recieved. Ignoring it.')
        
    if 'channel' in scan:
        if isinstance(scan['channel'], int)  and scan['timestamp'] > 0:
            _scan["channel"] = eval(scan["channel"])
        else:
            logger.info('Invalid channel recieved. Ignoring it.')
    
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
            logger.info('Invalid apscan found. Ignoring it.')

    # At least 2 scans are required to do a geolocation lookup
    if len(scans) < 2:
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
        logger.error("GEOLOCATION_API_KEY environment variable not set")

        abort(Response(
            status=500, 
            mimetype='application/json',
            response=json.dumps({
                'code': 500,
                'message': 'Server configuration error',
            })
        ))
        

    # Get the list of wifi access points in the format Geolocation expects
    wifi_access_points = request_body_to_wifiAccessPoints(request.json)

    # Query the Geolocation API
    location_response = make_geolocation_request(wifi_access_points, api_key)

    # Check for errors in the response
    if 'error' in location_response:

        # If the location cannot be found return a 404
        logger.info("Location not found")
        if location_response['error']['code'] == 404:
            abort(Response(
            status=404, 
            mimetype='application/json',
            response=json.dumps({
                'code': 404,
                'message': 'Location not found',
            })
        ))
        
        # Otherwise return a 500 if something else went wrong
        logger.error(f"Geolocation error {location_response['error']}")

        abort(Response(
            status=500, 
            mimetype='application/json',
            response=json.dumps({
                'code': 500,
                'message': 'Server error',
            })
        ))

    return jsonify(location_response), 200
