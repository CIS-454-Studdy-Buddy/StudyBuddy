# 

def test_login_user_not_existing(client):
    response = client.post("/login", data={"username": "nonexistent@syr.edu", "password": "ge3456"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid Login" in response.data

def test_login_invalid_token():
    pass

def test_login_email_verification_link_clicked():
    pass

def test_login_email_verification_link_not_clicked():
    pass

def test_login_password_not_matching():
    pass

def test_login_successful():
    pass