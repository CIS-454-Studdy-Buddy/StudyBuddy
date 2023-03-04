## Author: Talal Hakki
from flask import url_for, request
from app.auth import email_content_password_reset, url_for, send_email
from unittest import mock
import random
from app.models.user import User
from app.models.studyinterest import *
from app.subjectselection import *
from app.models.buddyrelation import *
import pytest



@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=5678, autospec=True)
#@mock.patch("random.randint", return_value=1234, autospec=True)
def test_find_buddy(mock_token2, mock_email, client):
    # send data to signup using post method
    # redirects to email confirmation
    username = "validt@syr.edu"
    first_name = "Bobby"
    last_name = "Goldstein"
    response = client.post("/signup", data={"first_name": first_name, "last_name": last_name,
                                            "username": username, "password": "ge3456",
                                            "re_enter_password": "ge3456"}, follow_redirects=True)
    #print(mock_token.return_value)
    #assert mock_token.return_value == 1234
    assert response.status_code == 200
    assert response.request.path == '/emailconfirmation'

    with client:
        # Simulate email verification click 
        # send data to login using post method with the right token redirection which is 1234
        # logged in by clicking the link in the confirmation email and not manipulating the token
        # therefore the user is redirected to the dashboard page  
        response = client.post('/login?t=5678', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username=username).first()
        print("User 1 user:", user.username)
        print("User 1 token:", user.token)
        print("User 1 first name:", user.first_name)
        assert user.username == username
        assert user.token == '5678'
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


        response = client.get('/logout')
        assert response.request.path == '/logout'
    
    
        session.clear()
        
    
    #2nd USER
    response = client.get('/')
    assert response.request.path == '/'
    with mock.patch("random.randint", return_value='1234', autospec=True):
        print("2nd User")
        

    

        username2 = "testing@syr.edu"
        first_name2 = "James"
        last_name2 = "Albert"
        response2 = client.post("/signup", data={"first_name": first_name2, "last_name": last_name2, 
                                            "username": username2, "password": "ab1234", 
                                            "re_enter_password": "ab1234"}, follow_redirects=True)

        #assert mock_token2.return_value == 1234
        assert response2.status_code == 200 
        assert response2.request.path == '/emailconfirmation'

        with client:
            # Simulate email verification click 
            # send data to login using post method with the right token redirection which is 1234
            # logged in by clicking the link in the confirmation email and not manipulating the token
            # therefore the user is redirected to the dashboard page  
            response2 = client.post('/login?t=1234', data={"username": username2 , "password": "ab1234"}, follow_redirects=True)
            assert response2.status_code == 200
            print("USERNAME2", username2)
            user2 = User.query.filter_by(username=username2).first()
            print("User 2 user:", user2.username)
            print("User 2 token:", user2.token)
            print("User 2 first name:", user2.first_name)
            print(user2.token)
            assert user2.username == username2
            assert user2.token == '1234'
            assert user2.is_verified
            assert response2.request.path == '/dashboard'

            # Go to the subject selection page
            response2 = client.get('/subjectselection')
            assert response2.status_code == 200
            assert response2.request.path == '/subjectselection'
            course = Course.query.filter_by(subject_code="CIS").first()
            course_id = course.id
            user2 = User.query.filter_by(username=current_user.username).first()
            response2 = client.post('/subjectselection', 
                               data={"subject_code": "CIS", "course_title": course_id, "pro_ans1": "2", "pro_ans2": "2", "pro_ans3" : "2", "but" : "1"}, follow_redirects=True)
            si = StudyInterest.query.filter_by(user_id=user2.id).filter_by(course_id=course.id).first()

            ## Go to findstudybuddy page
            ## select subject and check if users that have selected the subject and thier avg. score are displayed on page

            response2 = client.get('/findstudybuddy')
            assert response2.status_code == 200
            assert response2.request.path == '/findstudybuddy'

        
            response2 = client.post('/findstudybuddy', 
                               data={"subject_code": "CIS 151 - Fundamentals of Computing and Programming", "buddy_but" : "1"}, follow_redirects=True)
            
            print(first_name, last_name, str(si.pro_score))
            u1 = first_name + " " + last_name + " " + str(si.pro_score)
            print(response2.text)
            #assert u1 in response2.data
            #print(course.course_name)
            #print(course)


            #siBud = BuddyRelation.query.filter_by(buddy_sender=current_user.id, buddy_receiver=receiver.first_name, study_interest_id=si).first()
            
            
            #print(siBud.user.first_name)
            
            #print(si.user.first_name)
            #assert first_name in response2.text
            #print(response2.text)
            #assert username in response2.text
            #print(response2.text)

            # testing if the selected subject and its averge proficiency test score
            # is successfully displayed to the user on the subjectselection web page
            #print(course.subject_code)
            #print(response2.text)
            #assert course.subject_code in response2.text
            #assert course.course_number in response2.text
            #assert course.course_name in response2.text
            #assert str(si.pro_score) in response2.text

            assert False == True








        
    

        

        
    
    











    

