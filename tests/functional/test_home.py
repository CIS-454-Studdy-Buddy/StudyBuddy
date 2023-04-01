# Author: Aaron Alakkadan
from flask import url_for, request
from app.auth import home
from unittest import mock
from app.extensions import email

'''
The function test_home_is_presented tests if the information on the landing page is presented on the page
'''
def test_home_is_presented(client): 
    response = client.get("/")
    assert b"Studying alone? Find your Buddy Today!" in response.data
    assert b"Study buddy is a new application designed to help you achieve your goals" in response.data 
    assert b"during your college years. Making friends in your major is vital for a successful college" in response.data 
    assert b"experience," in response.data 
    assert b"and for students that embark on this journey alone, sometimes it can be tough to find buddies in" in response.data 
    assert b"their" in response.data
    assert b"classes. Study Buddy is here to help you make long lasting connections and to help make your" in response.data
    assert b"transition" in response.data
    assert b"and involvement in classes smoother." in response.data

'''
The function checks if the links on the home page redirects to the right corresponding page
'''
def test_home_links_work(client):
    response = client.get("/")
    assert "/login" in response.text
    assert "/signup" in response.text

'''
The function checks if the contact us form at the bottom of the home page sends an email to the correct email address
    with the correct information
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
def test_contact_us_email_send(mock_send, client):
    response = client.post("/", data={"name": "Matt", "email": "testingemail@syr.edu", 
                                      "subject": "Subject", "message": "Test message 11"}, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/'

    with client:
        assert mock_send.called == True
        assert mock_send.call_count == 1
        args = mock_send.call_args
        msg = args[0][0]
        assert msg.subject == "Subject"
        assert msg.recipients == ['su.study.buddy@gmail.com']
        assert msg.sender == 'su.study.buddy@gmail.com'
        assert msg.body == "Name: Matt\nEmail: testingemail@syr.edu\n\nTest message 11"
