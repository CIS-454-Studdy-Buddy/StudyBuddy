

def test_home_is_presented(client): 
    response = client.get("/")
    assert b"SU Study Buddy!" in response.data