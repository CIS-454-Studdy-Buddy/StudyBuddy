from app.auth import RegisterForm

def test_signup_new_user(client):

    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein", 
                                            "username": "bobby@syr.edu", "password": "ge3456",
                                            "re_enter_password": "ge516"})
    assert response.status_code == 200

    
def test_signup_failed_email_syr_new_user(client):
    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein",
                                            "username": "bobby@gmail.com", "password": "ge3456",
                                            "re_enter_password": "ge516"})
    assert response.status_code == 200
    assert b"Your email address must be a valid Syracuse University email" in response.data

def test_signup_username_not_email(client):
    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein",
                                            "username": "bobby", "password": "ge3456",
                                            "re_enter_password": "ge516"})
    assert response.status_code == 200
    assert b"The email address is not valid. It must have exactly one @-sign." in response.data
    assert b"Your email address must be a valid Syracuse University email" in response.data


def test_signup_existing_user(client):
    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein",
                                            "username": "exist_user@syr.edu", "password": "ge3456",
                                           "re_enter_password": "ge3456"}, follow_redirects=True)
    assert response.status_code == 200
    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein",
                                            "username": "exist_user@syr.edu", "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert b"That username already exists. Please choose a different one." in response.data


def test_fail_re_enter_password(client):
    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein",
                                            "username": "renterpw@syr.edu", "password": "ge3456",
                                           "re_enter_password": "615ge"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Passwords do not match, try again." in response.data

     








