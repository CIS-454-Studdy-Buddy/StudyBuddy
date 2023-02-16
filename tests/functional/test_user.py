from app.auth import RegisterForm


def test_signup_new_user(client):

    response = client.post("/signup", data={"username": "bobby@syr.edu", "password": "ge3456"})
    assert response.status_code == 200

  


def test_signup_existing_user(client):

    response = client.post("/signup", data={"username": "bobby@syr.edu", "password": "ge3456"})
    assert response.status_code == 200
    response = client.post("/signup", data={"username": "bobby@syr.edu", "password": "ge3456"})
    assert b"That username already exists. Please choose a different one." in response.data
     
   



