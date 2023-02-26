## Author: Talal Hakki
from flask import url_for, request
from app.auth import email_content_password_reset, url_for, send_email
from unittest import mock
import random
from app.models.user import User
from app.models.studyinterest import *
from app.subjectselection import *
import pytest

'''
This function tests if you can add one subject to your subject list
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_single_subject(mock_token, mock_email, client):
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

        assert si.course.subject_code == course.subject_code
        assert si.course.course_number == course.course_number
        assert si.course.course_name == course.course_name 
        assert si.pro_score == 2.00

        assert response.request.path == '/subjectselection'


'''
This function tests if you can add two subject to your subject list
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_two_subject(mock_token, mock_email, client):
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

        assert si.course.subject_code == course.subject_code
        assert si.course.course_number == course.course_number
        assert si.course.course_name == course.course_name 
        assert si.pro_score == 2.00
        
        assert response.request.path == '/subjectselection'

        # user selecting a second course

        course = Course.query.filter_by(subject_code="BIO").first()
        course_id = course.id

        response = client.post('/subjectselection', 
                               data={"subject_code": "BIO", "course_title": course_id, "pro_ans1": "3", "pro_ans2": "3", "pro_ans3" : "3", "but" : "1"}, follow_redirects=True)
        si2 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        assert si2.course.subject_code == course.subject_code
        assert si2.course.course_number == course.course_number
        assert si2.course.course_name == course.course_name 
        assert si2.pro_score == 3.00

        assert response.request.path == '/subjectselection'


'''
This function tests if you can add three subject to your subject list
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_three_subject(mock_token, mock_email, client):
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

        assert si.course.subject_code == course.subject_code
        assert si.course.course_number == course.course_number
        assert si.course.course_name == course.course_name 
        assert si.pro_score == 2.00    

        assert response.request.path == '/subjectselection'

        # user selecting a second course

        course = Course.query.filter_by(subject_code="BIO").first()
        course_id = course.id

        response = client.post('/subjectselection', 
                               data={"subject_code": "BIO", "course_title": course_id, "pro_ans1": "3", "pro_ans2": "3", "pro_ans3" : "3", "but" : "1"}, follow_redirects=True)
        si2 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        assert si2.course.subject_code == course.subject_code
        assert si2.course.course_number == course.course_number
        assert si2.course.course_name == course.course_name 
        assert si2.pro_score == 3.00
        
        assert response.request.path == '/subjectselection'

        # user selecting a third course

        course = Course.query.filter_by(subject_code="ACC").first()
        course_id = course.id

        response = client.post('/subjectselection', 
                               data={"subject_code": "ACC", "course_title": course_id, "pro_ans1": "4", "pro_ans2": "4", "pro_ans3" : "4", "but" : "1"}, follow_redirects=True)
        si3 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        assert si3.course.subject_code == course.subject_code
        assert si3.course.course_number == course.course_number
        assert si3.course.course_name == course.course_name 
        assert si3.pro_score == 4.00

        assert response.request.path == '/subjectselection'


'''
This function tests if you can add four subject to your subject list
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_four_subject(mock_token, mock_email, client):
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

        assert si.course.subject_code == course.subject_code
        assert si.course.course_number == course.course_number
        assert si.course.course_name == course.course_name 
        assert si.pro_score == 2.00
        
        assert response.request.path == '/subjectselection'

        # user selecting a second course

        course = Course.query.filter_by(subject_code="BIO").first()
        course_id = course.id

        response = client.post('/subjectselection', 
                               data={"subject_code": "BIO", "course_title": course_id, "pro_ans1": "3", "pro_ans2": "3", "pro_ans3" : "3", "but" : "1"}, follow_redirects=True)
        si2 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        assert si2.course.subject_code == course.subject_code
        assert si2.course.course_number == course.course_number
        assert si2.course.course_name == course.course_name 
        assert si2.pro_score == 3.00

        assert response.request.path == '/subjectselection'

        # user selecting a third course

        course = Course.query.filter_by(subject_code="ACC").first()
        course_id = course.id

        response = client.post('/subjectselection', 
                               data={"subject_code": "ACC", "course_title": course_id, "pro_ans1": "4", "pro_ans2": "4", "pro_ans3" : "4", "but" : "1"}, follow_redirects=True)
        si3 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        assert si3.course.subject_code == course.subject_code
        assert si3.course.course_number == course.course_number
        assert si3.course.course_name == course.course_name 
        assert si3.pro_score == 4.00

        assert response.request.path == '/subjectselection'

        # user selecting a fourth course

        course = Course.query.filter_by(subject_code="ARB").first()
        course_id = course.id
        response = client.post('/subjectselection', 
                               data={"subject_code": "ARB", "course_title": course_id, "pro_ans1": "1", "pro_ans2": "2", "pro_ans3" : "3", "but" : "1"}, follow_redirects=True)
        si4 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        assert si4.course.subject_code == course.subject_code
        assert si4.course.course_number == course.course_number
        assert si4.course.course_name == course.course_name 
        assert si4.pro_score == 2.00

        assert response.request.path == '/subjectselection'

