from app.auth import email_content_password_reset, url_for

def test_email_content(client):
    email_content_password_reset("aalakkad@syr.edu", "/reset_password?t=5301637811")
    assert 1 == 2