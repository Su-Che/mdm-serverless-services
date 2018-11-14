import unittest
import lambdas.post_to_servicenow_createasset as snow
import lambdas.mdmapi as mdmapi
import json
from unittest.mock import Mock, patch

class TestSMDM(unittest.TestCase):
    global laptop_data
    laptop_data={
        "data": {
        "type": "device",
        "id": 121,
        "relationships": {
        "device_group": {
        "data": {
        "type": "device_group",
        "id": 37
    }}}}}

    @patch('lambdas.mdmapi.requests.get')
    def test_get_machine_id_returns_valid_machine_id(self,mock_get):
        response_data={
        "data": [
        {
        "type": "device",
        "id": 121,
        }]}
        mock_get.return_value.json.return_value = response_data
        response=mdmapi.get_machine_id('C02RK1L3G8WL','key')
        self.assertEqual(response,121)

    @patch('lambdas.mdmapi.requests.post')
    def test_move_to_filevault_group(self,mock_post):
        mock_post.return_value.json.return_value = laptop_data
        response=mdmapi.move_to_filevault_group('121','12345','key')
        self.assertEqual(response.json(),laptop_data)

    @patch('lambdas.mdmapi.requests.get')
    def test_query_group_should_return_valid_smdm_group_id(self,mock_get):
        mock_get.return_value.json.return_value=laptop_data
        response=mdmapi.query_group('121','key')
        self.assertEqual(response,37)

    @patch('lambdas.mdmapi.requests.get')
    def test_get_laptop_information_returning_laptop_data(self,mock_get):
        mock_get.return_value.json.return_value=laptop_data
        response=mdmapi.get_laptop_information('121','key')
        self.assertEqual(response,json.dumps(laptop_data))


if __name__ == '__main__':
    unittest.main()
