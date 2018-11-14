import unittest
import lambdas.post_to_servicenow_assignment as snow_assign
import lambdas.post_to_servicenow_createasset as snow_asset
import json
from unittest.mock import patch

class TestSNOW(unittest.TestCase):

    @patch('lambdas.post_to_servicenow_assignment.requests.post')
    def test_should_assign_serialNumber_to_registered_user(self, mock_post):
        payload = {
            'user': "user@thoughtworks.com",
            'serial_number': "C02SN3CPF822"
            }
        response_data = {
            "result": {
                "Status": "Successful ",
                "Response": "asset with serial number C02SN3CPF822 is assigned to user@thoughtworks.com"
                }}
        mock_post.return_value.json.return_value = response_data
        response = snow_assign.post_to_servicenow(payload)
        self.assertEqual(response.json(),response_data)

    @patch('lambdas.post_to_servicenow_createasset.requests.post')
    def test_should_create_asset_in_serviceNow(self, mock_post):
        laptop_data = {
                "data": {
                    "attributes": {
                        "status": "enrolled",
                        "serial_number": "DNFJE9DNG5MG",
                        "wifi_mac": "f0:db:e2:df:e9:2f",
                        "model": "MacBookAir13,1"
                    }}}
        response_data = {
                "result": {
                    "Status": "Successful ",
                    "Response": "asset created with serial number C02W8FG8LrL"
                    }}
        mock_post.return_value.json.return_value = response_data
        response = snow_asset.post_to_servicenow(laptop_data)
        self.assertEqual(response.json(),response_data)
