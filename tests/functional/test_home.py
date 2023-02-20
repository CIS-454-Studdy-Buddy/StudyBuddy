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
    assert b"Study Buddy" in response.data
    assert b"Studying Alone?" in response.data
    assert b"Study Buddy is a service where students can help each other succeed in their studies." in response.data
    assert b"Also, it's a" in response.data
    assert b"great way to meet students in your major and making long lasting connections!" in response.data
    assert b"Find your Buddy today!" in response.data

'''
The function checks if the links on the home page redirects to the right corresponding page
'''
def test_home_links_work(client):
    response = client.get("/")
    assert "/login" in response.text
    assert "/signup" in response.text