'''
This function tests if you can add five subject to your subject list
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_five_subject(mock_token, mock_email, client):
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

        assert si.course.subject_code == course.subject_code
        assert si.course.course_number == course.course_number
        assert si.course.course_name == course.course_name 
        assert si.pro_score == 2.00

        assert response.request.path == '/subjectselection'

        # user selecting a second course

        course = Course.query.filter_by(subject_code="BIO").first()
        course_id = course.id

        response = client.post('/subjectselection', 
                               data={"subject_code": "BIO", "course_title": course_id, "pro_ans1": "3", "pro_ans2": "3", "pro_ans3" : "3", "but" : "1"}, follow_redirects=True)
        si2 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()


        assert si2.course.subject_code == course.subject_code
        assert si2.course.course_number == course.course_number
        assert si2.course.course_name == course.course_name 
        assert si2.pro_score == 3.00
        

        assert response.request.path == '/subjectselection'

        # user selecting a third course

        course = Course.query.filter_by(subject_code="ACC").first()
        course_id = course.id

        response = client.post('/subjectselection', 
                               data={"subject_code": "ACC", "course_title": course_id, "pro_ans1": "4", "pro_ans2": "4", "pro_ans3" : "4", "but" : "1"}, follow_redirects=True)
        si3 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        assert si3.course.subject_code == course.subject_code
        assert si3.course.course_number == course.course_number
        assert si3.course.course_name == course.course_name 
        assert si3.pro_score == 4.00

        assert response.request.path == '/subjectselection'

        # user selecting a fourth course

        course = Course.query.filter_by(subject_code="ARB").first()
        course_id = course.id
        response = client.post('/subjectselection', 
                               data={"subject_code": "ARB", "course_title": course_id, "pro_ans1": "1", "pro_ans2": "2", "pro_ans3" : "3", "but" : "1"}, follow_redirects=True)
        si4 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        assert si4.course.subject_code == course.subject_code
        assert si4.course.course_number == course.course_number
        assert si4.course.course_name == course.course_name 
        assert si4.pro_score == 2.00

        assert response.request.path == '/subjectselection'

        # user selecting a fifth course

        course = Course.query.filter_by(subject_code="EAR").first()
        course_id = course.id

        response = client.post('/subjectselection', 
                               data={"subject_code": "EAR", "course_title": course_id, "pro_ans1": "2", "pro_ans2": "3", "pro_ans3" : "4", "but" : "1"}, follow_redirects=True)
        si5 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        assert si5.course.subject_code == course.subject_code
        assert si5.course.course_number == course.course_number
        assert si5.course.course_name == course.course_name 
        assert si5.pro_score == 3.00

        assert response.request.path == '/subjectselection'

'''
This function tests if you can add six subject to your subject list
(a user can only have up to 5 subjects)
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_six_subject(mock_token, mock_email, client):
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

        assert si.course.subject_code == course.subject_code
        assert si.course.course_number == course.course_number
        assert si.course.course_name == course.course_name 
        assert si.pro_score == 2.00
        
        assert response.request.path == '/subjectselection'

        # user selecting a second course

        course = Course.query.filter_by(subject_code="BIO").first()
        course_id = course.id
        response = client.post('/subjectselection', 
                               data={"subject_code": "BIO", "course_title": course_id, "pro_ans1": "3", "pro_ans2": "3", "pro_ans3" : "3", "but" : "1"}, follow_redirects=True)
        si2 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        assert si2.course.subject_code == course.subject_code
        assert si2.course.course_number == course.course_number
        assert si2.course.course_name == course.course_name 
        assert si2.pro_score == 3.00

        assert response.request.path == '/subjectselection'

        # user selecting a third course

        course = Course.query.filter_by(subject_code="ACC").first()
        course_id = course.id
        response = client.post('/subjectselection', 
                               data={"subject_code": "ACC", "course_title": course_id, "pro_ans1": "4", "pro_ans2": "4", "pro_ans3" : "4", "but" : "1"}, follow_redirects=True)
        si3 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        assert si3.course.subject_code == course.subject_code
        assert si3.course.course_number == course.course_number
        assert si3.course.course_name == course.course_name 
        assert si3.pro_score == 4.00

        assert response.request.path == '/subjectselection'

        # user selecting a fourth course

        course = Course.query.filter_by(subject_code="ARB").first()
        course_id = course.id
        response = client.post('/subjectselection', 
                               data={"subject_code": "ARB", "course_title": course_id, "pro_ans1": "1", "pro_ans2": "2", "pro_ans3" : "3", "but" : "1"}, follow_redirects=True)
        si4 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        assert si4.course.subject_code == course.subject_code
        assert si4.course.course_number == course.course_number
        assert si4.course.course_name == course.course_name 
        assert si4.pro_score == 2.00

        assert response.request.path == '/subjectselection'

        # user selecting a fifth course

        course = Course.query.filter_by(subject_code="EAR").first()
        course_id = course.id

        response = client.post('/subjectselection', 
                               data={"subject_code": "EAR", "course_title": course_id, "pro_ans1": "2", "pro_ans2": "3", "pro_ans3" : "4", "but" : "1"}, follow_redirects=True)
        si5 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        assert si5.course.subject_code == course.subject_code
        assert si5.course.course_number == course.course_number
        assert si5.course.course_name == course.course_name 
        assert si5.pro_score == 3.00

        assert response.request.path == '/subjectselection'

        # user selecting a sixth course (where the maximum number of courses for a user is five)

        course = Course.query.filter_by(subject_code="EEE").first()
        course_id = course.id
        response = client.post('/subjectselection', 
                               data={"subject_code": "EEE", "course_title": course_id, "pro_ans1": "1", "pro_ans2": "1", "pro_ans3" : "1", "but" : "1"}, follow_redirects=True)
        si6 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        assert si6 == None
        
        assert response.request.path == '/subjectselection'