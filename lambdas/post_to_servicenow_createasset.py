import requests
import os
import json
import lambdas.mdmapi as mdmapi

apikey = os.environ.get('SimpleMDM_API_KEY')
serviceNowUser = os.environ.get('SERVICENOW_USER')
serviceNowPassword = os.environ.get('SERVICENOW_PASSWORD')
serviceNow_createasset = os.environ.get('SERVICENOW_CREATEASSET_URL')


def post_to_servicenow(json_data):
    payload = json_data
    headers = {
        'Cache-Control': "no-cache",
        'Content-Type': "application/json"
    }
    response = requests.post(
        serviceNow_createasset,
        auth=(serviceNowUser, serviceNowPassword),
        data=payload,
        headers=headers
    )
    print(response.text)
    return response


def post_to_snow_lambda(event, context):
    jsonEvent = json.loads(event['body'])
    serial = jsonEvent['serial_number']
    machine_id = mdmapi.get_machine_id(serial, apikey)
    laptop_json = mdmapi.get_laptop_information(machine_id, apikey)
    message = ("Posting device Serial {} with SimpleMDM ID {} to ServiceNow".format(serial, machine_id))
    post_to_servicenow(laptop_json)
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': message
    }
