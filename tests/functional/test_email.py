from app.auth import email_content_password_reset, url_for, send_email
from unittest import mock

# testing the return value of send_email. mock ignores app.extensions.email.send. 
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
def test_email(mock_email):
    email_address = "aalakkad@syr.edu"
    msg = send_email(email_address, "Test html", "Hello")
    assert msg.sender == 'su.study.buddy@gmail.com'
    assert email_address in msg.recipients
    assert mock_email.return_value  
    assert mock_email.called

