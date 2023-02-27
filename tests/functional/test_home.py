'''
Author: Aaron Alakkadan 
'''
from flask import url_for, request
import app.auth

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