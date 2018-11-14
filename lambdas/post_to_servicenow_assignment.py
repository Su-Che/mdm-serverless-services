import requests
import os
import json

serviceNowUser = os.environ.get('SERVICENOW_USER')
serviceNowPassword = os.environ.get('SERVICENOW_PASSWORD')
serviceNow_createasset = os.environ.get('SERVICENOW_ASSIGNMENT_URL')


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
    return response


def post_to_snow_lambda(event, context):
    jsonEvent = json.loads(event['body'])
    serial = jsonEvent['serial_number']
    user = jsonEvent['user']
    message = ("Assigning {} to device {} in ServiceNow".format(user, serial))
    print(message)
    payload = {'user': user, 'serial_number': serial}
    result = post_to_servicenow(json.dumps(payload))
    print(result.text)
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': result.text
    }
