from flask import url_for, request
from app.auth import email_content_password_reset, url_for, send_email
from unittest import mock
import random
from app.models.user import User
from app.profile import current_user

'''
This function tests if the first name, last name, and username fields are present when visiting the profile page
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_profile_fields_present(mock_token, mock_email, client):
    # send data to signup using post method
    # redirects to email confirmation
    username = "validt@syr.edu"
    first_name = "Bobby"
    last_name = "Goldstein"
    response = client.post("/signup", data={"first_name": first_name, "last_name": last_name,
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        # send data to login using post method with the right token redirection which is 1234
        # logged in by clicking the link in the confirmation email and not manipulating the token
        # therefore the user is redirected to the dashboard page  
        response = client.post('/login?t=1234', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified
        assert response.request.path == '/dashboard' 

        # Go to the profile page to check these fields
        response = client.get('/profile') 
        assert response.request.path == '/profile'
        assert current_user.first_name == user.first_name
        assert current_user.last_name == user.last_name
        assert current_user.username == user.username

'''
The function checks if the user wants to input the phoneNumber into the optional field
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_profile_input_phonenumber(mock_token, mock_email, client):
    # send data to signup using post method
    # redirects to email confirmation
    username = "validt@syr.edu"
    first_name = "Bobby"
    last_name = "Goldstein"
    response = client.post("/signup", data={"first_name": first_name, "last_name": last_name,
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        # send data to login using post method with the right token redirection which is 1234
        # logged in by clicking the link in the confirmation email and not manipulating the token
        # therefore the user is redirected to the dashboard page  
        response = client.post('/login?t=1234', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified
        assert response.status_code == 200
        assert response.request.path == '/dashboard' 

        # Go to the profile page to check these fields
        # Enter phone number via post data and save it 
        # Redirect to dashboard page
        # Go to profile page to ensure change has been made 
        assert response.status_code == 200
        response = client.get('/profile')
        phoneNumber = "1234567890"
        assert response.status_code == 200
        assert response.request.path == '/profile'
        assert current_user.first_name == user.first_name
        assert current_user.last_name == user.last_name
        assert current_user.username == user.username
        response = client.post('/profile', data={"phoneNumber": phoneNumber, "aboutMe": "hello world", "saveButton" : "1"}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/profile'
        assert phoneNumber in response.text

'''
The function checks if the user wants to input the aboutMe into the optional field
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_profile_input_aboutme(mock_token, mock_email, client):
    # send data to signup using post method
    # redirects to email confirmation
    username = "validt@syr.edu"
    first_name = "Bobby"
    last_name = "Goldstein"
    response = client.post("/signup", data={"first_name": first_name, "last_name": last_name,
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        # send data to login using post method with the right token redirection which is 1234
        # logged in by clicking the link in the confirmation email and not manipulating the token
        # therefore the user is redirected to the dashboard page  
        response = client.post('/login?t=1234', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified
        assert response.status_code == 200
        assert response.request.path == '/dashboard' 

        # Go to the profile page to check these fields
        # Enter phone number via post data and save it 
        # Redirect to dashboard page
        # Go to profile page to ensure change has been made 
        assert response.status_code == 200
        response = client.get('/profile')
        aboutMe = "Hi, my name is Bob and I like computer science"
        assert response.status_code == 200
        assert response.request.path == '/profile'
        assert current_user.first_name == user.first_name
        assert current_user.last_name == user.last_name
        assert current_user.username == user.username
        response = client.post('/profile', data={"phoneNumber": "1234567890", "aboutMe": aboutMe, "saveButton" : "1"}, follow_redirects=True)
        assert response.status_code == 200
        assert aboutMe in response.text

'''
The function checks if the user wants to input the phone number and aboutMe into the optional field
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_profile_input_phonenumber_and_aboutme(mock_token, mock_email, client):
    # send data to signup using post method
    # redirects to email confirmation
    username = "validt@syr.edu"
    first_name = "Bobby"
    last_name = "Goldstein"
    response = client.post("/signup", data={"first_name": first_name, "last_name": last_name,
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        # send data to login using post method with the right token redirection which is 1234
        # logged in by clicking the link in the confirmation email and not manipulating the token
        # therefore the user is redirected to the dashboard page  
        response = client.post('/login?t=1234', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified
        assert response.status_code == 200
        assert response.request.path == '/dashboard' 

        # Go to the profile page to check these fields
        # Enter phone number via post data and save it 
        # Redirect to dashboard page
        # Go to profile page to ensure change has been made 
        assert response.status_code == 200
        response = client.get('/profile')
        phoneNumber = "1234567890"
        aboutMe = "Hi, my name is Bob and I like computer science"
        assert response.status_code == 200
        assert response.request.path == '/profile'
        assert current_user.first_name == user.first_name
        assert current_user.last_name == user.last_name
        assert current_user.username == user.username
        response = client.post('/profile', data={"phoneNumber": phoneNumber, "aboutMe": aboutMe, "saveButton" : "1"}, follow_redirects=True)
        assert response.status_code == 200
        assert phoneNumber in response.text
        assert aboutMe in response.text

'''
This function checks if the user wants to edit their phone number and the new phone number is displayed
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_profile_edit_phonenumber(mock_token, mock_email, client):
    # send data to signup using post method
    # redirects to email confirmation
    username = "validt@syr.edu"
    first_name = "Bobby"
    last_name = "Goldstein"
    response = client.post("/signup", data={"first_name": first_name, "last_name": last_name,
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        # send data to login using post method with the right token redirection which is 1234
        # logged in by clicking the link in the confirmation email and not manipulating the token
        # therefore the user is redirected to the dashboard page  
        response = client.post('/login?t=1234', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified
        assert response.status_code == 200
        assert response.request.path == '/dashboard' 

        # Go to the profile page to check these fields
        # Enter phone number via post data and save it 
        # Redirect to dashboard page
        # Go to profile page to ensure change has been made 
        assert response.status_code == 200
        response = client.get('/profile')
        phoneNumber = "1234567890"
        phoneNumber2 = "56765567"
        assert response.status_code == 200
        assert response.request.path == '/profile'
        assert current_user.first_name == user.first_name
        assert current_user.last_name == user.last_name
        assert current_user.username == user.username
        response = client.post('/profile', data={"phoneNumber": phoneNumber, "aboutMe": "hello world", "saveButton" : "1"}, follow_redirects=True)
        assert response.status_code == 200
        response = client.post('/profile', data={"phoneNumber": phoneNumber2, "aboutMe": "hello world", "saveButton" : "1"}, follow_redirects=True)
        assert response.status_code == 200
        assert phoneNumber2 in response.text

'''
This function checks if the user wants to edit their about me and the new about me is displayed
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_profile_edit_aboutme(mock_token, mock_email, client):
    # send data to signup using post method
    # redirects to email confirmation
    username = "validt@syr.edu"
    first_name = "Bobby"
    last_name = "Goldstein"
    response = client.post("/signup", data={"first_name": first_name, "last_name": last_name,
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        # send data to login using post method with the right token redirection which is 1234
        # logged in by clicking the link in the confirmation email and not manipulating the token
        # therefore the user is redirected to the dashboard page  
        response = client.post('/login?t=1234', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified
        assert response.status_code == 200
        assert response.request.path == '/dashboard' 

        # Go to the profile page to check these fields
        # Enter phone number via post data and save it 
        # Redirect to dashboard page
        # Go to profile page to ensure change has been made 
        assert response.status_code == 200
        response = client.get('/profile')
        aboutMe = "Hi, my name is Bob and I like computer science"
        aboutMe2 = "Hi, my name is Bob and I like music"
        assert response.status_code == 200
        assert response.request.path == '/profile'
        assert current_user.first_name == user.first_name
        assert current_user.last_name == user.last_name
        assert current_user.username == user.username
        response = client.post('/profile', data={"phoneNumber": "1234567890", "aboutMe": aboutMe, "saveButton" : "1"}, follow_redirects=True)
        assert response.status_code == 200
        response = client.post('/profile', data={"phoneNumber": "1234567890", "aboutMe": aboutMe2, "saveButton" : "1"}, follow_redirects=True)
        assert response.status_code == 200
        assert aboutMe2 in response.text

'''
This function checks if the user wants to edit their phone number
and about me and the new phone number and about me is displayed
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_profile_edit_phonenumber_and_about_me(mock_token, mock_email, client):
    # send data to signup using post method
    # redirects to email confirmation
    username = "validt@syr.edu"
    first_name = "Bobby"
    last_name = "Goldstein"
    response = client.post("/signup", data={"first_name": first_name, "last_name": last_name,
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        # send data to login using post method with the right token redirection which is 1234
        # logged in by clicking the link in the confirmation email and not manipulating the token
        # therefore the user is redirected to the dashboard page  
        response = client.post('/login?t=1234', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified
        assert response.status_code == 200
        assert response.request.path == '/dashboard' 

        # Go to the profile page to check these fields
        # Enter phone number via post data and save it 
        # Redirect to dashboard page
        # Go to profile page to ensure change has been made 
        assert response.status_code == 200
        response = client.get('/profile')
        phoneNumber = "1234567890"
        phoneNumber2 = "56765567"
        aboutMe = "Hi, my name is Bob and I like computer science"
        aboutMe2 = "Hi, my name is Bob and I like music"
        assert response.status_code == 200
        assert response.request.path == '/profile'
        assert current_user.first_name == user.first_name
        assert current_user.last_name == user.last_name
        assert current_user.username == user.username
        response = client.post('/profile', data={"phoneNumber": phoneNumber, "aboutMe": aboutMe, "saveButton" : "1"}, follow_redirects=True)
        assert response.status_code == 200
        response = client.post('/profile', data={"phoneNumber": phoneNumber2, "aboutMe": aboutMe2, "saveButton" : "1"}, follow_redirects=True)
        assert response.status_code == 200
        assert phoneNumber2 in response.text
        assert aboutMe2 in response.text

'''
This function checks for the character limit in phone number
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_profile_phonenumber_char_limit_error(mock_token, mock_email, client):
    # send data to signup using post method
    # redirects to email confirmation
    username = "validt@syr.edu"
    first_name = "Bobby"
    last_name = "Goldstein"
    response = client.post("/signup", data={"first_name": first_name, "last_name": last_name,
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        # send data to login using post method with the right token redirection which is 1234
        # logged in by clicking the link in the confirmation email and not manipulating the token
        # therefore the user is redirected to the dashboard page  
        response = client.post('/login?t=1234', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified
        assert response.status_code == 200
        assert response.request.path == '/dashboard' 

        # Go to the profile page to check these fields
        # Enter phone number via post data and save it 
        # Redirect to dashboard page
        # Go to profile page to ensure change has been made 
        assert response.status_code == 200
        response = client.get('/profile')
        phoneNumber = "12345678904545646545644565656"
        assert response.status_code == 200
        assert response.request.path == '/profile'
        assert current_user.first_name == user.first_name
        assert current_user.last_name == user.last_name
        assert current_user.username == user.username
        response = client.post('/profile', data={"phoneNumber": phoneNumber, "aboutMe": "hello world", "saveButton" : "1"}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Invalid phone number, please use digits and less than 15 characters" in response.data


'''
This function checks if the phone number is not numeric 
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_profile_phonenumber_numeric_limit_error(mock_token, mock_email, client):
    # send data to signup using post method
    # redirects to email confirmation
    username = "validt@syr.edu"
    first_name = "Bobby"
    last_name = "Goldstein"
    response = client.post("/signup", data={"first_name": first_name, "last_name": last_name,
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        # send data to login using post method with the right token redirection which is 1234
        # logged in by clicking the link in the confirmation email and not manipulating the token
        # therefore the user is redirected to the dashboard page  
        response = client.post('/login?t=1234', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified
        assert response.status_code == 200
        assert response.request.path == '/dashboard' 

        # Go to the profile page to check these fields
        # Enter phone number via post data and save it 
        # Redirect to dashboard page
        # Go to profile page to ensure change has been made 
        assert response.status_code == 200
        response = client.get('/profile')
        phoneNumber = "123abcdef"
        assert response.status_code == 200
        assert response.request.path == '/profile'
        assert current_user.first_name == user.first_name
        assert current_user.last_name == user.last_name
        assert current_user.username == user.username
        response = client.post('/profile', data={"phoneNumber": phoneNumber, "aboutMe": "hello world", "saveButton" : "1"}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Invalid phone number, please use digits and less than 15 characters" in response.data

'''
This function checks the character limit for aboutMe
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_profile_aboutMe_char_limit_error(mock_token, mock_email, client):
    # send data to signup using post method
    # redirects to email confirmation
    username = "validt@syr.edu"
    first_name = "Bobby"
    last_name = "Goldstein"
    response = client.post("/signup", data={"first_name": first_name, "last_name": last_name,
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        # send data to login using post method with the right token redirection which is 1234
        # logged in by clicking the link in the confirmation email and not manipulating the token
        # therefore the user is redirected to the dashboard page  
        response = client.post('/login?t=1234', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified
        assert response.status_code == 200
        assert response.request.path == '/dashboard' 

        # Go to the profile page to check these fields
        # Enter phone number via post data and save it 
        # Redirect to dashboard page
        # Go to profile page to ensure change has been made 
        assert response.status_code == 200
        response = client.get('/profile')
        aboutMe = "My favorite soup is creamy tomato bisque with grilled cheese."
        assert response.status_code == 200
        assert response.request.path == '/profile'
        assert current_user.first_name == user.first_name
        assert current_user.last_name == user.last_name
        assert current_user.username == user.username
        response = client.post('/profile', data={"phoneNumber": "1234567890", "aboutMe": aboutMe, "saveButton" : "1"}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Invalid, the maximum character limit for about me description is 50" in response.data

'''
This function tests if the phoneNumber and aboutMe fields are not changed 
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_profile_unchanged_phonenumber_and_about_me(mock_token, mock_email, client):
    # send data to signup using post method
    # redirects to email confirmation
    username = "validt@syr.edu"
    first_name = "Bobby"
    last_name = "Goldstein"
    response = client.post("/signup", data={"first_name": first_name, "last_name": last_name,
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        # send data to login using post method with the right token redirection which is 1234
        # logged in by clicking the link in the confirmation email and not manipulating the token
        # therefore the user is redirected to the dashboard page  
        response = client.post('/login?t=1234', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified
        assert response.status_code == 200
        assert response.request.path == '/dashboard' 

        # Go to the profile page to check these fields
        # Enter phone number via post data and save it 
        # Redirect to dashboard page
        # Go to profile page to ensure change has been made 
        assert response.status_code == 200
        response = client.get('/profile')
        phoneNumber = "1234567890"
        phoneNumber2 = "1234567890"
        aboutMe = "Hi, my name is Bob and I like computer science"
        aboutMe2 = "Hi, my name is Bob and I like computer science"
        assert response.status_code == 200
        assert response.request.path == '/profile'
        assert current_user.first_name == user.first_name
        assert current_user.last_name == user.last_name
        assert current_user.username == user.username
        response = client.post('/profile', data={"phoneNumber": phoneNumber, "aboutMe": aboutMe, "saveButton" : "1"}, follow_redirects=True)
        assert response.status_code == 200
        response = client.post('/profile', data={"phoneNumber": phoneNumber2, "aboutMe": aboutMe2, "saveButton" : "1"}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Phone number and about me description not changed" in response.data

