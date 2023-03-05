## Author: Talal Hakki, Aaron Alakkadan 
from flask import url_for, request
from app.auth import email_content_password_reset, url_for, send_email
from unittest import mock
import random
from app.models.user import User
from app.models.studyinterest import *
from app.subjectselection import *
from app.models.buddyrelation import *
import pytest

'''
This function tests if the second user can find select a buddy (first user)
based on subject selection
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=5678, autospec=True)
def test_find_buddy_subject_selection(mock_token2, mock_email, client):
    # send data to signup using post method
    # redirects to email confirmation
    
    username = "validt@syr.edu"
    first_name = "Bobby"
    last_name = "Goldstein"
    response = client.post("/signup", data={"first_name": first_name, "last_name": last_name,
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        # send data to login using post method with the right token redirection which is 1234
        # logged in by clicking the link in the confirmation email and not manipulating the token
        # therefore the user is redirected to the dashboard page  
        response = client.post('/login?t=5678', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user_receiver = User.query.filter_by(username=username).first()
        assert user_receiver.username == username
        assert user_receiver.token == '5678'
        assert user_receiver.is_verified
        assert response.request.path == '/dashboard'

        # Go to the subject selection page
        response = client.get('/subjectselection')
        assert response.status_code == 200
        assert response.request.path == '/subjectselection'
        course = Course.query.filter_by(subject_code="CIS").first()
        course_id = course.id
        user_receiver = User.query.filter_by(username=current_user.username).first()
        response = client.post('/subjectselection', 
                               data={"subject_code": "CIS", "course_title": course_id, "pro_ans1": "2", "pro_ans2": "2", "pro_ans3" : "2", "but" : "1"}, follow_redirects=True)
        si_receiver = StudyInterest.query.filter_by(user_id=user_receiver.id).filter_by(course_id=course_id).first()

        assert si_receiver.course.course_name == course.course_name 

        response = client.get('/logout')
        assert response.request.path == '/logout'
       
        session.clear()
        
    
    #2nd USER
    response = client.get('/')
    assert response.request.path == '/'
    with mock.patch("random.randint", return_value='1234', autospec=True):
        
        username2 = "testing@syr.edu"
        first_name2 = "James"
        last_name2 = "Albert"
        response2 = client.post("/signup", data={"first_name": first_name2, "last_name": last_name2, 
                                            "username": username2, "password": "ab1234", 
                                            "re_enter_password": "ab1234"}, follow_redirects=True)

        assert response2.status_code == 200 
        assert response2.request.path == '/emailconfirmation'

        with client:
            # Simulate email verification click 
            # send data to login using post method with the right token redirection which is 1234
            # logged in by clicking the link in the confirmation email and not manipulating the token
            # therefore the user is redirected to the dashboard page  
            response2 = client.post('/login?t=1234', data={"username": username2 , "password": "ab1234"}, follow_redirects=True)
            assert response2.status_code == 200
            user_sender = User.query.filter_by(username=username2).first()
            assert user_sender.username == username2
            assert user_sender.token == '1234'
            assert user_sender.is_verified
            assert response2.request.path == '/dashboard'

            # Go to the subject selection page
            response2 = client.get('/subjectselection')
            assert response2.status_code == 200
            assert response2.request.path == '/subjectselection'
            user_sender = User.query.filter_by(username=current_user.username).first()
            response2 = client.post('/subjectselection', 
                               data={"subject_code": "CIS", "course_title": course_id, "pro_ans1": "2", "pro_ans2": "2", "pro_ans3" : "2", "but" : "1"}, follow_redirects=True)
            si_sender = StudyInterest.query.filter_by(user_id=user_sender.id).filter_by(course_id=course_id).first()

            assert si_sender.course.course_name == course.course_name 

            ## Go to findstudybuddy page
            ## select subject and check if users that have selected the subject and their avg. score are displayed on page
            ## Also check when they select for a buddy that the invitation status has chnaged and thenn nget redirected to the confirmation page

            response2 = client.get('/findstudybuddy')
            assert response2.status_code == 200
            assert response2.request.path == '/findstudybuddy'

            response2 = client.post('/findstudybuddy', 
                               data={"subject_code": course_id, "buddy_but" : "1", "select_buddy": user_receiver.id}, follow_redirects=True)
            

            si_receiver = StudyInterest.query.filter_by(user_id=user_receiver.id).filter_by(course_id=course_id).first()

            assert si_receiver.buddy_status == 'N'
            assert si_receiver.user.first_name in response2.text
            assert si_receiver.user.last_name in response2.text
            assert str(si_receiver.pro_score) in response2.text

        
            response2 = client.post('/findstudybuddy', 
                               data={"subject_code": course_id, "select_buddy": user_receiver.id, "select_buddy_but" : "1"}, follow_redirects=True)
        
            br = BuddyRelation.query.filter_by(buddy_sender=user_sender.id, buddy_receiver=user_receiver.id, study_interest_id=si_receiver.id).first()
            
            assert br.invitation_status == 'S'
            assert response2.request.path == '/findbuddyconfirmation'
            assert b"Pending Buddy Relation Status" in response2.data
            assert b"Invitation has been sent, you will be notified when buddy responds" in response2.data


'''
This function tests if the second user can find select a buddy (first user)
based on subject selection and proficiency score filters 
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=5678, autospec=True)
def test_find_buddy_subject_selection_and_pro_score(mock_token2, mock_email, client):
    # send data to signup using post method
    # redirects to email confirmation
    
    username = "validt@syr.edu"
    first_name = "Bobby"
    last_name = "Goldstein"
    response = client.post("/signup", data={"first_name": first_name, "last_name": last_name,
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        # send data to login using post method with the right token redirection which is 1234
        # logged in by clicking the link in the confirmation email and not manipulating the token
        # therefore the user is redirected to the dashboard page  
        response = client.post('/login?t=5678', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user_receiver = User.query.filter_by(username=username).first()
        assert user_receiver.username == username
        assert user_receiver.token == '5678'
        assert user_receiver.is_verified
        assert response.request.path == '/dashboard'

        # Go to the subject selection page
        response = client.get('/subjectselection')
        assert response.status_code == 200
        assert response.request.path == '/subjectselection'
        course = Course.query.filter_by(subject_code="CIS").first()
        course_id = course.id
        user_receiver = User.query.filter_by(username=current_user.username).first()
        response = client.post('/subjectselection', 
                               data={"subject_code": "CIS", "course_title": course_id, "pro_ans1": "2", "pro_ans2": "2", "pro_ans3" : "2", "but" : "1"}, follow_redirects=True)
        si_receiver = StudyInterest.query.filter_by(user_id=user_receiver.id).filter_by(course_id=course_id).first()

        assert si_receiver.course.course_name == course.course_name 

        response = client.get('/logout')
        assert response.request.path == '/logout'
       
        session.clear()
        
    
    #2nd USER
    response = client.get('/')
    assert response.request.path == '/'
    with mock.patch("random.randint", return_value='1234', autospec=True):
        
        username2 = "testing@syr.edu"
        first_name2 = "James"
        last_name2 = "Albert"
        response2 = client.post("/signup", data={"first_name": first_name2, "last_name": last_name2, 
                                            "username": username2, "password": "ab1234", 
                                            "re_enter_password": "ab1234"}, follow_redirects=True)

        assert response2.status_code == 200 
        assert response2.request.path == '/emailconfirmation'

        with client:
            # Simulate email verification click 
            # send data to login using post method with the right token redirection which is 1234
            # logged in by clicking the link in the confirmation email and not manipulating the token
            # therefore the user is redirected to the dashboard page  
            response2 = client.post('/login?t=1234', data={"username": username2 , "password": "ab1234"}, follow_redirects=True)
            assert response2.status_code == 200
            user_sender = User.query.filter_by(username=username2).first()
            assert user_sender.username == username2
            assert user_sender.token == '1234'
            assert user_sender.is_verified
            assert response2.request.path == '/dashboard'

            # Go to the subject selection page
            response2 = client.get('/subjectselection')
            assert response2.status_code == 200
            assert response2.request.path == '/subjectselection'
            user_sender = User.query.filter_by(username=current_user.username).first()
            response2 = client.post('/subjectselection', 
                               data={"subject_code": "CIS", "course_title": course_id, "pro_ans1": "2", "pro_ans2": "2", "pro_ans3" : "2", "but" : "1"}, follow_redirects=True)
            si_sender = StudyInterest.query.filter_by(user_id=user_sender.id).filter_by(course_id=course_id).first()

            assert si_sender.course.course_name == course.course_name 

            ## Go to findstudybuddy page
            ## select subject and proficency score and also check if users that have selected the subject and their avg. score are displayed on page
            ## Also check when they select for a buddy that the invitation status has chnaged and thenn nget redirected to the confirmation page

            response2 = client.get('/findstudybuddy')
            assert response2.status_code == 200
            assert response2.request.path == '/findstudybuddy'

            response2 = client.post('/findstudybuddy', 
                               data={"subject_code": course_id, "prof_select": "1", "buddy_but" : "1", "select_buddy": user_receiver.id}, follow_redirects=True)
            

            si_receiver = StudyInterest.query.filter_by(user_id=user_receiver.id).filter_by(course_id=course_id).first()

            assert si_receiver.buddy_status == 'N'
            assert si_receiver.user.first_name in response2.text
            assert si_receiver.user.last_name in response2.text
            assert str(si_receiver.pro_score) in response2.text

        
            response2 = client.post('/findstudybuddy', 
                               data={"subject_code": course_id, "select_buddy": user_receiver.id, "select_buddy_but" : "1"}, follow_redirects=True)
        
            br = BuddyRelation.query.filter_by(buddy_sender=user_sender.id, buddy_receiver=user_receiver.id, study_interest_id=si_receiver.id).first()
            
            assert br.invitation_status == 'S'
            assert response2.request.path == '/findbuddyconfirmation'
            assert b"Pending Buddy Relation Status" in response2.data
            assert b"Invitation has been sent, you will be notified when buddy responds" in response2.data


'''
This function tests if the second user can find select a buddy (first user)
based on multiple subject selection and proficiency score filters 
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=5678, autospec=True)
def test_find_buddy_multi_subject_selection_and_pro_score(mock_token2, mock_email, client):
    # send data to signup using post method
    # redirects to email confirmation
    
    username = "validt@syr.edu"
    first_name = "Bobby"
    last_name = "Goldstein"
    response = client.post("/signup", data={"first_name": first_name, "last_name": last_name,
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        # send data to login using post method with the right token redirection which is 1234
        # logged in by clicking the link in the confirmation email and not manipulating the token
        # therefore the user is redirected to the dashboard page  
        response = client.post('/login?t=5678', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user_receiver = User.query.filter_by(username=username).first()
        assert user_receiver.username == username
        assert user_receiver.token == '5678'
        assert user_receiver.is_verified
        assert response.request.path == '/dashboard'

        # Go to the subject selection page
        response = client.get('/subjectselection')
        assert response.status_code == 200
        assert response.request.path == '/subjectselection'
        course = Course.query.filter_by(subject_code="CIS").first()
        course_id = course.id
        user_receiver = User.query.filter_by(username=current_user.username).first()
        response = client.post('/subjectselection', 
                               data={"subject_code": "CIS", "course_title": course_id, "pro_ans1": "2", "pro_ans2": "2", "pro_ans3" : "2", "but" : "1"}, follow_redirects=True)
        si_receiver = StudyInterest.query.filter_by(user_id=user_receiver.id).filter_by(course_id=course_id).first()

        assert si_receiver.course.course_name == course.course_name

        # Select another subject
        course = Course.query.filter_by(subject_code="EAR").first()
        course_id = course.id

        response = client.post('/subjectselection', 
                               data={"subject_code": "EAR", "course_title": course_id, "pro_ans1": "3", "pro_ans2": "3", "pro_ans3" : "3", "but" : "1"}, follow_redirects=True)
        si_receiver2 = StudyInterest.query.filter_by(user_id=user_receiver.id).filter_by(course_id=course.id).first()
        assert si_receiver2.course.course_name == course.course_name

        response = client.get('/logout')
        assert response.request.path == '/logout'
       
        session.clear()
        
    
    #2nd USER
    response = client.get('/')
    assert response.request.path == '/'
    with mock.patch("random.randint", return_value='1234', autospec=True):
        
        username2 = "testing@syr.edu"
        first_name2 = "James"
        last_name2 = "Albert"
        response2 = client.post("/signup", data={"first_name": first_name2, "last_name": last_name2, 
                                            "username": username2, "password": "ab1234", 
                                            "re_enter_password": "ab1234"}, follow_redirects=True)

        assert response2.status_code == 200 
        assert response2.request.path == '/emailconfirmation'

        with client:
            # Simulate email verification click 
            # send data to login using post method with the right token redirection which is 1234
            # logged in by clicking the link in the confirmation email and not manipulating the token
            # therefore the user is redirected to the dashboard page  
            response2 = client.post('/login?t=1234', data={"username": username2 , "password": "ab1234"}, follow_redirects=True)
            assert response2.status_code == 200
            user_sender = User.query.filter_by(username=username2).first()
            assert user_sender.username == username2
            assert user_sender.token == '1234'
            assert user_sender.is_verified
            assert response2.request.path == '/dashboard'

            # Go to the subject selection page
            response2 = client.get('/subjectselection')
            assert response2.status_code == 200
            assert response2.request.path == '/subjectselection'
            user_sender = User.query.filter_by(username=current_user.username).first()
            response2 = client.post('/subjectselection', 
                               data={"subject_code": "CIS", "course_title": course_id, "pro_ans1": "2", "pro_ans2": "2", "pro_ans3" : "2", "but" : "1"}, follow_redirects=True)
            si_sender = StudyInterest.query.filter_by(user_id=user_sender.id).filter_by(course_id=course_id).first()

            assert si_sender.course.course_name == course.course_name 

            # Select another subject
            course = Course.query.filter_by(subject_code="EAR").first()
            course_id = course.id

            response = client.post('/subjectselection', 
                               data={"subject_code": "EAR", "course_title": course_id, "pro_ans1": "1", "pro_ans2": "1", "pro_ans3" : "1", "but" : "1"}, follow_redirects=True)
            si_sender2 = StudyInterest.query.filter_by(user_id=user_sender.id).filter_by(course_id=course.id).first()

            assert si_sender2.course.course_name == course.course_name

            ## Go to findstudybuddy page
            ## select subject and proficency score and also check if users that have selected the subject and their avg. score are displayed on page
            ## Also check when they select for a buddy that the invitation status has chnaged and thenn nget redirected to the confirmation page

            response2 = client.get('/findstudybuddy')
            assert response2.status_code == 200
            assert response2.request.path == '/findstudybuddy'

            response2 = client.post('/findstudybuddy', 
                               data={"subject_code": course_id, "prof_select": "2", "buddy_but" : "1", "select_buddy": user_receiver.id}, follow_redirects=True)
            

            si_receiver2 = StudyInterest.query.filter_by(user_id=user_receiver.id).filter_by(course_id=course_id).first()

            assert si_receiver2.buddy_status == 'N'
            assert si_receiver2.user.first_name in response2.text
            assert si_receiver2.user.last_name in response2.text
            assert str(si_receiver2.pro_score) in response2.text

        
            response2 = client.post('/findstudybuddy', 
                               data={"subject_code": course_id, "select_buddy": user_receiver.id, "select_buddy_but" : "1"}, follow_redirects=True)
        
            br = BuddyRelation.query.filter_by(buddy_sender=user_sender.id, buddy_receiver=user_receiver.id, study_interest_id=si_receiver2.id).first()
            
            assert br.invitation_status == 'S'
            assert response2.request.path == '/findbuddyconfirmation'
            assert b"Pending Buddy Relation Status" in response2.data
            assert b"Invitation has been sent, you will be notified when buddy responds" in response2.data
