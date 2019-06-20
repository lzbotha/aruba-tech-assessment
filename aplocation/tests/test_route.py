import unittest

import werkzeug

from aplocation.route import request_body_to_wifiAccessPoints

class TestRequestBodyToWifiAccessPoints(unittest.TestCase):
    
    def test_valid_request(self):
        # Note we have tested the functionality of the actual parsing in
        # the tests for helper.py. We only need to test the remaining 
        # logic here.

        request_dict = {
            "apscan_data": [
            {
                "band": "2.4",
                "bssid": "9c:b2:b2:66:c1:be",
                "channel": "5",
                "frequency": 2432,
                "rates": "1.0 - 135.0 Mbps",
                "rssi": -35,
                "security": "wpa-psk",
                "ssid": "HUAWEI-B315-C1BE",
                "timestamp": 1522886457.0,
                "vendor": "HUAWEI TECHNOLOGIES CO.,LTD",
                "width": "20"
            },
            {
                "band": "2.4",
                "bssid": "84:78:ac:b9:76:19",
                "channel": "1",
                "frequency": 2412,
                "rates": "6.5 - 270.0 Mbps",
                "rssi": -56,
                "security": "wpa-eap",
                "ssid": "1 Telkom Connect",
                "timestamp": 1522886457.0,
                "vendor": "Cisco Systems, Inc",
                "width": "20"
            },
            {
                "band": "2.4",
                "bssid": "c0:a0:bb:c4:10:d6",
                "channel": "1",
                "frequency": 2412,
                "rates": "1.0 - 54.0 Mbps",
                "rssi": -66,
                "security": "wpa-psk",
                "ssid": "default",
                "timestamp": 1522886457.0,
                "vendor": "D-Link International",
                "width": "40"
            }
            ]
        }

        access_points = request_body_to_wifiAccessPoints(request_dict)
        self.assertEqual(len(access_points), 3)

    def test_insufficient_access_points(self):
        # Test that a request with no apscan data fails
        with self.assertRaises(werkzeug.exceptions.HTTPException):
            request_body_to_wifiAccessPoints({})

        # Test that a request with insufficient aps fails
        with self.assertRaises(werkzeug.exceptions.HTTPException):
            request_body_to_wifiAccessPoints({
                'apscan_data': []
            })
        