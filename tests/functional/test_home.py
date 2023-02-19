

def test_home_is_presented(client): 
    response = client.get("/")
    assert b"SU Buddy Landing Page" in response.data