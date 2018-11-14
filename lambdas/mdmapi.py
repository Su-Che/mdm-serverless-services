import requests
import json

base_url = "https://a.simplemdm.com/api/v1"


def get_machine_id(serial_number, apikey):
    url = '{}/devices?search={}'.format(
        base_url,
        serial_number
    )
    laptop_data = requests.get(url, auth=(apikey, ''))
    json_laptop_data = laptop_data.json()
    try:
        simplemdm_machine_id = json_laptop_data['data'][0]['id']
        print((
            'Laptop serial number {}'
            'has a SimpleMDM machine id of {}').format(
            serial_number,
            simplemdm_machine_id
        ))
        return simplemdm_machine_id
    except Exception as e:
        print('{} is not in SimpleMDM'.format(serial_number))
        print('Error is: {}'.format(e))
        return

# Pulling the "Enable Filevault group from an environment variable"
# so this code is reusable in Dev and Prod


def move_to_filevault_group(machine_id, filevault_group_id, apikey):
    url = '{}/device_groups/{}/devices/{}'.format(
        base_url,
        filevault_group_id,
        machine_id
    )
    response = requests.post(url, auth=(apikey, ''))
    print((
        'Moving a machine with SimpleMDM ID {} '
        'to the Enable Filevault Group').format(machine_id))
    return response


def query_group(machine_id, apikey):
    url = '{}/devices/{}'.format(base_url, machine_id)
    response = requests.get(url, auth=(apikey, ''))
    json_response = response.json()
    try:
        simplemdm_group = (
            json_response
            ["data"]
            ["relationships"]
            ["device_group"]
            ["data"]
            ["id"]
        )
        print('Machine id {} is in SimpleMDM Group {}'.format(
            machine_id,
            simplemdm_group)
        )
        return simplemdm_group
    except Exception as e:
        print("no such group")
        print("Error is {}".format(e))
        return
    return simplemdm_group


def get_laptop_information(machine_id, apikey):
    url = "{}/devices/{}".format(base_url, machine_id)
    laptop_data = requests.get(url, auth=(apikey, ''))
    json_laptop_data = laptop_data.json()
    fixed_json_laptop_data = json.dumps(json_laptop_data)
    print(fixed_json_laptop_data)
    return fixed_json_laptop_data
