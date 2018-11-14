# Our three MDM serverless services

In the order that they are triggered during MDM enrolment:

1. **Rolzog** – a serverless Python app using the Flask framework. We’re running it in AWS Lambda. It is opened during the enrolment process, in the user's browser, including the laptop's serial number in the query string. Rolzog prompts the user to login to Okta. Rolzog sends the serial number and authenticated username to our new asset management tool, ServiceNow. ServiceNow then "assigns" the laptop to the user by recording their user ID against the laptop record.
1. **post-to-snow** – A simple function that posts a JSON object to a ServiceNow API containing all of the hardware details SimpleMDM holds about the laptop. This is called by Rolzog (back-end call) during enrolment. In future this will hook into SimpleMDM to get regular updates on hardware and software into ServiceNow.
1. **move-group** – a simple function that calls a SimpleMDM API to move a device into the group that delivers the FileVault (disk encryption) configuration profile. This is called by Rolzog (back-end call) after the other enrolment configuration (password policy, firewall, Rolzog is complete) – it has to be done after the other configuration because the filevault profile requires a valid user account to exist on the laptop, which isn’t the case during the initial enrolment of a brand new laptop.


## Build and deployment

The build and deployment is on https://seed.run. You'll need access to the thoughtworks-identity organization.

## Running tests locally

`docker build -t mdm .`

`docker run -i --mount type=bind,source="$(pwd)"/tests,target=/app/tests --mount type=bind,source="$(pwd)"/lambdas,target=/app/lambdas -t mdm`

`python -m unittest discover tests`


### LIBXMLSEC1

The pysaml2 library will need libxmlsec1 binaries and libraries from Amazon Linux to work as a lambda function. 

## ci / create_servicenow_param

A script to generate secure passwords and store encrypted in parameter store is included, but not in use. During development, we found this lead to a 'chicken and the egg' problem re ServiceNow credentials. It would require manual intervention either way. Presently the pipeline is configured with static credentials.

This script will be lambda'ized to implement rotating passwords.
