# Author: Aaron Alakkadan
from app.auth import email_content_password_reset, url_for, send_email
from unittest import mock

'''
Testing the return value of send_email. mock ignores app.extensions.email.send.
Looks up an object in a given module and replaces that object with a Mock
This function tests for send email by asserting if the sender is su.study.buddy@gmail.com
It also asserts if the username which is stored in a variable email_address is in the recipients list
The function also tests if the method returns a value and is called 
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
def test_email(mock_email, client):
    with client.application.test_request_context():
        email_address = "su.study.buddy@gmail.com"
        msg = send_email(email_address, "Test html", "Hello")
        assert msg.sender == 'su.study.buddy@gmail.com'
        assert email_address in msg.recipients
        assert mock_email.return_value  
        assert mock_email.called