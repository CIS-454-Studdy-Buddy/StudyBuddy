def test_home(client): 
    response = client.get("/")
    assert b"<h1>Login Authentication System in Flask</h1>" in response.data