# 
from app.auth import email_content_password_reset, url_for, send_email
from unittest import mock
import random
from app.models.user import User 

@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_login_email_verification_link_clicked(mock_token, mock_email, client):
    username = "validt@syr.edu"
    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein",
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

@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_login_invalid_token(mock_token, mock_email, client):
    username = "invalidt@syr.edu"
    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein",
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        response = client.post('/login?t=4321', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified == False
        assert response.request.path == '/login'
        assert b"Invalid token" in response.data   

def test_login_user_not_existing(client):
    response = client.post("/login", data={"username": "nonexistent@syr.edu", "password": "ge3456"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid Login" in response.data

@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_login_email_verification_link_not_clicked(mock_token, mock_email, client):
    username = "notoken@syr.edu"
    response = client.post("/signup", data={"first_name": "Bobby", "last_name": "Goldstein",
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        response = client.post('/login', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified == False
        assert response.request.path == '/login'
        assert b"Did not click on the link which was sent to your email" in response.data


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
        response = client.post('/login?t=1234', data={"username": username , "password": "abc675"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.token == '1234'
        assert user.is_verified == False
        assert response.request.path == '/login'
        assert b"Invalid Login" in response.data

