## Author: Aaron Alakkadan 
from flask import url_for, request
from app.auth import email_content_password_reset, url_for, send_email
from unittest import mock
import random
from app.models.user import User
from app.models.studyinterest import *
from app.subjectselection import *
from app.models.buddyrelation import *
from app.models.buddyrating import *
import pytest


'''
This function tests if buddy rating is sucessfully completed with rewards points are displayed to the dashboard as well as the star rating
'''
@mock.patch("app.extensions.email.send", return_value=True, autospec=True)
@mock.patch("random.randint", return_value=5678, autospec=True)
def test_buddy_rate_and_reward_points_on_dashboard_success(mock_token2, mock_email, client):
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
            ## Also check when they select for a buddy that the invitation status has changed and then get redirected to the confirmation page

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

            response = client.get('/logout')
            assert response.request.path == '/logout'
       
            session.clear()

    #1st USER checks their pending invitation requests and clicks on the request and accepts the request
    response = client.get('/')
    assert response.request.path == '/'
    response = client.get('/login')
    assert response.request.path == '/login'
    with client:
        response = client.post('/login', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.request.path == '/dashboard'
        br = BuddyRelation.query.filter_by(buddy_sender=user_sender.id, buddy_receiver=user_receiver.id, study_interest_id=si_receiver.id).first()
        assert br.sender.first_name in response.text
        assert br.sender.last_name in response.text
        assert br.study_interest.course.course_name in response.text
        response = client.get(f"/invitation?id={br.id}")
        br = BuddyRelation.query.filter_by(buddy_sender=user_sender.id, buddy_receiver=user_receiver.id, study_interest_id=si_receiver.id).first()
        assert br.sender.first_name in response.text
        assert br.sender.last_name in response.text
        assert br.study_interest.course.course_name in response.text
        response = client.post(f"/invitation?id={br.id}", data={"accept_buddy_but": "1"})
        assert response.status_code == 200
        br = BuddyRelation.query.filter_by(buddy_sender=user_sender.id, buddy_receiver=user_receiver.id, study_interest_id=si_receiver.id).first()
        assert br.invitation_status == 'A'

        response = client.get('/logout')
        assert response.request.path == '/logout'
       
        session.clear()

    # 2nd user goes to dashboard and checks their connections and then rate the buddy 
    response = client.get('/')
    assert response.request.path == '/'
    response = client.get('/login')
    assert response.request.path == '/login'
    with client:
        response = client.post('/login', data={"username": username2 , "password": "ab1234"}, follow_redirects=True)
        assert response.request.path == '/dashboard'
        br = BuddyRelation.query.filter_by(buddy_sender=user_sender.id, buddy_receiver=user_receiver.id, study_interest_id=si_receiver.id).first()
        assert br.receiver.first_name in response.text
        assert br.receiver.last_name in response.text
        assert br.study_interest.course.course_name in response.text
        assert br.receiver.username in response.text

        # Rate your buddy
        # Check if buddy the user is rating for is displayed as well as the subject
        # Post data of the required fields with comments and rate the buddy with rewards points when answering yes for is gained knowledge
        # Check if you are taken to the confirmation page 
        response = client.get(f"/rate?id={br.id}")
        br_id = int(request.args.get("id"))
        br = BuddyRelation.query.filter_by(id=br_id).first()
        user = User.query.filter_by(username=current_user.username).first()
        buddy = br.get_buddy(current_user.username)
        buddy_id = buddy.id
        assert b"Buddy you are Rating:" in response.data
        assert buddy.first_name in response.text
        assert buddy.last_name in response.text
        assert b"Subject for Buddy you are Rating:" in response.data
        assert br.study_interest.course.course_name in response.text
        response = client.post(f"/rate?id={br_id}", data={"month": 3,
                                                        "year": 2023,
                                                        "is_score_improved": "No",
                                                        "is_gained_knowledge": "Yes", 
                                                        "buddy_rate": 2,  
                                                        "comment": "I gained some knowledge",
                                                        "rate_but": 1}, follow_redirects=True)
        
        br_rate = BuddyRating.query.filter_by(buddy_relation_id=br_id, rating_sender=user.id,
                                                  rating_receiver=buddy.id, month=3, year=2023).first()
        assert br_rate.is_survey_completed == True
        assert br_rate.buddy_rate == 2
        assert br_rate.reward_points == 5
        
        assert response.request.path == '/rateconfirmation'
        assert b"You have successfully rated your buddy"  in response.data

        response = client.get('/logout')
        assert response.request.path == '/logout'
       
        session.clear()
   
    # 1st user goes to dashboard and rewards points along with the buddy rating should be displayed to the user
    response = client.get('/')
    assert response.request.path == '/'
    response = client.get('/login')
    assert response.request.path == '/login'
    with client:
        response = client.post('/login', data={"username": username , "password": "ge3456"}, follow_redirects=True)
        assert response.request.path == '/dashboard'
        
        # Checking if thhe correct data for your connections is displayed
        br = BuddyRelation.query.filter_by(buddy_sender=user_sender.id, buddy_receiver=user_receiver.id, study_interest_id=si_receiver.id).first()
        assert br.sender.first_name in response.text
        assert br.sender.last_name in response.text
        assert br.study_interest.course.course_name in response.text
        assert br.sender.username in response.text
        
        # Checking if the correct data for rewards points is displayed
        user = User.query.filter_by(id=buddy_id).first()
        assert str(user.total_reward_points) in response.text

        #Checking if the correct data for subjects and buddy rating is displayed
        si = StudyInterest.query.filter_by(user_id=buddy_id, course_id=course_id).first()
        assert si.course.subject_code in response.text
        assert si.course.course_number in response.text
        assert si.course.course_name in response.text
        assert str(si.buddy_star_rating) in response.text


