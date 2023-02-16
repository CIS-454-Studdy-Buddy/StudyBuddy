import unittest
from app.auth import RegisterForm
from app.models.user import User 



class MyEmailTest(unittest.TestCase):
    def test_email(self):
        with self.request(method='POST', data={"username": "bobby@hotmail.com", "password": "ge516"}):
            f = RegisterForm(request.form, csrf_enabled=False)
            self.assertEquals(f.validate_username("bobby"))
        
     
