from app.auth import email_content_password_reset, url_for, send_email
from unittest import mock
import random
from app.models.user import User

def test_forgot_email_not_registered_user(client):
    # The user is not registered in the system, 
    # send post data of a username to the forgot page that doesn't exist.
    # assert b "the error message" in response.data
    username = "notexistent@syr.edu"
    response = client.post("/forgot", data={"username": username}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Your email is not registered" in response.data


@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_forgot_email_not_verified(mock_token, mock_email, client):
    # The user is registered in the system,
    # send post data of signup credentials
    # mock the email of signup
    # didn't click link
    # send post data to forgot page with username
    # assert b "error message" in response.data
    username = "existent@syr.edu"
    response = client.post("/signup", data={"first_name": "Matt", "last_name": "Jones",
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'
    response = client.post("/forgot", data={"username": username}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Your email is not verified" in response.data


@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_forgot_email_is_registered_user(mock_token, mock_email, client):
    # The user is registered in the system,
    # send post data of signup credentials
    # mock the email of signup
    # clicked the link
    # redirects to login page with right token enter same credientials 
    # send post data to forgot page with username
    # assert redirection page is true
    username = "existent@syr.edu"
    response = client.post("/signup", data={"first_name": "Matt", "last_name": "Jones",
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        response = client.post('/login?t=1234', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified
        assert response.request.path == '/dashboard'
        response = client.post("/forgot", data={"username": username}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/forgotconfirmation'

@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_forgot_email_is_registered_user_invalid_email(mock_token, mock_email, client):
    # The user is registered in the system,
    # send post data of signup credentials
    # mock the email of signup
    # clicked the link
    # redirects to login page with right token enter same credientials 
    # send post data to forgot page with invalid username
    # assert redirection page is true
    username = "existent@syr.edu"
    invalid_username = "nonexistent@syr.edu"
    response = client.post("/signup", data={"first_name": "Matt", "last_name": "Jones",
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        response = client.post('/login?t=1234', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified
        assert response.request.path == '/dashboard'
        response = client.post("/forgot", data={"username": invalid_username}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/forgot'
        assert b"Your email is not registered" in response.data 


def test_reset_password_not_registered_user(client):
    # The user is not registered in the system, 
    # send post data of a username to the reset password page that doesn't exist.
    # assert b "the error message" in response.data
    username = "notexistent@syr.edu"
    response = client.post("/reset_password", data={"username": username, "password": "ge415",
                                                    "re_enter_password": "ge415"}, follow_redirects=True)
    assert b"Invalid User" in response.data


@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_reset_password_re_enter_password_not_match(mock_token, mock_email, client):
    # The user is registered in the system,
    # send post data of signup credentials
    # mock the email of signup
    # clicked the link
    # redirects to login page with right token enter same credientials 
    # send post data to forgot page with username
    # assert redirection page is true 
    # mock the email for password reset and clicked the link 
    # send post data to reset_password with the re-enter of passwords not matching
    # assert b the error message

    username = "existent@syr.edu"
    response = client.post("/signup", data={"first_name": "Matt", "last_name": "Jones",
                                            "username": username, "password": "ge415",
                                            "re_enter_password": "ge415"}, follow_redirects=True)
    
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        response = client.post('/login?t=1234', data={"username": username , "password": "ge415"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified
        assert response.request.path == '/dashboard'
        response = client.post("/forgot", data={"username": username}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/forgotconfirmation'
        response = client.post("/reset_password?t1234", data={"username": username, "password": "ge415",
                                                    "re_enter_password": "abc415"}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/reset_password'
        assert b"Passwords do not match, try again." in response.data



@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_reset_password_invalid_token(mock_token, mock_email, client):
    # The user is registered in the system,
    # send post data of signup credentials
    # mock the email of signup
    # clicked the link
    # redirects to login page with right token enter same credientials 
    # send post data to forgot page with username
    # assert redirection page is true 
    # mock the email for password reset and did click the link 
    # manipulated the token 
    # assert b error message

    username = "existent@syr.edu"
    response = client.post("/signup", data={"first_name": "Matt", "last_name": "Jones",
                                            "username": username, "password": "ge415",
                                            "re_enter_password": "ge415"}, follow_redirects=True)
    
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        response = client.post('/login?t=1234', data={"username": username , "password": "ge415"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified
        assert response.request.path == '/dashboard'
        response = client.post("/forgot", data={"username": username}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/forgotconfirmation'
        response = client.post("/reset_password?t=4321", data={"username": username, "password": "ge415",
                                                    "re_enter_password": "ge415"}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/reset_password'
        assert b"Invalid token" in response.data


@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_reset_password_empty_token(mock_token, mock_email, client):
    # The user is registered in the system,
    # send post data of signup credentials
    # mock the email of signup
    # clicked the link
    # redirects to login page with right token enter same credientials 
    # send post data to forgot page with username
    # assert redirection page is true 
    # mock the email for password reset and did not click the link 
    # assert b error message
    username = "existent@syr.edu"
    response = client.post("/signup", data={"first_name": "Matt", "last_name": "Jones",
                                            "username": username, "password": "ge415",
                                            "re_enter_password": "ge415"}, follow_redirects=True)
    
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        response = client.post('/login?t=1234', data={"username": username , "password": "ge415"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified
        assert response.request.path == '/dashboard'
        response = client.post("/forgot", data={"username": username}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/forgotconfirmation'
        response = client.post("/reset_password", data={"username": username, "password": "ge415",
                                                    "re_enter_password": "ge415"}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/reset_password'
        assert b"Empty token" in response.data


@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_reset_password_success(mock_token, mock_email, client):
    # The user is registered in the system,
    # send post data of signup credentials
    # mock the email of signup
    # clicked the link
    # redirects to login page with right token enter same credientials 
    # send post data to forgot page with username
    # assert redirection page is true 
    # mock the email for password reset and click the link
    # enter valid credentials in password reset page
    # redirect to login page
    # enter new credentials  
    # assert redirected to dashboard
    username = "existent@syr.edu"
    response = client.post("/signup", data={"first_name": "Matt", "last_name": "Jones",
                                            "username": username, "password": "ge415",
                                            "re_enter_password": "ge415"}, follow_redirects=True)
    
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        response = client.post('/login?t=1234', data={"username": username , "password": "ge415"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified
        assert response.request.path == '/dashboard'
        response = client.post("/forgot", data={"username": username}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/forgotconfirmation'
        response = client.post("/reset_password?t=1234", data={"username": username, "password": "ge415",
                                                    "re_enter_password": "ge415"}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/login'
        response = client.post('/login', data={"username": username , "password": "ge415"}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/dashboard'

