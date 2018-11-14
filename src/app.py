from flask import Flask, render_template, request
import boto3
import requests
import os
import urllib
import uuid
import json

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from saml2 import (
    BINDING_HTTP_POST,
    BINDING_HTTP_REDIRECT,
    entity,
)
from saml2.client import Saml2Client
from saml2.config import Config as Saml2Config

metadata_url_for = {
    'rolzog': os.environ.get('METADATA_URL')
}

app = Flask(__name__)
app._static_folder = "../static"
app.secret_key = str(uuid.uuid4())
login_manager = LoginManager()
login_manager.setup_app(app)



def saml_client_for(idp_name=None):
    '''
    Given the name of an IdP, return a configuation.
    The configuration is a hash for use by saml2.config.Config
    '''

    if idp_name not in metadata_url_for:
        raise Exception("Settings for IDP '{}' not found".format(idp_name))
    acs_url = url_for(
        "idp_initiated",
        idp_name=idp_name,
        _external=True)
    https_acs_url = url_for(
        "idp_initiated",
        idp_name=idp_name,
        _external=True,
        _scheme='https')

    #   SAML metadata changes very rarely. On a production system,
    #   this data should be cached as approprate for your production system.
    rv = requests.get(metadata_url_for[idp_name])
    settings = {
        "entityid": "rolzog",
        'metadata': {
            'inline': [rv.text],
            },
        'service': {
            'sp': {
                'endpoints': {
                    'assertion_consumer_service': [
                        (acs_url, BINDING_HTTP_REDIRECT),
                        (acs_url, BINDING_HTTP_POST),
                        (https_acs_url, BINDING_HTTP_REDIRECT),
                        (https_acs_url, BINDING_HTTP_POST)
                    ],
                },
                # Don't verify that the incoming requests originate from us via
                # the built-in cache for authn request ids in pysaml2
                'allow_unsolicited': True,
                # Don't sign authn requests, since signed requests only make
                # sense in a situation where you control both the SP and IdP
                'authn_requests_signed': False,
                'logout_requests_signed': True,
                'want_assertions_signed': True,
                'want_response_signed': False,
            },
        },
    }
    spConfig = Saml2Config()
    spConfig.load(settings)
    spConfig.allow_unknown_attributes = True
    saml_client = Saml2Client(config=spConfig)
    return saml_client


class User(UserMixin):
    def __init__(self, user_id):
        self.id = None
        try:
            self.id = user_id
        except Exception:
            pass


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route("/saml/sso/<idp_name>", methods=['POST'])
def idp_initiated(idp_name):
    saml_client = saml_client_for(idp_name)
    authn_response = saml_client.parse_authn_request_response(
        request.form['SAMLResponse'],
        entity.BINDING_HTTP_POST)
    authn_response.get_identity()
    user_info = authn_response.get_subject()
    email = user_info.text

    # This is what as known as "Just In Time (JIT) provisioning".
    # What that means is that, if a user in a SAML assertion
    # isn't in the user store, we create that user first, then log them in
    # if email not in user_store:
    #     user_store[email] = {
    #         'id': email
    #         }
    #

    user = User(email)
    session['saml_attributes'] = authn_response.ava
    login_user(user)
    if 'RelayState' in request.form:
        url = request.form['RelayState']
    return redirect(url)


@app.route("/")
def main():
    serial = request.args.get("serial")
    if not serial:
        return render_template('oops.html', details="Missing Serial Number")

    return render_template('index.html', serial=serial, env=os.environ.get('ENV_TYPE'))


@app.route("/register")
def register():
    serial = request.args.get("serial")
    if not serial:
        return render_template('oops.html', details="Missing Serial Number")

    if (not current_user.is_authenticated):
        idp_name = next(iter(metadata_url_for.keys()))
        relaystate = b"register?" + request.query_string
        return redirect("saml/login/%s/%s" % (idp_name, urllib.parse.quote(relaystate)))

    apiGateway = boto3.client('apigateway', region_name="eu-west-1")

    apiKeyName ="post-to-servicenow-api-key-{}".format(os.environ.get("ENV_TYPE"))
    apiKey = ''
    for item in apiGateway.get_api_keys(includeValues=True)['items']:
        if item['name'] == apiKeyName:
            apiKey = item['value']

    headers = {'Content-Type': 'application/json', 'x-api-key': apiKey}
    apiKeyName ="post-to-servicenow-api-key-{}".format(os.environ.get("ENV_TYPE"))
    data = json.dumps({'user': current_user.id, 'serial_number': serial})

#Enable encryption
    moveDevice_url = "{}moveDevice".format(request.url_root)
    print("Posting {} to: {}".format(data, moveDevice_url))

    result = requests.post(url=moveDevice_url, data=data, headers=headers)
    if (result.status_code == 200):
        print(result.text)
    else:
        print("error moving device to encryption group")
        print(result.text)


# createasset
    postToServiceNow_url = "{}postToServiceNowCreateAsset".format(request.url_root)
    print("Posting {} to: {}".format(data, postToServiceNow_url))

    result = requests.post(url=postToServiceNow_url, data=data, headers=headers)
    if (result.status_code == 200):
        print(result.text)
    else:
        print("error in creating asset")
        print(result.text)

 # Assignment
    postToServiceNow_url = "{}postToServiceNowAssignment".format(request.url_root)
    print("Posting {} to: {}".format(data, postToServiceNow_url))

    result = requests.post(url=postToServiceNow_url, data=data, headers=headers)
    if (result.status_code == 200):
        template = 'done.html'
    else:
        template = 'oops.html'
    return render_template(template, env=os.environ.get('ENV_TYPE'))


@app.route("/saml/login/<idp_name>/<relaystate>")
def sp_initiated(idp_name, relaystate):
    saml_client = saml_client_for(idp_name)
    reqid, info = saml_client.prepare_for_authenticate()

    redirect_url = None
    # Select the IdP URL to send the AuthN request to
    for key, value in info['headers']:
        if key is 'Location':
            redirect_url = value + "&RelayState=" + relaystate
    response = redirect(redirect_url, code=302)
    response.headers['Cache-Control'] = 'no-cache, no-store'
    response.headers['Pragma'] = 'no-cache'
    return response


if __name__ == "__main__":
    app.run()
