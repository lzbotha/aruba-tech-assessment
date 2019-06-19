import time
import re

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

    # Validate the format of the macAddress
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
        # Channels are strings coming, but could be ints
        try:
            chan = eval(scan['channel'])
        except:
            chan = scan['channel']

        if isinstance(chan, int)  and chan > 0:
            _scan["channel"] = eval(scan["channel"])
        else:
            logger.info('Invalid channel recieved. Ignoring it.')
    
    return _scan