import boto3
import secrets

serviceNowPassword = ""
ssm_client = boto3.client('ssm')
kms_client = boto3.client('kms')

char_set = {
    'lower': 'abcdefghijklmnopqrstuvwxyz',
    'upper': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'num': '0123456789',
    'special': '!@#$%^&*()-_+={[]}|,<.>;;'
}

def get_secret(key):
    resp = ssm_client.get_parameter(
        Name=key,
        WithDecryption=True
    )
    return resp['Parameter']['Value']


#def secret_exist(key):
#    try:
#        client.get_parameter(Name=key, WithDecryption=True)
#    except botocore.errorfactory.ParameterNotFound:
#        return False
#    return True

def generate_password(length=20):
    password = []
    while len(password) < length:
        key = secrets.choice(char_set.keys())
        char = secrets.choice(char_set[key])
        password.append(char)
    return ''.join(password)


def main():
    try:

        paramKey = kms_client.describe_key(
            KeyId="alias/SERVICENOW_PARAM_KEY"
        )
        keyid = paramKey['KeyMetadata']['KeyId']
    except kms_client.exceptions.NotFoundException:
        paramKey = kms_client.create_key(
            Description='parameter decryption key',
            KeyUsage='ENCRYPT_DECRYPT',
            Origin='AWS_KMS'
        )
        keyid = paramKey['KeyMetadata']['KeyId']
        kms_client.create_alias(
            AliasName="alias/SERVICENOW_PARAM_KEY",
            TargetKeyId=keyid
        )

    newpassword = generate_password()
    
    try:
        serviceNowPassword = get_secret('SERVICENOW_PASSWORD')
    except ssm_client.exceptions.ParameterNotFound:
        ssm_client.put_parameter(
            Name='SERVICENOW_PASSWORD',
            Description='Password for ServiceNow',
            Value=newpassword,
            Type='SecureString',
            KeyId=keyid,
            Overwrite=True
        )
        serviceNowPassword = newpassword
    print("The password for ServiceNow user SimpleMDMUser has been set to {}".format(serviceNowPassword))
    print("Change it manually with an admin account")



if __name__ =="__main__":
    main()
