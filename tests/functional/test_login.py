'''
Author: Aaron Alakkadan 
'''
from app.auth import email_content_password_reset, url_for, send_email
from unittest import mock
import random
from app.models.user import User

'''
Test case for login email verification link clicked and successfully login
Mocks record how you use them, 
Allowing you to make assertions about what your code has done to them. 
The patch() decorators makes it easy to temporarily replace classes in a particular module with a Mock object   
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_login_email_verification_link_clicked(mock_token, mock_email, client):
    # send data to signup using post method
    # redirects to email confirmation
    username = "validt@syr.edu"
    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein",
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

'''
The function test_login_invalid_token is the test case for if they signup with the right credentials
but manipulated the token value   
''' 
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_login_invalid_token(mock_token, mock_email, client):
    # send data to signup using post method
    # redirects to email confirmation
    username = "invalidt@syr.edu"
    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein",
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click
        # sends data to login via post method
        # will not work becuse the token 4321 does not match the token 1234 therfore Invalid token error 
        response = client.post('/login?t=4321', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified == False
        assert response.request.path == '/login'
        assert b"Invalid token" in response.data   

'''
The function test_login_user_not_existing checks the test case of a user trying to login without signing
in first 
'''
def test_login_user_not_existing(client):
    # send data to login via post method
    # the user doesn't exist because they never signed up therefore throws Invalid Login error 
    response = client.post("/login", data={"username": "nonexistent@syr.edu", "password": "ge3456"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid Login" in response.data


'''
The function test_login_email_verification_link_not_clicked checks the test case where
the user signed in with valid credentials but never clicked the email confirmation link
therefore when they try to login an error message will be displayed 
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_login_email_verification_link_not_clicked(mock_token, mock_email, client):
    # send data to signup using post method
    # redirects to email confirmation
    username = "notoken@syr.edu"
    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein",
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        # sends data to login via post method
        # will not work because did not click the email verification link  
        response = client.post('/login', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified == False
        assert response.request.path == '/login'
        assert b"Did not click on the link which was sent to your email" in response.data

'''
The function test_login_password_not_matching tests is a user completes the signup process, email
verification process but fails to login because the password that they put in signup is a different password
that they have put in login
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_login_password_not_matching(mock_token, mock_email, client):
    username = "validt@syr.edu"
    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein",
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click
        # sends data to login via post method
        # will work because click the email verification link
        # redirected to login entered valid username but invalid password   
        response = client.post('/login?t=1234', data={"username": username , "password": "abc675"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified == False
        assert response.request.path == '/login'
        assert b"Invalid Login" in response.data

