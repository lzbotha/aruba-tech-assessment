import time
import os
import json


from flask import Flask, jsonify
from flask import request
from flask import abort, Response

from aplocation.geolocation import make_geolocation_request
from aplocation.helpers import scan_is_valid, apscan_to_wifiAccessPoint

app = Flask(__name__)

import logging
logger = logging.getLogger(__name__)


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

    if 'apscan_data' not in request_dict:
        abort(Response(
            status=400, 
            mimetype='application/json',
            response=json.dumps({
                'code': 400,
                'message': 'No apscan_data in request',
            })
        ))
    
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


def get_api_key():
    """
    Helper method that gets the API key from an environment variable or throws
    a HTTPException (via flask.abort) if not found.

    Returns:
        string with the API key

    Raises:
        HTTPException: if GEOLOCATION_API_KEY the environment variable is not set
    """

    try:
        return os.environ['GEOLOCATION_API_KEY']
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

def handle_errors(location_response):
    """
    Check the Geolocation response for errors and deal with them appropriately.

    Args:
        location_response:  dict containing response from the Geolocation API.
    Raises:
        HTTPException: if GEOLOCATION_API_KEY the environment variable is not set
    """

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

def fetch_response_from_cache(wifi_access_points):
    """
    Placeholder method for caching functionality.

    Args:
        wifi_access_points: a list of dictionaries containing the converted apscans

    Returns:
        bool:   true if result is cached false otherwise
        dict:   the cached response
    """

    return False, None

@app.route('/api/v1.0/location', methods=['POST'])
def get_location_from_ap_scans():

    # Get the API key for the geolocation API
    api_key = get_api_key()
        
    # Get the list of wifi access points in the format Geolocation expects
    wifi_access_points = request_body_to_wifiAccessPoints(request.json)

    # Hit the cache
    success, response = fetch_response_from_cache(wifi_access_points)
    if success:
        return jsonify(response), 200

    # Query the Geolocation API
    location_response = make_geolocation_request(wifi_access_points, api_key)

    # Check for errors in the response
    handle_errors(location_response)

    return jsonify(location_response), 200
