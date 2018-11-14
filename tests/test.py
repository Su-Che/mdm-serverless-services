import unittest
from flask import url_for
import src.app as app
from flask import current_app

class TestApp(unittest.TestCase):

    def submit_serial(self, client, serial):
        return client.get('/', query_string=dict(
            serial=serial
        ), follow_redirects=True)

    def register_submit_serial(self,client,serial):
        return client.get('/register',query_string=dict(
            serial=serial,
            register='1'
        ), follow_redirects=True)

    def test_should_display_error_message_if_no_serial_provided(self):
        client = app.app.test_client()
        response = self.submit_serial(client, '')
        self.assertTrue(b'Missing Serial Number' in response.data)

    def test_should_display_nice_message_if_serial_present(self):
        client = app.app.test_client()
        response = self.submit_serial(client, 'C0257875G8WL')
        self.assertTrue(b'register.png' in response.data)

    def test_should_redirect_to_SAML_login_page_if_user_is_not_authenticated(self):
        client = app.app.test_client()
        app.app.config['SERVER_NAME'] = 'localhost'
        response = client.get('/register?serial=chuhi&live=1', follow_redirects=False)
        print(response)
        self.assertEqual(response.status_code, 302)

    def test_should_display_error_if_no_serial_provided_on_register(self):
        client = app.app.test_client()
        response = self.register_submit_serial(client, '')
        self.assertTrue(b'Missing Serial Number' in response.data)


if __name__ == '__main__':
    unittest.main()
