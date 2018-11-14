import os
import json
import lambdas.mdmapi as mdmapi


apikey = os.environ.get('SimpleMDM_API_KEY')
newLaptopGroupID = int(os.environ.get('NewLaptopGroupID'))
existingLaptopGroupID = int(os.environ.get('ExistingLaptopGroupID'))
enableFileVaultGroupID = int(os.environ.get('EnableFileVaultGroupID'))


def move_device_lambda(event, context):
    jsonEvent = json.loads(event['body'])
    serial = jsonEvent['serial_number']
    machine_id = mdmapi.get_machine_id(serial, apikey)
    groupid = mdmapi.query_group(machine_id, apikey)

    if groupid in [newLaptopGroupID, existingLaptopGroupID]:
        mdmapi.move_to_filevault_group(
            machine_id,
            enableFileVaultGroupID,
            apikey
        )
        message = (
            "Moving laptop {} to the production"
            " 'enable filevault' group").format(serial)
        print(message)
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': message
        }
    else:
        message = ('Laptop not in New machine or Existing Machine group')
        print(message)
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': message
        }
