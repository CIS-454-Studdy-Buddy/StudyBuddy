from flask import url_for, request
from app.auth import email_content_password_reset, url_for, send_email
from unittest import mock
import random
from app.models.user import User
from app.models.studyinterest import *
from app.subjectselection import *
import pytest

'''
This function tests if you can calculate a proficiency score based on the 3 proficiency answers
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_proficiency_pro_score_one(mock_token, mock_email, client):
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
        

        # Go to the subject selection page
        response = client.get('/subjectselection')
        assert response.status_code == 200
        assert response.request.path == '/subjectselection'
        course = Course.query.filter_by(subject_code="CIS").first()
        course_id = course.id
        user = User.query.filter_by(username=current_user.username).first()
       
        response = client.post('/subjectselection', 
                               data={"subject_code": "CIS", "course_title": course_id, "pro_ans1": "2", "pro_ans2": "2", "pro_ans3" : "2", "but" : "1"}, follow_redirects=True)
        si = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()
        assert pytest.approx(float(si.pro_score),0.1) == 2.00

'''
This function tests if you can calculate a proficiency score based on the 3 proficiency answers
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_proficiency_pro_score_two(mock_token, mock_email, client):
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
        

        # Go to the subject selection page
        response = client.get('/subjectselection')
        assert response.status_code == 200
        assert response.request.path == '/subjectselection'
        course = Course.query.filter_by(subject_code="CIS").first()
        course_id = course.id
        user = User.query.filter_by(username=current_user.username).first()
       
        response = client.post('/subjectselection', 
                               data={"subject_code": "CIS", "course_title": course_id, "pro_ans1": "2", "pro_ans2": "3", "pro_ans3" : "5", "but" : "1"}, follow_redirects=True)
        si = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()
        assert pytest.approx(float(si.pro_score), 0.1) == 3.33

'''
This function tests if you can calculate a proficiency score based on the 3 proficiency answers
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_proficiency_pro_score_three(mock_token, mock_email, client):
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
        

        # Go to the subject selection page
        response = client.get('/subjectselection')
        assert response.status_code == 200
        assert response.request.path == '/subjectselection'
        course = Course.query.filter_by(subject_code="CIS").first()
        course_id = course.id
        user = User.query.filter_by(username=current_user.username).first()
       
        response = client.post('/subjectselection', 
                               data={"subject_code": "CIS", "course_title": course_id, "pro_ans1": "4", "pro_ans2": "5", "pro_ans3" : "2", "but" : "1"}, follow_redirects=True)
        si = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()
        assert pytest.approx(float(si.pro_score), 0.1) == 3.66
