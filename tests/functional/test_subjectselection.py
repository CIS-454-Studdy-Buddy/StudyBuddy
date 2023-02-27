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
This function tests if the user can add one subject to their subject list 
and answer the proficiency test questions
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

        # testing if the selected subject and its average proficiency test score
        # is successfully saved to database
        assert si.course.subject_code == course.subject_code
        assert si.course.course_number == course.course_number
        assert si.course.course_name == course.course_name 
        assert si.pro_score == 2.00

        # testing if the selected subject and its averge proficiency test score
        # is successfully displayed to the user on the subjectselection web page
        assert course.subject_code in response.text
        assert course.course_number in response.text
        assert course.course_name in response.text
        assert str(si.pro_score) in response.text


        assert response.request.path == '/subjectselection'




'''
This function simulates the user adding 6 subjects. Given that a user can
only select a total of 5 subjects, this test demonstrates that when a user 
attempts to add a 6th subject, the 6th subject is not added to their course list
and an error message is displayed.
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

        # testing if the 1st selected subject and its average proficiency test score
        # is successfully saved to database
        assert si.course.subject_code == course.subject_code
        assert si.course.course_number == course.course_number
        assert si.course.course_name == course.course_name 
        assert si.pro_score == 2.00

        # testing if the 1st selected subject and its averge proficiency test score
        # is successfully displayed to the user on the subjectselection web page
        assert course.subject_code in response.text
        assert course.course_number in response.text
        assert course.course_name in response.text
        assert str(si.pro_score) in response.text
        
        assert response.request.path == '/subjectselection'

        # user selecting a second course

        course = Course.query.filter_by(subject_code="BIO").first()
        course_id = course.id
        response = client.post('/subjectselection', 
                               data={"subject_code": "BIO", "course_title": course_id, "pro_ans1": "3", "pro_ans2": "3", "pro_ans3" : "3", "but" : "1"}, follow_redirects=True)
        si2 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        # testing if the 2nd selected subject and its average proficiency test score
        # is successfully saved to database
        assert si2.course.subject_code == course.subject_code
        assert si2.course.course_number == course.course_number
        assert si2.course.course_name == course.course_name 
        assert si2.pro_score == 3.00

        # testing if the 2nd selected subject and its averge proficiency test score
        # is successfully displayed to the user on the subjectselection web page
        assert course.subject_code in response.text
        assert course.course_number in response.text
        assert course.course_name in response.text
        assert str(si2.pro_score) in response.text

        assert response.request.path == '/subjectselection'

        # user selecting a third course

        course = Course.query.filter_by(subject_code="ACC").first()
        course_id = course.id
        response = client.post('/subjectselection', 
                               data={"subject_code": "ACC", "course_title": course_id, "pro_ans1": "4", "pro_ans2": "4", "pro_ans3" : "4", "but" : "1"}, follow_redirects=True)
        si3 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        # testing if the 3rd selected subject and its average proficiency test score
        # is successfully saved to database
        assert si3.course.subject_code == course.subject_code
        assert si3.course.course_number == course.course_number
        assert si3.course.course_name == course.course_name 
        assert si3.pro_score == 4.00

        # testing if the 3rd selected subject and its averge proficiency test score
        # is successfully displayed to the user on the subjectselection web page
        assert course.subject_code in response.text
        assert course.course_number in response.text
        assert course.course_name in response.text
        assert str(si3.pro_score) in response.text

        assert response.request.path == '/subjectselection'

        # user selecting a fourth course

        course = Course.query.filter_by(subject_code="ARB").first()
        course_id = course.id
        response = client.post('/subjectselection', 
                               data={"subject_code": "ARB", "course_title": course_id, "pro_ans1": "1", "pro_ans2": "2", "pro_ans3" : "3", "but" : "1"}, follow_redirects=True)
        si4 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        # testing if the 4th selected subject and its average proficiency test score
        # is successfully saved to database
        assert si4.course.subject_code == course.subject_code
        assert si4.course.course_number == course.course_number
        assert si4.course.course_name == course.course_name 
        assert si4.pro_score == 2.00

        # testing if the 4th selected subject and its averge proficiency test score
        # is successfully displayed to the user on the subjectselection web page
        assert course.subject_code in response.text
        assert course.course_number in response.text
        assert course.course_name in response.text
        assert str(si4.pro_score) in response.text

        assert response.request.path == '/subjectselection'

        # user selecting a fifth course

        course = Course.query.filter_by(subject_code="EAR").first()
        course_id = course.id

        response = client.post('/subjectselection', 
                               data={"subject_code": "EAR", "course_title": course_id, "pro_ans1": "2", "pro_ans2": "3", "pro_ans3" : "4", "but" : "1"}, follow_redirects=True)
        si5 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        # testing if the 5th selected subject and its average proficiency test score
        # is successfully saved to database
        assert si5.course.subject_code == course.subject_code
        assert si5.course.course_number == course.course_number
        assert si5.course.course_name == course.course_name 
        assert si5.pro_score == 3.00

        # testing if the 5th selected subject and its averge proficiency test score
        # is successfully displayed to the user on the subjectselection web page
        assert course.subject_code in response.text
        assert course.course_number in response.text
        assert course.course_name in response.text
        assert str(si5.pro_score) in response.text

        assert response.request.path == '/subjectselection'

        # user selecting a sixth course (where the maximum number of courses for a user is five)

        course = Course.query.filter_by(subject_code="EEE").first()
        course_id = course.id
        response = client.post('/subjectselection', 
                               data={"subject_code": "EEE", "course_title": course_id, "pro_ans1": "1", "pro_ans2": "1", "pro_ans3" : "1", "but" : "1"}, follow_redirects=True)
        si6 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        # testing that the 6th selected subject and its average proficiency test score
        # is not saved to the database. This is because the maximum number of subjects
        # a user can have in thier course list is 5
        assert si6 == None

        # testing that a message is displayed to the user indicating that
        # they have already selected the maximum number of subjects (5 subjects)
        assert b"Maximum number of subjects selected" in response.data

        
        assert response.request.path == '/subjectselection'

'''
This function tests if the user can add one subject to their subject list 
and answer the proficiency test questions and also delete the subject
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=1234, autospec=True)
def test_delete_single_subject(mock_token, mock_email, client):
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
        to_be_deleted_course_id = course_id
        user = User.query.filter_by(username=current_user.username).first()
        response = client.post('/subjectselection', 
                               data={"subject_code": "CIS", "course_title": course_id, "pro_ans1": "2", "pro_ans2": "2", "pro_ans3" : "2", "but" : "1"}, follow_redirects=True)
        si = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        # testing if the selected subject and its average proficiency test score
        # is successfully saved to database
        assert si.course.subject_code == course.subject_code
        assert si.course.course_number == course.course_number
        assert si.course.course_name == course.course_name 
        assert si.pro_score == 2.00

        # testing if the selected subject and its averge proficiency test score
        # is successfully displayed to the user on the subjectselection web page
        assert course.subject_code in response.text
        assert course.course_number in response.text
        assert course.course_name in response.text
        assert str(si.pro_score) in response.text
        assert response.request.path == '/subjectselection'

         # user selecting a second course

        course = Course.query.filter_by(subject_code="BIO").first()
        course_id = course.id
        response = client.post('/subjectselection', 
                               data={"subject_code": "BIO", "course_title": course_id, "pro_ans1": "3", "pro_ans2": "3", "pro_ans3" : "3", "but" : "1"}, follow_redirects=True)
        si2 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()

        # testing if the 2nd selected subject and its average proficiency test score
        # is successfully saved to database
        assert si2.course.subject_code == course.subject_code
        assert si2.course.course_number == course.course_number
        assert si2.course.course_name == course.course_name 
        assert si2.pro_score == 3.00

        # testing if the selected subject is now deleted from the list
        course = Course.query.filter_by(subject_code="CIS").first()
        course_id =  to_be_deleted_course_id
        si = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course_id).first()
        to_be_deleted_subject_number = si.course.course_number
        to_be_deleted_course_name= si.course.course_name
        response = client.post('/subjectselection', 
                               data={"subject_remove": course_id, "delbut" : "1"}, follow_redirects=True)
        si2 = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course_id).first()
        assert si2 == None
        assert to_be_deleted_subject_number not in response.text
        assert to_be_deleted_course_name not in response.text
        assert response.request.path == '/subjectselection'