'''
Author: Aaron Alakkadan 
'''
from app.auth import RegisterForm

'''
The function test_signup_user tests if the user entered a valid syr email and rentered a correct password
also when they do so they will be redirected to the email confirmation page
'''
def test_signup_new_user(client):

    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein", 
                                            "username": "bobby@syr.edu", "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

'''
The function test_signup_failed_email_syr_new_user tests when the user input an email that is not 
@syr.edu then they should stay on the signup page and throw an error message 
'''    
def test_signup_failed_email_syr_new_user(client):
    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein",
                                            "username": "bobby@gmail.com", "password": "ge3456",
                                            "re_enter_password": "ge516"}, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/signup'
    assert b"Your email address must be a valid Syracuse University email" in response.data


'''
The function test_signup_username_not_email tests if a user inputs an username without an @ symbol
and it is an invalid @syr.edu email then they should stay on the signup page and throw an error message
'''
def test_signup_username_not_email(client):
    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein",
                                            "username": "bobby", "password": "ge3456",
                                            "re_enter_password": "ge516"}, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/signup'
    assert b"The email address is not valid. It must have exactly one @-sign." in response.data
    assert b"Your email address must be a valid Syracuse University email" in response.data


'''
The function test_signup_existing_user tests if a user signs in with valid credentials but tries to
sign in again with the same credentials even though the user already exits it will throw an error
'''
def test_signup_existing_user(client):
    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein",
                                            "username": "exist_user@syr.edu", "password": "ge3456",
                                           "re_enter_password": "ge3456"}, follow_redirects=True)
    assert response.status_code == 200
    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein",
                                            "username": "exist_user@syr.edu", "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert response.request.path == '/signup'
    assert b"That username already exists. Please choose a different one." in response.data

'''
The function test_fail_re_enter_password tests if a user signs in with a valid username and password but 
fails to re-enter the same password it will throw an error
'''
def test_fail_re_enter_password(client):
    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein",
                                            "username": "renterpw@syr.edu", "password": "ge3456",
                                           "re_enter_password": "615ge"}, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/signup'
    assert b"Passwords do not match, try again." in response.data


