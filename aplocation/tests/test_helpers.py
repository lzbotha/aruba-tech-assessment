import unittest

from aplocation.helpers import scan_is_valid, apscan_to_wifiAccessPoint

class TestScanIsValid(unittest.TestCase):
    
    def test_valid_scan(self):
        scan = {
            'bssid' : "c0:a0:bb:c4:10:d6"
        }

        self.assertTrue(scan_is_valid(scan))

    def test_missing_mac_address(self):
        scan = {}

        self.assertFalse(scan_is_valid(scan))

    def test_malformed_mac_address(self):
        scan = {
            'bssid' : "nonsense"
        }

        self.assertFalse(scan_is_valid(scan))


class TestApscanToWifiAccessPoint(unittest.TestCase):

    def test_valid_scan(self):
        scan = {
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

        ap = apscan_to_wifiAccessPoint(scan)
        
        self.assertEqual(ap['macAddress'], 'c0:a0:bb:c4:10:d6')
        self.assertEqual(ap['channel'], 1)
        self.assertEqual(ap['signalStrength'], -66)

    
    def test_invalid_optional_values(self):
        scans = [
            {   
                "bssid": "c0:a0:bb:c4:10:d6",
                "channel": "nonsense",
                "rssi": "nonsense",
                "timestamp": "nonsense",
            },
            {   
                "bssid": "c0:a0:bb:c4:10:d6",
                "channel": -1,
                "timestamp": -1,
            }
        ]

        for scan in scans:
            ap = apscan_to_wifiAccessPoint(scan)

            self.assertNotIn('age', ap)
            self.assertNotIn('channel', ap)
            self.assertNotIn('signalStrength', ap)