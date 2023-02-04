

def test_signup_new_user(client):

    response = client.post("/signup", data={"username": "bobby", "password": "ge3456"})
    assert response.status_code == 200

  


def test_signup_existing_user(client):

    response = client.post("/signup", data={"username": "bobby", "password": "ge3456"})
    assert response.status_code == 200
    response = client.post("/signup", data={"username": "bobby", "password": "ge3456"})
    assert b"Invalid SignUp" in response.data 
  




