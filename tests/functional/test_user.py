from app.auth import RegisterForm

def test_signup_new_user(client):

    response = client.post("/signup", data={"username": "bobby@syr.edu", "password": "ge3456"})
    assert response.status_code == 200

    
def test_signup_failed_email_syr_new_user(client):
    response = client.post("/signup", data={"username": "bobby@gmail.com", "password": "ge3456"})
    assert response.status_code == 200
    assert b"email address must syracuse university email address" in response.data

def test_signup_username_not_email(client):
    response = client.post("/signup", data={"username": "bobby", "password": "ge3456"})
    assert response.status_code == 200
    assert b"The email address is not valid. It must have exactly one @-sign." in response.data
    assert b"email address must syracuse university email address" in response.data

  

def test_signup_existing_user(client):

    response = client.post("/signup", data={"username": "bobby@syr.edu", "password": "ge3456"})
    assert response.status_code == 200
    response = client.post("/signup", data={"username": "bobby@syr.edu", "password": "ge3456"})
    assert b"That username already exists. Please choose a different one." in response.data
     
def test_user_not_existing(client):
    response = client.post("/login", data={"username": "nonexistent@syr.edu", "password": "ge3456"}, follow_redirects=True)
    assert response.status_code == 200
    print(response.data)
    assert b"Invalid Login" in response.data




