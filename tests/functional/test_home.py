

def test_home_is_presented(client): 
    response = client.get("/")
    assert b"<title>Home</title>" in response.data